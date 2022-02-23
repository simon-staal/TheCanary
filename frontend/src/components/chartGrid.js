import * as React from 'react';
import Box from '@mui/material/Box'

import Grid from '@mui/material/Grid';
import CustomChart from './chart'


export default function chartGrid (props){
    const chartInfos = 
    [
    {color: 'yellow', label: 'Air pressure', route: '/graph'},
    {color: 'red', label: 'CO2', route: '/graph'},
    {color: 'green', label: 'Temperature', route: '/graph'},
    {color: 'blue', label: 'Humidity', route: '/graph'}
    ]
    return (
        <Box>
        <Grid container spacing={{ xs: 2, md: 3 }} columns={{ xs: 4, sm: 8, md: 12 }}>
            <Grid item xs={6} key={chartInfos[0].label}>
                    <CustomChart id={props.id} chartdata={chartInfos[0]}/>
            </Grid>
            <Grid item xs={6} key={chartInfos[1].label}>
                    <CustomChart id={props.id} chartdata={chartInfos[1]}/>
            </Grid>
            <Grid item xs={6} key={chartInfos[2].label}>
                    <CustomChart id={props.id} chartdata={chartInfos[2]}/>
            </Grid>
            <Grid item xs={6} key={chartInfos[3].label}>
                    <CustomChart id={props.id} chartdata={chartInfos[3]}/>
            </Grid>
        </Grid>
        </Box>
    )
}