const express = require("express");
const path = require("path");
const cors = require('cors');
const jwt = require('jsonwebtoken');
const fs = require('fs');

const PORT = process.env.PORT || 8000;

const app = express();

app.use(express.static(path.resolve(__dirname, '../client/build')));

app.use(express.json());

app.use(express.urlencoded({ extended: true })) ;

app.use(cors());

const privateKey = fs.readFileSync('../../AWS/cert/webapp.key')

// Can be accessed without authentication
app.get('/', (req, res) => {
    res.send("Welcome to our API!")
})

app.post('/login', (req, res) => {
    console.log(req.body);
    if (req.body.username === 'admin' && req.body.password === "password") {
        let token = jwt.sign({ token: 'poggers'}, privateKey);
        res.send(token);
    }
    else {
        res.status(418).send("I CAN'T BREW COFFEE");
    }
})

// Can't be accessed without authentication
app.get('/api', (req, res) => {
    let token = req.query.token;
    jwt.verify(token, privateKey, (err, decoded) => {
        if(!err) {
            if(decoded.token === 'poggers') {
                res.send('You are authenticated');
            }
            console.log(JSON.stringify(decoded))
            res.status(401).send({ name: "TokenError", message: "Invalid Token"})
        }
        else {
	    res.status(401).send(err);
        }
    })
})

app.listen('13337')
