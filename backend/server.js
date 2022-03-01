//Initialising HTTP variables
const express = require("express");
const path = require("path");
const cors = require('cors');
const jwt = require('jsonwebtoken');
const fs = require('fs');
const https = require('https')

const PORT = process.env.PORT || 8000;
const HTTPS_PORT = 8443;

const app = express();

app.use(express.static(path.resolve(__dirname, '../client/build')));
app.use(express.json());
app.use(express.urlencoded({ extended: true })) ;
app.use(cors());

// Setup certificates for encrypted communication with front-end
const cert = fs.readFileSync('/etc/letsencrypt/live/thecanary.duckdns.org/fullchain.pem', 'utf8');
const key = fs.readFileSync('/etc/letsencrypt/live/thecanary.duckdns.org/privkey.pem', 'utf8');
const SSL_options = {
  key: key,
  cert: cert
};
const httpsServer = https.createServer(SSL_options, app);

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
    httpsServer.listen(HTTPS_PORT, () => {
        console.log(`Listening with HTTPS at thecanary.duckdns.org:${HTTPS_PORT}`);
    })
});


// Can be accessed without authentication
app.get('/', (req, res) => {
    console.log(req.body)
    res.send("Welcome to our API!")
})

// Key used for signing login token
const privateKey = fs.readFileSync('../AWS/cert/webapp.key')

// Used to authenticate the user
// If successful this returns a session token to be included as part of the query parameters for all subsequent endpoint calls
app.post('/login', (req, res) => {
    // Purely for demonstrative purposes, if we had actual users we would store users + password hashes in a database, and compare to those
    console.log(req.body)
    if (req.body.username === 'admin' && req.body.password === "password") {
        let token = jwt.sign({ token: 'poggers'}, privateKey);
        res.send({token: token});
    }
    else {
        res.status(401).send({ name: "AuthenticationError", message: "Invalid Credentials"});
    }
});

//front-end requesting current data for each miner
app.get("/miners", (req, res) => {
    authenticateThenDo(req, res, async () => {
        try {
            const miners = await getMiners()
            console.log(miners)
            res.send(miners)
        } catch (err) {
            console.log(err)
            res.status(418).send(err)
        }
    });
});

//front-end requesting historical data for one miner
app.get("/graph", (req, res) => {
    authenticateThenDo(req, res, async () => {
        const minerId = req.query?.id;
        if(minerId) {
            try {
                const data = await getHistoricalData(minerId)
                res.send(data)
            } catch (err) {
                console.log(err)
                res.status(500).send(err)
            }
        }
        else {
            res.status(500).send({ error: 'No id(ea) provided' })
        }
    })
});

//front-end requesting historical data for one miner
app.get("/CO2", (req, res) => {
    authenticateThenDo(req, res, async () => {
        const minerId = req.query?.id;
        if(minerId) {
            try {
                const data = await getHistoricalData(minerId, ["CO2", "TVOC"])
                res.send(data)
            } catch (err) {
                console.log(err)
                res.status(500).send(err)
            }
        }
        else {
            res.status(500).send({ error: 'No id(ea) provided' })
        }
    })
});

//front-end requesting historical data for one miner
app.get("/Pressure", (req, res) => {
    authenticateThenDo(req, res, async () => {
        const minerId = req.query?.id;
        if(minerId) {
            try {
                const data = await getHistoricalData(minerId, ["Pressure"])
                res.send(data)
            } catch (err) {
                console.log(err)
                res.status(500).send(err)
            }
        }
        else {
            res.status(500).send({ error: 'No id(ea) provided' })
        }
    })
});
//front-end requesting historical data for one miner
app.get("/Temperature", (req, res) => {
    authenticateThenDo(req, res, async () => {
        const minerId = req.query?.id;
        if(minerId) {
            try {
                const data = await getHistoricalData(minerId, ["Temperature"])
                res.send(data)
            } catch (err) {
                console.log(err)
                res.status(500).send(err)
            }
        }
        else {
            res.status(500).send({ error: 'No id(ea) provided' })
        }
    })
});
app.get("/Humidity", (req, res) => {
    authenticateThenDo(req, res, async () => {
        const minerId = req.query?.id;
        if(minerId) {
            try {
                const data = await getHistoricalData(minerId, ["Humidity"])
                res.send(data)
            } catch (err) {
                console.log(err)
                res.status(500).send(err)
            }
        }
        else {
            res.status(500).send({ error: 'No id(ea) provided' })
        }
    })
});

