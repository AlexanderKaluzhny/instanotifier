import React from 'react';
import { Typography, Grid } from "@material-ui/core";
import SwitchDownvoted from "./SwitchDownvoted";

export default function DrawerContent(props) {
  return (
    <React.Fragment>
      <Grid container alignItems="center">
        <Grid item>
          <Typography>Hide Downvoted</Typography>
        </Grid>
        <Grid item>
          <SwitchDownvoted />
        </Grid>
      </Grid>
    </React.Fragment>
  );

}