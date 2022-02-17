import './App.css';
import ResponsiveAppBar from './components/appBar';
import Miners from './components/MinerGrid';
import * as React from 'react';
import axios from 'axios'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import useToken from './components/useToken';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    primary: {
      main: '#FEEE4D',
    },
    secondary: {
      main: '#FFFAC8',
      background: '#313131',
    },
    backgroundDark: {
      main: '#121212',
    },
    backgroundLight: {
      main: '#313131',
    },
  }
});

function App() {
  const [miners, setMiners] = React.useState([]);
  const {token, setToken} = useToken();

  React.useEffect(() => {
      console.log(process.env.REACT_APP_DOMAIN);
      axios.get(process.env.REACT_APP_DOMAIN + '/miners')
        .then(res => {
          setMiners(res.data);
        })
        .catch(err => {
          console.log(err);
        },)
    }, []); //error handling
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

  if(!token) {
    return (
      <ThemeProvider theme = {theme}>
      <div className="App">
        <header className="App-header">
          <Login setToken={setToken} />
        </header>
      </div>
      </ThemeProvider>
    );
  }
  return (
    <ThemeProvider theme={theme}>
    <div className="App">
      <header className="App-header">
      <ResponsiveAppBar/>
        <Miners  miners = {miners} xs ={xs}/>
      </header>
    </div>
    </ThemeProvider>
  );
}

export default App;
