import React from 'react';
import "./Login.css"
import PropTypes from 'prop-types';
import TextField from '@mui/material/TextField';
import { alpha, styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import axios from 'axios';

async function loginUser(credentials) {
    console.log(credentials);
    console.log(JSON.stringify(credentials));

    axios.post(process.env.REACT_APP_DOMAIN + '/login', credentials)
    .then(response => {console.log(response); return response.data.token;})
    .catch(err => {
        alert("there was an error" + err);
    });
}

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

export default function Login({ setToken }) {
  const [username, setUserName] = React.useState();
  const [password, setPassword] = React.useState();
  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      username: username,
      password: password
    });
    setToken(token);
  }

  return(
    <div style={{width: '20%', flexDirection: 'column', flexWrap: "wrap",   display: 'flex',
    alignItems: 'center'}}>
    <Typography variant="h3" color="primary">
        The Canary
    </Typography>
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

  )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
  }