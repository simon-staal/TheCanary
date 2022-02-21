import React from 'react';
import {Chart as ChartJS,CategoryScale,  LinearScale, PointElement, LineElement, Title, Tooltip, Legend,} from 'chart.js';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
  );

  export const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: 'My chart',
        font: {size: 18}
      },
    },
    scales: {
      y: {
        ticks: {
          color: "grey",
          font: {
            size: 14,
          },
        },
        title: {
          display: true,
          text: 'Name Y',
          font: {
            size: 14,
          }
        }
      },
      x: {
        ticks: {
          color: "grey",
          font: {
            size: 14
          },
        },
        title: {
          display: true,
          text: 'Name X',
          font: {
            size: 14,
          }
        }
      },
    },
  };
  
  
  export default function CustomChart() {
    const [xVal, setXVal] = React.useState([]);
    const [yVal, setYVal] = React.useState([]);
    let data = {
      labels: xVal,
      datasets: [
        {
          label: 'MinerData',
          data: yVal,
          borderColor: 'yellow',
          backgroundColor: 'yellow',
        },
      ],
    };

    React.useEffect(() => {
      axios.get(process.env.REACT_APP_DOMAIN + '/graph')
        .then(res => {
          setXVal(res.data.x);
          setYVal(res.data.y);
          data.labels=res.data.x;
          data.datasets[0].data=res.data.y;
        })
        .catch(err => {
          console.log(err);
        },)
    }, []); 



    return (
      <div>
        <Line options={options} data={data} />
      </div>
    );
  }