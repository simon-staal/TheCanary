import React from 'react';
import "./Login.css"
import PropTypes from 'prop-types';
import TextField from '@mui/material/TextField';

async function loginUser(credentials) {
    return fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(credentials)
    })
      .then(data => data.json())
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
    <form onSubmit={handleSubmit}>
      <label>
        <TextField id="username" label="Username" variant="outlined" onChange={e => setUserName(e.target.value)} />
      </label>
      <label>
        <p>Password</p>
        <TextField if="password" label="Password" variant="outlined" onChange={e => setPassword(e.target.value)} />
      </label>
      <div>
        <button type="submit">Submit</button>
      </div>
    </form>
  )
}

Login.propTypes = {
    setToken: PropTypes.func.isRequired
  }