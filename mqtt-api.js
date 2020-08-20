var net = require('net');
var utill = require('util');
var mqtt = require('mqtt');

var topic = 'sensors/connect';
var option = {
	host: '192.168.0.73',
	port: 1883,
	username: 'gateway',
};

var client = mqtt.connect(option);
client.on('connect', ()=> {
	console.log('MQTT Client connected');
});
client.on('error', (error) => {
	console.log('MQTT Client connect failed');
});

function send() {
	data = 199.1
	console.log('temperature:' + data);
	msg = {'serialNumber':'SN-001', 'model':'T1000','temperature':data};
	client.publish(topic, JSON.stringify(msg));
}

send()
client.end()
process.exit()
