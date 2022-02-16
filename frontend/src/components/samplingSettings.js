import * as React from 'react';
import Box from '@mui/material/Box';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
import axios from 'axios';

let freqs = [10,20,30,40];

export default function BasicSelect() {
  const [freq, setFreq] = React.useState('');

  const handleChange = (event) => {
    const oldfreq = freq;
    setFreq(event.target.value);
    //send post request to backend
    axios.post(process.env.REACT_APP_DOMAIN + '/freq', {global: event.target.value})
        .then(response => console.log("updated successfully"))
        .catch(err => {
            setFreq(oldfreq);
            alert("there was an error" + err);
        });
  };

  return (
    <Box sx={{ minWidth: 180 }}>
      <FormControl fullWidth>
        <InputLabel id="demo-simple-select-label">Sampling frequency</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={freq}
          label="Sampling frequency"
          onChange={handleChange}
        >
          {freqs.map((f) => (
              <MenuItem value={f} >{f}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}