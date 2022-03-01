import React from 'react';
import "./Login.css"
import PropTypes from 'prop-types';
import TextField from '@mui/material/TextField';
import { alpha, styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import axios from 'axios';
import Card from '@mui/material/Card'
import { CardMedia } from '@mui/material';


   const RedditTextField = styled(TextField)(({theme}) => ({
    "& .MuiInputBase-root": {
        color: theme.palette.secondary.main,
        height: '5%',
        backgroundColor: '#434341',
        marginTop: '5%',
        marginBottom: '5%'
      },
    "& .MuiFormLabel-root": {
        color: theme.palette.secondary.main //initial input label color
    },
    '& label.Mui-focused': {
      color: theme.palette.secondary.main,
    },
    '& .MuiOutlinedInput-root': {
      '& fieldset': {
        borderColor: theme.palette.secondary.main,
        
      },
      '&:hover fieldset': {
        borderColor: theme.palette.primary.main,
      },
      '&.Mui-focused fieldset': {
        borderColor: theme.palette.primary.main,
        
      },
    },
  }));

  const ColorButton = styled(Button)(({ theme }) => ({
    color: '#434341',
    backgroundColor: theme.palette.secondary.main,
    '&:hover': {
      backgroundColor:theme.palette.primary.main,
    },
  }));

async function loginUser(credentials) {
  return axios.post(process.env.REACT_APP_DOMAIN + '/login', credentials)
    .then(res => {
      console.log(res.data);
      return res.data.token;
    })
    .catch(err => {
      console.log(err);
    })
  }

export default function Login({ setToken }) {
  const [username, setUserName] = React.useState();
  const [password, setPassword] = React.useState();
  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      username,
      password
    });
    setToken(token);
  }

  return(
    <div style={{width: '100%', flexDirection: 'column', flexWrap: "wrap",   display: 'flex',
    alignItems: 'center'}}>
    <Card>
    <CardMedia
        component="img"
        width= "80%"
        image={require("./../img/logo.png")}
        alt="logo"/>
    </Card>
    <div style={{width: '20%', flexDirection: 'column', flexWrap: "wrap",   display: 'flex',
    alignItems: 'center'}}>

    <form onSubmit={handleSubmit}>
        <RedditTextField id="username" label="Username" onChange={e => setUserName(e.target.value)} />
        
        <RedditTextField
            id="password"
            label="Password"
            type="password"
            onChange={e => setPassword(e.target.value)} />

      <div>
        <ColorButton type="submit">Submit</ColorButton>
      </div>
    </form>
    </div>
    </div>

  )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
  }