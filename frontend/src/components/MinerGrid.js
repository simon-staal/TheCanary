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



const Item = styled(Paper)(({ theme }) => ({
    ...theme.typography.body2,
    padding: theme.spacing(2),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  }));

export default function Miners(props) {
    return(
        <Box sx={{paddingTop: "1%", flexGrow: 1 }}>
        <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: props.xs, sm: 8, md: 12 }}>
        {props.miners.map((miner) => (
            <Grid item xs={props.xs}  key={miner.id}>
                <Miner id={miner.id} data={miner.data}/>
            </Grid>
        ))}
        </Grid>
        </Box>


    );
}