import './App.css';
import React from 'react';
import { Provider as StoreProvider } from "react-redux";
import { configureStore } from "./store";
import Container from '@material-ui/core/Container';
import ItemsList from './components/ItemsList';
import ItemsRequestor from './components/ItemsRequestor';
import Pagination from "./components/Pagination";

const store = configureStore();

function App() {
  return (
    <div className="App">
      <StoreProvider store={store}>
        <ItemsRequestor />
        <Container>
          <Pagination />
          <ItemsList />
        </Container>
      </StoreProvider>
    </div>
  );
}

export default App;
