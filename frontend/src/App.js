import logo from './logo.svg';
import './App.css';
import ResponsiveAppBar from './components/appBar';
import Miner from './components/Miner';
import Miners from './components/MinerGrid';
import * as React from 'react';
import axios from 'axios'


function App() {
  const [miners, setMiners] = React.useState([]);
  React.useEffect(() => {
      axios.get('http://localhost:8000/miners')
        .then(res => {
          setMiners(res.data);
        })
        .catch(err => {
          console.log(err);
        })
    }); //error handling
  let miners2 = [{id: "Team 1", data: ["sensor data", "air pressure"]}, {id:"Team 2", data: ["sensor data"]},
  {id:"Team 3", data: ["sensor data"]}
];
  let xs = 2
  if(miners.length<=4){
    xs = 6;
  }
  else if(miners.length<=8){
    xs = 3;
  }
  else if(miners.length<=12){
    xs = 2;
  }
  else {
    xs = 1;
  }
  return (
    <div className="App">
      <header className="App-header">
      <ResponsiveAppBar/>
        <Miners  miners = {miners} xs ={xs}/>
      </header>
    </div>
  );
}

export default App;
