import React from 'react';
import {Chart as ChartJS,TimeScale,  LinearScale, PointElement, LineElement, Title, Tooltip, Legend} from 'chart.js';
import { Line } from 'react-chartjs-2';
import "chartjs-adapter-moment";
import axios from 'axios';

ChartJS.register(
    TimeScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
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
      x: {
        type: 'time',
        time: {
        	unit: 'minute',
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
          text: 'Time',
          font: {
            size: 14,
          }
        }
      },
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
          setYVal(res.data.data);
          data.labels=res.data.x;
          Object.keys(res.data.data).map((key, index)=>{
            data.datasets[index].data= res.data.data[key]
          })
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
