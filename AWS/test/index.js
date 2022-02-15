const mqtt = require('mqtt')

const clientOptions = {
    clientID: "mqttjs01",
    username: "webapp",
    rejectUnauthorized: false
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
	publish('test/test','hello from backend');
})

// Runs if unable to connect to broker
client.on("error", error => {
	console.log("cannot connect " + error);
	process.kill(process.pid, 'SIGTERM');
});