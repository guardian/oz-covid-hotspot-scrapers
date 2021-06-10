const AWS = require('aws-sdk')
//const puppeteer = require('puppeteer');
const chromium = require('chrome-aws-lambda');
const fetch = require('node-fetch')
const cheerio = require('cheerio')
const cheerioTableparser = require('cheerio-tableparser');
const contains = require('./contains')
const agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'
const timer = ms => new Promise(res => setTimeout(res, ms)) 
const s3 = new AWS.S3()

let s3params = {
    Bucket: "gdn-cdn",
    ACL: 'public-read',
    ContentType: 'application/json',
    CacheControl: 'max-age=300'
}

let database = []

async function wrapper() {

	let feed = await feedburner()

	let upload = await compare(feed)

	let message = 'Public exposure sites in victoria'

	let status = ( upload.exists==false && feed.length > 0 ) ? true : false ;

	console.log(`Feed length ${feed.length}, Feed exists? ${upload.exists}, status : ${status}`)

	if (status) {

		var gdoc = {
			"sheets": {
				"table": feed,
				"template": [],
				"options": [{
					"format": "scrolling",
					"enableSearch": "TRUE",
					"enableSort": "TRUE"
				}],
				"key": [],
				"chartId": [{
					"type": "table"
				}]
			}
		}

		s3params.Body = JSON.stringify(gdoc);

		s3params.Key = 'embed/aus/feeds/covid/public-exposure-sites-in-victoria.json'

		await s3.upload(s3params).promise().then((arg) => {

		  	return arg

		})	

		message = `A new feed with ${feed.length} public exposure sites in victoria has been uploaded`

	}

  	return { status : status,  message : message, feed : feed.length }

}

async function feedburner() {

	let result = null;
	let browser = null;
	let array = []

	try {

		browser = await chromium.puppeteer.launch({
		  args: chromium.args,
		  defaultViewport: chromium.defaultViewport,
		  executablePath: await chromium.executablePath,
		  headless: chromium.headless,
		  ignoreHTTPSErrors: true,
		});

		let page = await browser.newPage();

		await page.setUserAgent(agent)

		await page.goto('https://www.coronavirus.vic.gov.au/exposure-sites');

		let i = 0;

		let unique = false

		do {

			i = i + 1;

			let bodyHTML = await page.evaluate(() => document.body.innerHTML);

			let table = await wrangle(bodyHTML)	

			let $ = cheerio.load(bodyHTML);

			unique = ($(".rpl-pagination__nav").last().attr('disabled')==='disabled') ? false : true ;

			for await (const item of table) { 

				database.push( item )
			
			}

			console.log(`Page ${i}, incidents on page ${table.length}`)

			if (unique) {

				let button = await page.$$(".rpl-pagination__nav");

				let index = (i === 1) ? 0 : 1 ;

				await button[index].click();

			}

			await timer(250);

		} while (unique);

		await browser.close();

		let set = new Set(database)

		array = Array.from(set);

		await page.close();

		await browser.close();

	} catch (error) {

		console.log(error)

	} finally {

		if (browser !== null) {

		  await browser.close();

		}

	}

	return array;

}

async function wrangle(body) {

  return new Promise(function(resolve, reject) {

	try {

	    let $ = cheerio.load(body);

		cheerioTableparser($);

		var columns = $(`table`).parsetable();

		var rows = ["Suburb",
					"Site",
					"Exposure period",
					"Notes",
					"Date added",
					"Health advice"]

		var table = []

		for (let column of columns) {

			if (contains(rows, column[0])) {

				column.shift()

				table.push(column)

			}

		}

		var json = []

		for (var item = 0; item < table[0].length; item++) {

			var obj = {}

			for (var i = 0; i < rows.length; i++) {

				try {

					obj[rows[i]] = table[i][item]

				} catch(err) {


				}
			}

			if (obj.Notes != undefined) {

				json.push(obj)

			}

		}

		resolve(json)

	} catch(err) {

	  reject(err)

	}

  });

}

async function compare(feed) {

	return new Promise( (resolve, reject) => {

		fetch("https://interactive.guim.co.uk/embed/aus/feeds/covid/public-exposure-sites-in-victoria.json")
		    .then(res => res.json())
		    .then(json => {
		    	var upload = (JSON.stringify(json.sheets.table)===JSON.stringify(feed)) ? { exists : true } : { exists : false } 
				resolve(upload);
		    })
		   .catch((err) => {
          		reject(err)
      		});

	})

}


exports.handler = async (event) => {
    
    const response = await wrapper()

    return response;

};
