const fetch = require('node-fetch')

const AWS = require('aws-sdk')

const s3 = new AWS.S3()

var s3params = {
    Bucket: "gdn-cdn",
    ACL: 'public-read',
    ContentType: 'application/json',
    CacheControl: 'max-age=300'
}

async function wrapper() {

    const data = await fetcher()

    const instructions = await wrangle(data)

    let status = (instructions.update) ? true : false ;

    let message = "Nothing to see here. Move along."

    if (status) {

        s3params.Body = JSON.stringify(instructions.payload);

        s3params.Key = 'embed/aus/feeds/vaccine/vaccine-eligibility-in-australia.json'

        await s3.upload(s3params).promise().then((arg) => {

            return arg

        })  

        message = `Updated vaccine eligibility tracker feed - version ${instructions.f2}. The government vaccine tracker was updated. The Guardian feed has been updated from version ${instructions.f1} to version ${instructions.f2}. You should check that the Guarduan vaccine eligibility tracker is still working`

    }

    return { status : status,  message : message }

}

function fetcher() {

    return new Promise( (resolve, reject) => {

        Promise.all([
          fetch('https://covid-vaccine.healthdirect.gov.au/rules.json').then(res => res.json()),
          fetch('https://interactive.guim.co.uk/embed/aus/feeds/vaccine/vaccine-eligibility-in-australia.json').then(res => res.json())
        ]).then(json => {
            resolve(json)
        })
        .catch((err) => {
            reject(err)
        });

    });
}

async function wrangle(data) {

    var version = { origin : +data[0].version, destination : +data[1].version }

    var instructions = { update : (version.origin > version.destination) ? true : false , payload : data[0], f1: data[0].version, f2 : data[1].version }

    return instructions

}

exports.handler = async (event) => {
    
    const response = await wrapper()

    return response

};
