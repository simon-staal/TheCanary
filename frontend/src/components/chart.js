import React from 'react';
import {Chart as ChartJS,CategoryScale,  LinearScale, PointElement, LineElement, Title, Tooltip, Legend, TimeScale} from 'chart.js';
import { Line } from 'react-chartjs-2';
import axios from 'axios';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale,
  );

  export var options = {
    responsive: true,
    plugins: {
      legend: {
        labels: {
          color: 'white',
        },        
        position: 'top',
      },
      title: {
        color: 'white',
        display: true,
        text: "",
        font: {size: 18}
      },
    },
    scales: {
      y: {
        ticks: {
          color: "white",
          font: {
            size: 14,
          },
        },
        title: {
          color: 'white',
          display: true,
          text: 'Name Y',
          font: {
            size: 14,
          }
        }
      },
      xAxes: [{
        type: 'time',
        time: {
          unit: 'minute',
          displayFormats: {
            millisecond: 'MMM DD',
            second: 'MMM DD',
            minute: 'MMM DD',
            hour: 'MMM DD',
            day: 'MMM DD',
            week: 'MMM DD',
            month: 'MMM DD',
            quarter: 'MMM DD',
            year: 'MMM DD',
          }
        },
        ticks: {
          color: "white",
          font: {
            size: 14
          },
        },
        title: {
          color: "white",
          display: true,
          text: 'Name X',
          font: {
            size: 14,
          }
        }
      }],
    },
  };
  
  
  export default function CustomChart(props) {
    const [xVal, setXVal] = React.useState([]);
    const [yVal, setYVal] = React.useState([]);
    let data = {
      labels: xVal,
      datasets: [
        {
          label: props.chartdata.label,
          data: yVal,
          borderColor: props.chartdata.color,
          backgroundColor: props.chartdata.color,
        },
      ],
    };
    options.plugins.title.text=props.chartdata.label;

    React.useEffect(() => {
      axios.get(process.env.REACT_APP_DOMAIN + props.chartdata.route, { params: { id: props.id, token: sessionStorage.getItem('token')} })
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