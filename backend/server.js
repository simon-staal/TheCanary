const express = require("express");
const path = require("path");
const cors = require('cors');

const PORT = process.env.PORT || 8000;

const app = express();

app.use(express.static(path.resolve(__dirname, '../client/build')));

app.use(express.json());

app.use(express.urlencoded({ extended: true })) ;

app.use(cors());

app.get("/miners", (req, res) => {
    const miners = [{id: "Team 1", data: ["sensor data", "air pressure"]}, {id:"Team 2", data: ["sensor data"]},
    {id:"Team 3", data: ["sensor data"]},{id:"Team 4", data: ["sensor data"]}];
    res.send( miners);
  });

app.get("/graph", (req, res) => {
    const data = {y: [4,2,2,3,7,8,5], x: ["Jan", "Febr", "Mar", "Apr", "May", "June", "July"]};
    res.send( data);
    //get data from database
});

app.listen(PORT, () => {
    console.log("Browser server listening on " + PORT);
});

app.use('/login', (req, res) => {
    res.send({
      token: 'test123'
    });
  });

app.post('/freq', (req, res)=>{
    res.send('OK');
});



//------- HTTP done, MQTT from here

const mqtt=require('mqtt');

const client = mqtt.connect("mqtt://localhost",{clientId:"backend"});

client.on("connect",function(){	
    console.log("connected");
})

client.on('message', (topic, message, packet) => {
    //get measurements
    //don't really care about topic
    //message is JSON object -> check if type is correct
    let msg = "";
    try{
        msg = JSON.parse(message);
    } catch (err) {
        console.error("Bad message", err);
    }
    if(msg!=""){
        //save it in database
    }
});

