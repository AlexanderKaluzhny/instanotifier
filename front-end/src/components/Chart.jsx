import React from "react";
import Chart from "react-apexcharts";
import data from "./data/sampleData";
import countriesData from "./data/countriesDaily";

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      options: {
        chart: {
          id: "area-datetime",
          type: 'line',
          zoom: {
            enabled: true,
            type: "x",
            autoScaleYaxis: false,
          },
          toolbar: {
            show: true,
            tools: {
              download: true,
              selection: true,
              zoom: true,
              zoomin: true,
              zoomout: true,
              pan: true,
            },
          },
        },
        dataLabels: {
          enabled: false,
        },
        xaxis: {
          type: "datetime",
          // categories: data.map((item) => item[0]),
        },
        yaxis: {
          max: 50,
          min: 0,
        },
        tooltip: {
          x: {
            format: "dd MMM yyyy",
          },
        },
      },
      series: 
        countriesData.countries.map(country => ({ name: country.name, data: country.data }))
        // {
        //   name: "series-1",
        //   data: data.map((item) => item[1]),
        // },
        // {
        //   name: "series-2",
        //   data: data.map((item) => item[1]),
        // },
      ,
    };
  }
  render() {
    return (
      <Chart options={this.state.options} series={this.state.series} type="line" height={500} />
    )
  }
}