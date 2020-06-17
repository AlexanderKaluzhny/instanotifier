import "./App.css";
import React from "react";
import { Provider as StoreProvider } from "react-redux";
import { configureStore } from "./store";
import { Grid } from "@material-ui/core";
import ItemsRequestor from "./components/ItemsRequestor";
import DatesRequestor from "./components/DatesRequestor";
import ItemsList from "./components/ItemsList";
import DatesList from "./components/DatesList";
import Layout from "./Layout";
import ItemsListBar from "./components/ItemsListBar";
import { TotalPostedChart, CountriesChart } from "./components/Chart";

const store = configureStore();

function App() {
  return (
    <div className="App">
      <StoreProvider store={store}>
        <ItemsRequestor />
        <DatesRequestor />
        <Layout>
          <Grid container spacing={1} style={{ minHeight: "70vh" }}>
            <Grid item lg={12}>
              <ItemsListBar />
            </Grid>
            <Grid item lg={8}>
              <ItemsList />
            </Grid>
            <Grid item lg={4}>
              <DatesList />
            </Grid>
          </Grid>
          <hr />
          <TotalPostedChart />
          <hr />
          <CountriesChart />
        </Layout>
      </StoreProvider>
    </div>
  );
}

export default App;
