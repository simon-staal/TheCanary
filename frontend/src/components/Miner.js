import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import { CardActionArea } from '@mui/material';
import Box from '@mui/material/Box';

export default function Miner(props) {
  return (
    <Card sx={{ display: 'flex', width: "auto",justifyContent: 'center', alignItems: 'center'}}>
      <Box sx={{ display: 'flex', flexDirection: 'column' }}>
      <CardMedia
            component="img"
            width="100%"
            image={require("./../img/miner.png")}
            alt="miner"
        />
      </Box>
      
        <CardContent sx={{ flex: '1 0 auto' }}>
          <Typography component="div" variant="h5">
            {props.id}
          </Typography>
            {props.data.map((elem)=>{
                return (
                    <Typography color="text.secondary" component="div" aligh="left" key={elem}>
                        {elem}
                    </Typography>)
            })}

        </CardContent>
    </Card>
  );
}
