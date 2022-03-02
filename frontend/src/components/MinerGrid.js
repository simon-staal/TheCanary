import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import Grid from '@mui/material/Grid';
import Miner from './Miner.js'
import { experimentalStyled as styled } from '@mui/material/styles';
import Box from '@mui/material/Box';
import Paper from '@mui/material/Paper';
import axios from 'axios'



const Item = styled(Paper)(({ theme }) => ({
    ...theme.typography.body2,
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  }));

export default function Miners() {
    const [miners, setMiners] = React.useState({data:[], units:[]});
    let xs = 2
    if(miners.data.length==1){
        xs = 12;
    }
    else if(miners.data.length<=4){
      xs = 6;
    }
    else if(miners.data.length<=8){
      xs = 3;
    }
    else if(miners.data.length<=12){
      xs = 2;
    }
    else {
      xs = 1;
    }
    function getNewData() {
      axios.get(process.env.REACT_APP_DOMAIN + '/miners', {params: {token: sessionStorage.getItem('token')}})
          .then(res => {
            console.log(res.data);
            setMiners(res.data);
            
          })
          .catch(err => {
            console.log(err);
          },)
    }
    React.useEffect(() => {
        console.log(process.env.REACT_APP_DOMAIN);
        getNewData();
        const interval = setInterval(() => {
          getNewData();
        }, 200);
      
        return () => clearInterval(interval);
      }, []); //error handling
    return(
        <Box sx={{paddingTop: "1%", paddingBottom: "1%", paddingLeft:"1%", paddingRight:"1%", flexGrow: 1 }}>
        <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: xs, sm: 8, md: 12 }}>
        {miners.data.map((miner) => (
            <Grid item xs={xs}  key={miner.id}>
                <Miner id={miner.id} data={miner.data} units={miners.units}/>
            </Grid>
        ))}
        </Grid>
        </Box>


    );
}