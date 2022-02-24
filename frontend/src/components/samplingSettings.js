import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import axios from 'axios';
import { alpha, styled } from '@mui/material/styles';
import {theme} from './../App';
import InputBase from '@mui/material/InputBase';

let freqs = [10,20,30,40];

const StyledSelect = styled(({ className, ...props }) => (
  <Select {...props} MenuProps={{ classes: { paper: className } }} />
))
(({ theme }) => ({
    color: theme.palette.secondary.main,
    backgroundColor: theme.palette.backgroundLight.main,
    
}));

const StyledInput = styled(InputBase)(({ theme }) => ({
  'label + &': {
    marginTop: theme.spacing(0),
  },
  '& .MuiInputBase-input': {
    borderRadius: 4,
    color: theme.palette.secondary.main,
    position: 'relative',
    border: '1px solid',
    borderColor: theme.palette.primary.main,
    fontSize: 15,
    padding: '10px 26px 10px 12px',
  },
}));

export default function BasicSelect() {
  const [freq, setFreq] = React.useState('');

  const handleChange = (event) => {
    const oldfreq = freq;
    setFreq(event.target.value);
    //send post request to backend
    axios.post(process.env.REACT_APP_DOMAIN + '/freq', {global: event.target.value},{params:{token: sessionStorage.getItem('token')}})
        .then(response => console.log("updated successfully"))
        .catch(err => {
            setFreq(oldfreq);
            alert("there was an error" + err);
        });
  };

  const inputProps = {
    color: "red",
  }

  return (
    <Box sx={{ minWidth: 180 }}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label" sx={{color: theme.palette.primary.main, backgroundColor: theme.palette.backgroundLight.main}}>Sampling frequency</InputLabel>
        <StyledSelect
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={freq}
          label="Sampling frequency"
          onChange={handleChange}
          sx={{borderColor: "red"}}
          input={<StyledInput />}


        >
          {freqs.map((f) => (
              <MenuItem value={f} key={f}>{f}</MenuItem>
          ))}
        </StyledSelect>
      </FormControl>
    </Box>
  );
}