//from MUI
import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import IconButton from '@mui/material/IconButton';
import Typography from '@mui/material/Typography';
import Menu from '@mui/material/Menu';
import MenuIcon from '@mui/icons-material/Menu';
import Container from '@mui/material/Container';
import SettingsIcon from '@mui/icons-material/Settings';
import Button from '@mui/material/Button';
import Tooltip from '@mui/material/Tooltip';
import MenuItem from '@mui/material/MenuItem';
import BasicSelect from './samplingSettings';
import { styled , alpha} from '@mui/material/styles';
import PropTypes from 'prop-types';
import { Card, CardMedia } from '@mui/material';
import { Avatar } from '@mui/material';
import axios from 'axios';

const pages = [];


const StyledMenu = styled((props) => (
  <Menu
    elevation={0}
    anchorOrigin={{
      vertical: 'bottom',
      horizontal: 'right',
    }}
    transformOrigin={{
      vertical: 'top',
      horizontal: 'right',
    }}
    {...props}
  />
))(({ theme }) => ({
  '& .MuiPaper-root': {
    borderRadius: 6,
    marginTop: theme.spacing(1),
    minWidth: 180,
    color:
      theme.palette.primary.main,
    backgroundColor: theme.palette.backgroundLight.main,
    boxShadow:
      'rgb(255, 255, 255) 0px 0px 0px 0px, rgba(0, 0, 0, 0.05) 0px 0px 0px 1px, rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px',
    '& .MuiMenu-list': {
      padding: '4px 0',
    },
    
    '& .MuiMenuItem-root': {
      '& .MuiSvgIcon-root': {
        fontSize: 18,
        color: theme.palette.text.secondary,
        marginRight: theme.spacing(1.5),
      },
      '&:active': {
        backgroundColor: alpha(
          theme.palette.primary.main,
          theme.palette.action.selectedOpacity,
        ),
      },
      '.&MuiAvatar-root': {
        backgroundColor: "red"
      }
    },
  },
}));


const ResponsiveAppBar = ({setToken}) => {
  const [anchorElNav, setAnchorElNav] = React.useState(null);
  const [anchorElUser, setAnchorElUser] = React.useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };
  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const handleCloseUserMenu = () => {
    setAnchorElUser(null);
  };

  const archive = () => {
    axios.get(process.env.REACT_APP_DOMAIN + '/archive', { params: { token: sessionStorage.getItem('token')} })
    .then(res => {})
    .catch(err => {
      console.log(err);
    },)
    handleCloseUserMenu();
  };

  const logout = () => {
    setToken(undefined);
  }
  return (
    <AppBar style = {{background: '#434341'}} position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ mr: 2, display: { xs: 'none', md: 'flex' }, color: 'white' }}
          >
            <CardMedia
                component="img"
                height="65"
                image={require("./../img/logo2.png")}
                alt="logo"
                />
          </Typography>

          <Box sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon  color ="secondary"/>
            </IconButton>
            <Box sx={{ background: '#272A31',flexGrow: 0, display: { xs: 'none', md: 'flex' } }}>
            <StyledMenu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: 'bottom',
                horizontal: 'left',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'left',
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
              sx={{
                display: { xs: 'block', md: 'none' },
              }}
            >
              {pages.map((page) => (
                <MenuItem key={page} onClick={handleCloseNavMenu} selected>
                  <Typography textAlign="center">{page}  </Typography>
                </MenuItem>
              ))}
              
              
            </StyledMenu>
            </Box>
          </Box>
          <Typography
            variant="h6"
            noWrap
            component="div"
            color="white"
            sx={{ flexGrow: 1, display: { xs: 'flex', md: 'none' } }}
          >
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
            {pages.map((page) => (
              <Button
                key={page}
                onClick={handleCloseNavMenu}
                sx={{ my: 2, color: 'white', display: 'block' }}
              >
                {page}
              </Button>
            ))}
          </Box>

          <Box sx={{ flexGrow: 0 }}>
            <Tooltip title="Open settings">
              
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar>
                  <SettingsIcon sx={{ color: 'white' }} alt="Settings" color='white' />
                </Avatar>
              </IconButton>
              
            </Tooltip>
            <StyledMenu
              sx={{ mt: '45px', color:"black" }}
              id="menu-appbar"
              anchorEl={anchorElUser}
              anchorOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              keepMounted
              transformOrigin={{
                vertical: 'top',
                horizontal: 'right',
              }}
              open={Boolean(anchorElUser)}
              onClose={handleCloseUserMenu}
            >
                <MenuItem key="BasicSelect">
                  <BasicSelect/>
                </MenuItem>
                <MenuItem key="archive" onClick = {archive}>
                  Archive data
                </MenuItem>
                <MenuItem key="logout" onClick = {logout}>
                  Logout 
                </MenuItem>
            </StyledMenu>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
ResponsiveAppBar.propTypes = {
  setToken: PropTypes.func.isRequired
}
export default ResponsiveAppBar;
