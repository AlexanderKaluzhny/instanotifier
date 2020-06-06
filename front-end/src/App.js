import "./App.css";
import React from "react";
import { Provider as StoreProvider } from "react-redux";
import { configureStore } from "./store";
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
          <Pagination />
          <ItemsList />
        </Container>
        <Container>
          <DatesList />
        </Container>
      </StoreProvider>
    </div>
  );
}

export default App;
