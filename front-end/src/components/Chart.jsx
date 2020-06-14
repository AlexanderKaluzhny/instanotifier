import React, { useState, useEffect } from "react";
import Chart from "react-apexcharts";
import * as requests from "../utils/requests";

const options = {
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
  stroke: {
    curve: 'smooth',
  },
  xaxis: {
    type: "datetime",
    // categories: data.map((item) => item[0]),
  },
  yaxis: {
    min: 0,
  },
  tooltip: {
    x: {
      format: "dd MMM yyyy",
    },
  },
}

function useApi(url) {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const [response, setResponse] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);
      try {
        const json = await requests.get(url).then(
          requests.getResponseJsonOrError);
          console.log(json);
        setResponse(json);
      } catch (error) {
        setIsError(true);
      }
      setIsLoading(false);
    };
    fetchData();
  }, [url]);

  return [response, isLoading, isError];
}

export function CountriesChart(props) {
  const [response, isLoading, isError] = useApi("/api/v1/statistics/countries/daily-posted/");
  const series = (response.countries || []).map(country => ({ name: country.name, data: country.data }));
  // const series = [{
  //   name: "series-1",
  //   data: data.map((item) => item[1]),
  // },
  // {
  //   name: "series-2",
  //   data: data.map((item) => item[1]),
  // }]
  return (
    <Chart options={options} series={series} type="line" height={500} />
  )
};

export function TotalPostedChart(props) {
  const [response, isLoading, isError] = useApi("/api/v1/statistics/daily-totals/");
  const series = [{ name: "total", data: response.total || [] }];

  return <Chart options={options} series={series} type="line" height={500} />;
} 