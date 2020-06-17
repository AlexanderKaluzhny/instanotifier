import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import CssBaseline from '@material-ui/core/CssBaseline';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Container from "@material-ui/core/Container";
import Box from "@material-ui/core/Box";
import ScrollTop from "./components/ScrollTop";
import Drawer from '@material-ui/core/SwipeableDrawer';
import Fab from '@material-ui/core/Fab';
import Link from '@material-ui/core/Link';
import KeyboardArrowUpIcon from '@material-ui/icons/KeyboardArrowUp';
import IconButton from '@material-ui/core/IconButton';
import MenuIcon from '@material-ui/icons/Menu';
import AddBoxIcon from '@material-ui/icons/AddBox';
import DrawerContent from "./components/DrawerContent";
import { Grid } from "@material-ui/core";

const useStyles = makeStyles({
  drawer: {
    width: 250,
  },
  feedsButton: {
    color: "white"
  }
});

function FeedsListButton(props) {
  const classes = useStyles();

  return (
    <IconButton {...props} className={classes.feedsButton}>
      <AddBoxIcon />
    </IconButton>
  );
}

export default function Layout({ children }) {
  const classes = useStyles();
  const [open, setOpen] = React.useState(false);

  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const toggleDrawer = (toState) => setOpen(toState);

  return (
    <React.Fragment>
      <CssBaseline />
      <AppBar position="static" style={{ backgroundColor: "#043454" }}>
        <Toolbar id="back-to-top-anchor">
          <Grid container justify="space-between">
            <IconButton
              color="inherit"
              aria-label="open drawer"
              onClick={handleDrawerOpen}
              edge="start"
            >
              <MenuIcon />
            </IconButton>
            <Link
              href="/feeds/"
              component={FeedsListButton}
              title="Feeds List"
            ></Link>
          </Grid>
        </Toolbar>
      </AppBar>
      <Container>
        <Box my={2}>{children}</Box>
      </Container>
      <ScrollTop>
        <Fab color="secondary" size="small">
          <KeyboardArrowUpIcon />
        </Fab>
      </ScrollTop>
      <Drawer anchor="left" open={open} onClose={() => toggleDrawer(false)}>
        <Box className={classes.drawer} p={2}>
          <DrawerContent />
        </Box>
      </Drawer>
    </React.Fragment>
  );
}