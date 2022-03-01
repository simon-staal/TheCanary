import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import ButtonBase from '@mui/material/ButtonBase';
import Modal from '@mui/material/Modal';
import ChartGrid  from './chartGrid';
import { Button } from '@mui/material';
import { alpha, styled } from '@mui/material/styles';
import MinerTable from './table';



const style = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: '70%',
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
  display:"flex",
  justifyContent:"center",
  flexDirection:"column",
  textAlign: "center",
  backgroundColor: '#313131',
};


export default function Miner(props) {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);
  return (
    <Card sx={{ display: 'flex', width: "auto",justifyContent: 'center', alignItems: 'center', backgroundColor: '#313131'}}>
      <ButtonBase variant = "contained" sx={{ width: '100%'}} onClick={handleOpen}>
      <Box sx={{ display: 'flex'}}>
      <CardMedia
            component="img"
            width="100%"
            image={require("./../img/miner.png")}
            alt="miner"
        />
      </Box>
      
        <CardContent sx={{ flex: '1 0 auto' }}>
          <Typography component="div" variant="h5" color="primary">
            Team {props.id}
          </Typography>
              <MinerTable minerData={props.data} unit={props.units}/>


        </CardContent>
        </ButtonBase>
        <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
            <Typography id="modal-modal-title" variant="h5" component="h2" color="primary">
              Team {props.id}
            </Typography>
          <ChartGrid id = {props.id}/>
        </Box>
      </Modal>
    </Card>
  );
}
