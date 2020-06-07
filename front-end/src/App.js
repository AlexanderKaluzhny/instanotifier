import "./App.css";
import React from "react";
import { Provider as StoreProvider } from "react-redux";
import { configureStore } from "./store";
import { Grid } from "@material-ui/core";
import Container from "@material-ui/core/Container";
import ItemsRequestor from "./components/ItemsRequestor";
import DatesRequestor from "./components/DatesRequestor";
import Pagination from "./components/Pagination";
import ItemsList from "./components/ItemsList";
import DatesList from "./components/DatesList";

const store = configureStore();

function App() {
  return (
    <div className="App">
      <StoreProvider store={store}>
        <ItemsRequestor />
        <DatesRequestor />
        <Container>
          <Grid container>
            <Grid item lg={12}>
              <Pagination />
            </Grid>
            <Grid item lg={8}>
              <ItemsList />
            </Grid>
            <Grid item lg={4}>
              <DatesList />
            </Grid>
          </Grid>
        </Container>
      </StoreProvider>
    </div>
  );
}

export default App;
