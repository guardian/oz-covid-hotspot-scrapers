
const fetch = require('node-fetch')
const D3Node    = require('d3-node');
const moment = require("moment-timezone")
const AWS = require('aws-sdk')
const s3 = new AWS.S3()
const svgToDataURL = require('svg-to-dataurl')

function fetcher() {

    return new Promise( (resolve, reject) => {

        Promise.all([
          fetch('https://interactive.guim.co.uk/yacht-charter-data/aus-national-total-corona-cases.json').then(res => res.json()),
          fetch('https://interactive.guim.co.uk/yacht-charter-data/oz_vaccine_tracker_goals_trend_three_trend.json').then(res => res.json())
        ]).then(json => {
            resolve(json)
        })
        .catch((err) => {
            reject(err)
        });

    });
}

async function create(datum, today) {

	const d3n   = new D3Node();

	const d3    = d3n.d3;

	var data = datum.map(item => {
		return { index : d3.timeParse("%Y-%m-%d")(item.index), cases : item['New cases']}
	})

	var forthnight = data.slice(Math.max(data.length - 14, 0))

	var week =  forthnight.slice(Math.max(forthnight.length - 7, 0))

	var cases = sum (week, 'cases')

	var previous = sum ( forthnight.slice(0, 7) , 'cases' )

	var direction = (cases > previous) ? '+' : (cases < previous) ? '-' : '' ;

	var diff = difference(cases, previous)

	var ctx = (cases === previous) ? '' : `${direction}${diff} v last week` ;

	var payload = { cases : cases, previous : previous, difference : `${ctx}` }

	var margin = { top: 15, right: 15, bottom: 15, left: 15 },
	    width = (244 * 3) - margin.left - margin.right,
	    height = (100 * 3) - margin.top - margin.bottom;

	const svg = d3n.createSVG(width, height)
					.attr("preserveAspectRatio", "xMinYMin meet")
					.attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
					.classed("svg-content", true)
				    
	var grouped = svg.append("g")
					.attr("transform","translate(" + margin.left + "," + margin.top + ")");

	var x = d3.scaleTime()
	      .domain(d3.extent(data, function(d) { return d.index; }))
	      .range([ 0, width ]);

	var y = d3.scaleLinear()
		.domain([0, d3.max(data, function(d) { return +d.cases; })])
		.range([ height, 0 ]);

   	grouped.append("path")
		.datum(data)
		.attr("fill", "#e24c67")
		.attr("stroke", "#e6001f")
		.attr("stroke-width", 1.5)
		.attr("d", d3.area()
			.x(function(d) { return x(d.index) })
			.y0(y(0))
			.y1(function(d) { return y(d.cases) })
		)

	var chart = await d3n.svgString()

	return  { payload : payload , chart : chart }

}

