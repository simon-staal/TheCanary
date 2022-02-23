//Initialising HTTP variables
const express = require("express");
const path = require("path");
const cors = require('cors');

const PORT = process.env.PORT || 8000;

const app = express();

app.use(express.static(path.resolve(__dirname, '../client/build')));

app.use(express.json());

app.use(express.urlencoded({ extended: true })) ;

app.use(cors());

//Initialise MongoDB database
const { MongoClient, ServerApiVersion } = require('mongodb');

const uri = "mongodb+srv://TheCanary:bn8Ek7ILbvLxlBMy@cluster0.zplcu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority";
const oldDataColl = "HistoricalData";
const currDataColl = "CurrentData";

const DBClient = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });
var db;

// Initialize connection once
DBClient.connect((err) => {
    if(err) {
        console.log(err);
        throw err;
    }
    db = DBClient.db("TheCanary");
  // Start the application after the database connection is ready
    app.listen(PORT, () => {
        console.log("Browser server listening on " + PORT);
    });
});



//front-end requesting current data for each miner
app.get("/miners", (req, res) => {
    //const miners = [{id: "Team 1", data: ["sensor data", "air pressure"]}, {id:"Team 2", data: ["sensor data"]},
    //{id:"Team 3", data: ["sensor data"]},{id:"Team 4", data: ["sensor data"]}];
    res.send( getMiners());
  });

//front-end requesting historical data for one miner
app.get("/graph", (req, res) => {
    const minerId = req.query.id;
    //const data = {y: [4,2,2,3,7,8,5], x: ["Jan", "Febr", "Mar", "Apr", "May", "June", "July"]};
    res.send( getHistoricalData(minerId));
    //get data from database
});



app.use('/login', (req, res) => {
    res.send({
      token: 'test123'
    });
  });

//front-end updating sampling frequency
//need to send it down to each pi
app.post('/freq', (req, res)=>{
    publish('sensor/instructions/sampling', req.body.global);
    res.send('OK');
});



//------- HTTP done, MQTT from here

const mqtt=require('mqtt');
const fs = require('fs');
const { cursorTo } = require("readline");
const { resolve } = require("path/posix");

const clientOptions = {
    clientID: "mqttjs01",
    username: "webapp",
    password: "=ZCJ=4uzfZZZ#36f",

    key: fs.readFileSync('../../AWS/cert/webapp.key'), // MAKE SURE THE FILEPATH IS CORRECT
    cert: fs.readFileSync('../../AWS/cert/webapp.crt'),
    ca: [ fs.readFileSync('../../AWS/cert/ca.crt') ]
}
var MQTTclient = mqtt.connect('mqtts://thecanary.duckdns.org', clientOptions);

// Runs on connection to the broker
MQTTclient.on("connect", () => {
	console.log("connected " + client.connected);
	// Subscribes to topics on startup
	let topic = 'sensor/data';
	MQTTclient.subscribe(topic, (err, granted) => {
		if (err) {
		 console.log(err);
		 process.kill(process.pid, 'SIGTERM');
		}
		console.log('Subscribed to topics: ' + topic);
	});
	// Testing publishing ability
	publish('test/test','Hello from backend (securely)');
})

// Runs if unable to connect to broker
MQTTclient.on("error", error => {
	console.log("Cannot connect " + error);
	process.kill(process.pid, 'SIGTERM');
});


// Handles receiving messages from the broker
client.on('message', (topic, message, packet) => {
	if (topic === "sensor/data") {
		console.log(message.toString());
        addNewData(message.id, message.data);
	}
})

const pubOptions={
	retain:false,
	qos:1
};

// You can call this function to publish to things
function publish(topic,msg,options=pubOptions){
	console.log("publishing",msg);
	if (client.connected == true){
		client.publish(topic,msg,options);
	}
}

// Helper functions

//gets the current miner data from the database and returns them in an array
function getMiners() {
    db.collection(currDataColl).find({}, { projection: { _id: 0, id: 1, data: 1 } }).toArray((err, result) => {
        if(err){
            console.log(err);
            throw err;
        }
        resolve(result);
    }).then((res)=>{return res;})
}

function getHistoricalData(id) {
    var query = {id: id};
    let y = [];
    let x = [];
    const cursor = db.collection(oldDataColl).find(query, { projection: { _id: 0, data: 1, time:1 }})
    await cursor.toArray((err,res) => {
        if(err){
            console.log(err);
            throw err;
        }

        res.map((elem)=>{
            y.push(elem.data);
            x.push(elem.time);
        });
    })
    return {x:x,y:y}
}

function addNewData(id, data) {
    var query = {id: id};
    //delete data for this id form database
    db.collection(currDataColl).deleteMany(query,(err, obj) => {
        if (err){
            console.log(err);
            throw err;
        }
        else {
            console.log(obj.result.n + " document(s) deleted");
            db.collection(currDataColl).insertOne({id:id, data:data,time: newDate()}, function(err, res) {
                if (err){
                    console.log(err);
                    throw err;
                }
            }); 
        }
    });
    db.collection(currDataColl).insertOne({id:id, data:data,time: newDate()}, function(err, res) {
        if (err){
            console.log(err);
            throw err;
        }
    });
}

