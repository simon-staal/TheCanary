import * as React from 'react';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import ButtonBase from '@mui/material/ButtonBase';
import Modal from '@mui/material/Modal';
import ChartGrid  from './chartGrid';
import { alpha, styled } from '@mui/material/styles';
import MinerTable from './table';
import CloseIcon from '@mui/icons-material/Close';
import { Icon } from '@mui/material';
import { Avatar } from '@mui/material';
import { IconButton } from '@mui/material';
import axios from 'axios';


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

const StyledAvatar = styled(Avatar)(({theme})=>({
  '&.MuiAvatar-root':{
    backgroundColor: theme.palette.primary.main,
  }
}));

const StyledCloseIcon = styled(CloseIcon)(({theme})=>({
    '&&&': {
      color: theme.palette.backgroundLight.main,
    },
}));



export default function Miner(props) {
  const [open, setOpen] = React.useState(false);
  const handleOpen = () => setOpen(true);
  const handleClose = () => setOpen(false);

  function removeMiner(e){
    e.stopPropagation();
    axios.get(process.env.REACT_APP_DOMAIN + '/deleteMiner', {params: {token: sessionStorage.getItem('token'), id: props.id}})
          .then(res => {            
          })
          .catch(err => {
            console.log(err);
          },)
  }
  return (
    <Card sx={{ display: 'flex', width: "auto",justifyContent: 'center', alignItems: 'center', backgroundColor: '#313131'}}>
      <ButtonBase variant = "contained" sx={{ width: '100%'}} onClick={handleOpen}>
      <Box sx={{ display: 'flex'}}>
      <CardMedia
            component="img"
            image={require("./../img/miner.png")}
            alt="miner"
        />
      </Box>
      
        <CardContent sx={{ flex: '1 0 auto' }}>
          <Box sx={{width: '100%', display: 'flex', flexDirection: 'row', justifyContent: 'space-between'}}>
            <div></div>
            <Typography sx={{alignSelf: 'center'}} component="div" variant="h5" color="primary">
              Team {props.id}
            </Typography>
            <IconButton onClick={removeMiner}>
            <StyledAvatar sx={{width: '30px', height: "30px", alignSelf: "right"}}>
              <StyledCloseIcon/>
            </StyledAvatar>
            </IconButton>
          </Box>
          
          <MinerTable minerData={props.data} units={props.units}/>


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
