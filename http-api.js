const request = require('request');
var fs = require('fs');
//var data = fs.readFileSync('./test_rule_chain.json');
//var data = {"serialNumber":"SN-001", "model":"T1000", "illuminance":256.0}
var data = {"illuminance":100.0}
const options = {
    url: 'http://192.168.0.62:8080/api/v1/gateway/telemetry',
    method: 'POST',
    json: true,
    body: JSON.stringify(data),
};

const get_options = {
    url: 'http://127.0.0.1:8080/api/v1/illumacc/attributes',
    method: 'GET',
};

function post(){
    request.post(options, function(error, response, body) {
        if (error) {
            console.log(error);
        }else {
           console.log(response.statusCode);
           console.log("post success");
        }
    });
}

function get(){
    request.get(get_options, function(error, response, body){
        if (error) {
            console.log(error);
        }else {
            console.log(response.statusCode);
            console.log(body);
        }
    });
}

//get();
post()
