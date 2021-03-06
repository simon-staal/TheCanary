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

  
  
  export default function CustomChart(props) {
    var defaultOptions = {
      responsive: true,
      stacked: false,
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
          },
          type: 'linear',
          display: true,
          position: 'left',
        },
        y1: {
          ticks: {
            color: "white",
            font: {
              size: 14,
            },
          },
          title: {
            color: 'white',
            display: true,
            text: 'Name Y1',
            font: {
              size: 14,
            }
          },
          type: 'linear',
          display: false,
          position: 'right',
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
    
    const [xVal, setXVal] = React.useState([]);
    const [Ydata, setYdata] = React.useState([]);
    const [options, setOptions] = React.useState(defaultOptions)

    let data = {
      labels: xVal,
      datasets: Ydata,
      // grid line settings
      grid: {
        drawOnChartArea: false, // only want the grid lines for one axis to show up
      },
    };
    options.plugins.title.text=props.chartdata.label;
    function getNewData () {
      axios.get(process.env.REACT_APP_DOMAIN + props.chartdata.route, { params: { id: props.id, token: sessionStorage.getItem('token')} })
      .then(res => {
        setXVal(res.data.x);
        data.labels=res.data.x;
        let Ydata = [];
        let yIds = ['y', 'y1'];
        Object.keys(res.data.data).map((key, index)=>{
          let dataset = {
            label: props.chartdata.label[index],
            data: res.data.data[key],
            borderColor: props.chartdata.color[index],
            backgroundColor: props.chartdata.color[index],
            yAxisID: yIds[index],
          };
          Ydata.push(dataset);

          
        })
        setYdata(Ydata);

      })
      .catch(err => {
        console.log(err);
      },)
    } 
    React.useEffect(() => {      
      getNewData();
      let currOptions = options
      currOptions.scales.y.title.text = props.chartdata.label[0];
      if (props.chartdata.label.length >1){
        currOptions.scales.y1.display=true;
        currOptions.scales.y1.title.text = props.chartdata.label[1];
      }
      setOptions(currOptions);      
      const interval = setInterval(() => {
        getNewData();
      }, 10000);
    
      return () => clearInterval(interval);
    }, []); 



    return (
      <div>
        <Line options={options} data={data} />
      </div>
    );
  }