//front-end updating sampling frequency
//need to send it down to each pi
app.post('/freq', (req, res)=>{
    authenticateThenDo(req, res, () => {
        publish('sensor/instructions/sampling', req.body.global);
        res.send('OK');
    })
});

// Handles any other routes
app.use((req, res, next) => {
    res.status(404).send({ name: "NotFound", message: "This endpoint does not exist"})
})

/// If the request contains a valid token, process the request defined in function, else return an error
function authenticateThenDo(req, res, fun) {
    let token = req.query.token;
    console.log(token)
    jwt.verify(token, privateKey, (err, decoded) => {
        if(!err) {
            if(decoded.token === 'poggers') {
                fun();
            }
            else{
                console.log(JSON.stringify(decoded))
                res.status(401).send({ name: "TokenError", message: "Invalid Token"})
            }
        }
        else {
            console.log('Failed verification')
	        res.status(401).send(err);
        }
    })
}
//------- HTTP done, MQTT from here

const mqtt=require('mqtt');
const { setDatasets } = require("react-chartjs-2/dist/utils");

const clientOptions = {
    clientID: "mqttjs01",
    username: "webapp",
    password: "=ZCJ=4uzfZZZ#36f",

    key: fs.readFileSync('../AWS/cert/webapp.key'), // MAKE SURE THE FILEPATH IS CORRECT
    cert: fs.readFileSync('../AWS/cert/webapp.crt'),
    ca: [ fs.readFileSync('../AWS/cert/ca.crt') ]
}
var MQTTclient = mqtt.connect('mqtts://thecanary.duckdns.org', clientOptions);

// Runs on connection to the broker
MQTTclient.on("connect", () => {
	console.log("connected " + MQTTclient.connected);
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
MQTTclient.on('message', (topic, message, packet) => {
	if (topic === "sensor/data") {
        let msg = JSON.parse(message.toString())
        console.log(msg);
        addNewData(msg.id, msg.data);
	}
})

const pubOptions={
	retain:false,
	qos:1
};

// You can call this function to publish to things
function publish(topic,msg,options=pubOptions){
	console.log("publishing",msg);
	if (MQTTclient.connected == true){
		MQTTclient.publish(topic,msg.toString(),options);
	}
}

// Helper functions

//gets the current miner data from the database and returns them in an array
async function getMiners() {
    let result = await db.collection(currDataColl).find({}, { projection: { _id: 0, id: 1, data: 1 } }).toArray()
    return result;
}

async function getHistoricalData(id, keyArray) {
    var query = {id: id};
    let x = [];
    let data = {}
    keyArray.map((key) => {
        data[key] = [];
    })
    let result = await db.collection(oldDataColl).find(query, { projection: { _id: 0, data: 1, time:1 }}).toArray()
    result.map((elem) => {
        keyArray.map((key) => {
            data[key].push(elem.data[key]);
        })
        x.push(elem.time.getTime());
    })
    return {x: x, data: data}
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
            //console.log(obj.result.n + " document(s) deleted");
            db.collection(currDataColl).insertOne({id:id, data:data,time: new Date()}, function(err, res) {
                if (err){
                    console.log(err);
                    throw err;
                }
            }); 
        }
    });
    db.collection(oldDataColl).insertOne({id:id, data:data,time: new Date()}, function(err, res) {
        if (err){
            console.log(err);
            throw err;
        }
    });
}

// Handles shutting down application on critical errors
process.on('SIGTERM', () => {
	httpsServer.close(() => {
		console.log('HTTPS server terminated');
	});
	MQTTclient.end(() => {
		console.log('MQTT client disconnected');
	});
	DBClient.close(() => {
		console.log("Disconnected from MongoDB");
	});
})