async function goals(results, today) {

	const d3n   = new D3Node();

	const d3    = d3n.d3;

	var margin = { top: 15, right: 15, bottom: 15, left: 15 },
	    width = (244 * 3) - margin.left - margin.right,
	    height = (100 * 3) - margin.top - margin.bottom;

	const svg = d3n.createSVG(width, height)
						.attr("preserveAspectRatio", "xMinYMin meet")
						.attr("viewBox", `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
						.classed("svg-content", true)
						.attr("overflow", "hidden");					

	var clone = clone = JSON.parse(JSON.stringify(results));

	var data = clone.sheets.data

	var details = clone.sheets.template

	var labels = clone.sheets.labels

	var userKey = clone['sheets']['key']

	var breaks = "no"

	var dateParse = d3.timeParse(details[0]['dateFormat'])

	data = data.filter(d => dateParse(d.Date) <= dateParse(today))

	var keys = Object.keys(data[0])	

	var doses = keys[1]

	data = data.map(d => {
		return { date : d.Date, doses : d[doses], goal : d["Current goal"]}
	})

	keys = Object.keys(data[0])	

	var vaccination = data.find(d => d.date == today)

	var diff = vaccination.goal - vaccination.doses

	var percentage = 100 / 25693000 * vaccination.doses

	var payload = { total : numberFormat(vaccination.doses), gap : numberFormat(diff), percentage : percentage.toFixed(1) }

	var features = svg.append("g").attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	var xVar;

	if (details[0]['xColumn']) {
		xVar = details[0]['xColumn'];
		keys.splice(keys.indexOf(xVar), 1);
	} else {
		xVar = keys[0]
	 	keys.splice(0, 1);
	}
	
	var colors = ["#d10a10", "#ea5a0b", "#cccccc","#adadad", "#d10a10"];

	var color = d3.scaleOrdinal();

	color.domain(keys).range(colors);
	
	var x = d3.scaleTime()
		.rangeRound([0, width]);

	var y = d3.scaleLinear()
		.rangeRound([height, 0]);

	var color = d3.scaleOrdinal()
		.range(colors);	

	var lineGenerators = {};

	var allValues = [];

	keys.forEach(function(key, i) {

		if (breaks === "yes") {
			lineGenerators[key] = d3.line().defined(function(d) {
				return d;
			}).x(function(d) {
				return x(d[xVar]);
			}).y(function(d) {
				return y(d[key]);
			});
		} else if (breaks === "no") {
			lineGenerators[key] = d3.line().x(function(d) {
				return x(d[xVar]);
			}).y(function(d) {
				return y(d[key]);
			});
		}

		
		data.forEach(function(d) {
			if (typeof d[key] == 'string') {
				if (d[key].includes(",")) {
					if (!isNaN((d[key]).replace(/,/g, ""))) {
						d[key] = +(d[key]).replace(/,/g, "")
						allValues.push(d[key]);
					}
				} else if (d[key] != "") {
					if (!isNaN(d[key])) {
						d[key] = +d[key]
						allValues.push(d[key]);
					}
				} else if (d[key] == "") {
					d[key] = null
				}
			} else {
				allValues.push(d[key]);
			}
		});
	});

	data.forEach(function(d) {
		if (typeof d[xVar] == 'string') {	
			d[xVar] = dateParse(d[xVar])
		}	
	})

	var keyData = {}

	keys.forEach(function(key, i) {
		keyData[key] = []
		data.forEach(function(d) {
			if (d[key] != null) {
				var newData = {}
				newData[xVar] = d[xVar]
				newData[key] = d[key]
				keyData[key].push(newData)
			} else if (breaks == "yes") {
				keyData[key].push(null)
			}
		});
	})

	var shorter_data = data.filter(d => d.date >= dateParse("2021-04-15") )

	var areaData = shorter_data.filter(d => {return d[xVar] <= keyData[keys[0]][keyData[keys[0]].length - 1][xVar] })

	const area = d3.area().x((d) => x(d[xVar])).y0((d) => {
		return y(d[keys[0]])
	}).y1((d) => y(d[keys[1]]))

	labels.forEach(function(d, i) {
		if (typeof d.x == 'string') {
			d.x = dateParse(d.x);
		}
		if (typeof d.y == 'string') {
			d.y = +d.y;
		}
		if (typeof d.offset == 'string') {
			d.offset = +d.offset;
		}
	})

	var min = (details[0]['baseline'] === 'zero') ? 0 : d3.min(allValues);

	x.domain(d3.extent(data, function(d) { return d[xVar]; }));

	y.domain([0, d3.max(allValues)])

	svg.append("svg:defs").append("svg:marker")
		.attr("id", "arrow")
		.attr("refX", 6)
		.attr("refY", 6)
		.attr("markerWidth", 20)
		.attr("markerHeight", 20)
		.attr("markerUnits","userSpaceOnUse")
		.attr("orient", "auto")
		.append("path")
		.attr("d", "M 0 0 12 6 0 12 3 6")
		.style("fill", "black")

	features.append("path")
			.datum(areaData)
			.attr("class", "areaPath")
			.attr("fill", "rgb(245, 189, 44)")
			.attr("opacity", 0.6)
			.attr("stroke", "none")
			.attr("d", area)		

	keys.forEach(function(key, i) {

		features.append("path").datum(keyData[key]).attr("fill", "none").attr("stroke", function(d) {
			return color(key);
		}).attr("stroke-linejoin", "round").attr("stroke-linecap", "round").attr("stroke-width", 3).attr("d", lineGenerators[key]);

	});

	var chart = await d3n.svgString()

	return  { payload : payload , chart : chart }

}

async function writer(data, filepath) {

	let s3params = {
	    Bucket: "gdn-cdn",
	    ACL: 'public-read',
	    ContentType: 'application/json',
	    CacheControl: 'max-age=300'
	}

    s3params.Body = data;

    s3params.Key = filepath

    await s3.upload(s3params).promise().then((arg) => {

        return arg

    })  

    return { status : filepath }

}

async function wrapper() {

	const aust = moment();

	const today = aust.tz('Australia/Melbourne').format('YYYY-MM-DD');

	const data = await fetcher()

	const chart1 = await goals(data[1], today)

	const gap = svgToDataURL('<?xml version="1.0" encoding="utf-8"?>' + chart1.chart)

	const chart2 = await create(data[0].sheets.data, today)

	const cases = svgToDataURL('<?xml version="1.0" encoding="utf-8"?>' + chart2.chart)

	const json = { ...chart1.payload, ...chart2.payload }

	json.gap_image = `${gap}`

	json.cases_image = `${cases}`

	json.updated = aust.tz('Australia/Melbourne').format('LL');

	const message3 = await writer(JSON.stringify(json), "embed/aus/thrashers/vaccine-tracker/vaccine-thrasher.json")

	return { ...chart1.payload, ...chart2.payload }

}

exports.handler = async (event) => {
    
    const response = await wrapper()

    return response

};

function numberFormat(num) {
  if ( num > 0 ) {
      if ( num > 1000000000 ) { return ( num / 1000000000 ).toFixed(1) + 'bn' }
      if ( num >= 1000000 ) { return ( num / 1000000 ).toFixed(1) + 'm' }
      if ( num > 1000 ) { return ( num / 1000 ).toFixed(1) + 'k' }
      if (num % 1 != 0) { return num.toFixed(2) }
      else { return num.toLocaleString() }
  }
  if ( num < 0 ) {
      var posNum = num * -1;
      if ( posNum > 1000000000 ) return [ "-" + String(( posNum / 1000000000 )) + 'bn'];
      if ( posNum > 1000000 ) return ["-" + String(( posNum / 1000000 )) + 'm'];
      if ( posNum > 1000 ) return ["-" + String(( posNum / 1000 )) + 'k'];
      else { return num.toLocaleString() }
  }
  return num;
}

function sum(arr, prop) {

    let total = 0
    for ( var i = 0, _len = arr.length; i < _len; i++ ) {
        total += arr[i][prop]
    }
    return total
}

function difference(a, b) { 
	return Math.abs(a - b); 
}

