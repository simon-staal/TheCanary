const express = require("express");
const path = require("path");
var cors = require('cors');

const PORT = process.env.PORT || 8000;

const app = express();

app.use(express.static(path.resolve(__dirname, '../client/build')));

app.use(express.json());

app.use(express.urlencoded({ extended: true })) ;

app.use(cors());

app.get("/miners", (req, res) => {
    const miners = [{id: "Team 1", data: ["sensor data", "air pressure"]}, {id:"Team 2", data: ["sensor data"]},
    {id:"Team 3", data: ["sensor data"]}];
    res.send( miners);
  });

app.listen(PORT, () => {
    console.log("Browser server listening on " + PORT);
});

var mqtt=require('mqtt');

var client = mqtt.connect("mqtt://localhost",{clientId:"backend"});

client.on("connect",function(){	
    console.log("connected");
})

/*client.on('message', (topic, message, packet) => {

});*/

