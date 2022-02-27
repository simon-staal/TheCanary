import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell , { tableCellClasses } from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { styled } from '@mui/material';

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    [`&.${tableCellClasses.body}`]: {
      fontSize: 14,
      color: theme.palette.secondary.main,
    },
  }));

const StyledTableRow = styled(TableRow)(({ theme }) => ({
    '&:nth-of-type(odd)': {
      backgroundColor: theme.palette.tablebackground.odd,
    },
    '&:nth-of-type(even)': {
        backgroundColor: theme.palette.tablebackground.even,
      },
    // hide last border
    '&:last-child td, &:last-child th': {
      border: 0,
    },
    
  }));


export default function MinerTable(props) {
    return(
        <TableContainer sx={{backgroundColor:'rgba(52, 52, 52, 0.8)'}}component={Paper}>
        <Table 
            size='medium'
            sx=
                {{ minWidth: 200, [`& .${tableCellClasses.root}`]: {borderBottom: "none", backgroundColor:'rgba(52, 52, 52, 0.8)'}
  }} aria-label="simple table">
          <TableBody>
            {Object.keys(props.minerData).map((key, index) => (
              <StyledTableRow
                key={key}
                sx={{ '&:last-child td, &:last-child th': { border: 0 }}}
              >
                <StyledTableCell component="th" scope="row">
                  {key}
                </StyledTableCell>
                <StyledTableCell align="right">{props.minerData[key].toFixed(3)} {props.units[key]}</StyledTableCell>
              </StyledTableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    );
}