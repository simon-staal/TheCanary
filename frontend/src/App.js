import './App.css';
import ResponsiveAppBar from './components/appBar';
import Miners from './components/MinerGrid';
import * as React from 'react';
import axios from 'axios'
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './components/Login';
import useToken from './components/useToken';
import { createTheme, ThemeProvider } from '@mui/material/styles';


export const theme = createTheme({
  palette: {
    primary: {
      main: '#FEEE4D',
      light: '#FEEE4D',
      dark: '#FEEE4D',
    },
    secondary: {
      main: '#FFFAC8',
      background: '#313131',
      light: '#FEEE4D',
      dark: '#FEEE4D',

    },
    backgroundDark: {
      main: '#121212',
    },
    backgroundLight: {
      main: '#313131',
    },
  },
  overrides: {
    MuiMenuItem: {
      root: {
        '&$selected': {
          backgroundColor: `#121212`,
        },
      },
    },
    
  },
});

function App() {
  const {token, setToken} = useToken();
  React.useEffect(() => {
    document.title = "The Canary"
  }, [])
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
        <Miners/>
      </header>
    </div>
    </ThemeProvider>
  );
}

export default App;
