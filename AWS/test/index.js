const mqtt = require('mqtt')
const fs = require('fs');

const clientOptions = {
    clientID: "mqttjs01",
    username: "webapp",
    password: "=ZCJ=4uzfZZZ#36f",

    key: fs.readFileSync('../cert/webapp.key'),
    cert: fs.readFileSync('../cert/webapp.crt'),
    ca: [ fs.readFileSync('../cert/ca.crt') ]
}

var client = mqtt.connect('mqtts://thecanary.duckdns.org', clientOptions);

// Runs on connection to the broker
client.on("connect", () => {
	console.log("connected " + client.connected);
	// Subscribes to topics on startup
	let topic = 'test/#';
	client.subscribe(topic, (err, granted) => {
		if (err) {
		 console.log(err);
		 process.kill(process.pid, 'SIGTERM');
		}
		console.log('Subscribed to topic: ' + topic);
	});
	// Testing publishing ability
	publish('test/test','Hello from backend (securely)');
})

// Runs if unable to connect to broker
client.on("error", error => {
	console.log("Cannot connect " + error);
	process.kill(process.pid, 'SIGTERM');
});

client.on('message', (topic, message, packet) => {
    if (topic === "test/test") {
        console.log(message.toString());
    }
})

const pubOptions={
	retain:true,
	qos:1
};

// You can call this function to publish to things
function publish(topic,msg,options=pubOptions){
	console.log("publishing",msg);
	if (client.connected == true){
		client.publish(topic,msg,options);
		}
}