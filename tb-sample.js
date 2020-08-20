var mqtt = require('mqtt');
var broker = 'mqtt://127.0.0.1:1883';
var device = 'SN-001';
var client  = mqtt.connect(broker, {
  // Will topic to report that device is disconnected 
  will: {topic: 'sensors/' + device + '/disconnect', payload: '', qos: 1}
});

client.on('connect', function () {
    console.log('connected');
    // Report that device is connected to the gateway
    client.publish('sensors/' + device + '/connect', '');
    // Subscribe to RPC requests topic
    client.subscribe('sensors/' + device + '/request/+/+');
});

client.on('message', function (topic, message) {
    console.log('request.topic: ' + topic);
    console.log('request.body: ' + message.toString());
    console.log('response.topic: ' + topic.replace('request','response'));
    // Publish the response that will simply echo the request.
    client.publish(topic.replace('request','response'), message);
});
