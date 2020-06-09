import React from "react";
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Container from "@material-ui/core/Container";
import Box from "@material-ui/core/Box";
import ScrollTop from "./components/ScrollTop";
import Fab from '@material-ui/core/Fab';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';

export default function Layout({ children }) {
  return (
    <React.Fragment>
      <CssBaseline />
      <AppBar position="static" style={{ backgroundColor: "#043454" }}>
        <Toolbar id="back-to-top-anchor"></Toolbar>
      </AppBar>
      <Container>
        <Box my={4}>{children}</Box>
      </Container>
      <ScrollTop>
        <Fab color="secondary" size="small">
          <KeyboardArrowUpIcon />
        </Fab>
      </ScrollTop>
    </React.Fragment>
  );
}