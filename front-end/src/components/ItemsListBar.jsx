import React from 'react';
import { useSelector } from 'react-redux';
import Typography from '@material-ui/core/Typography';
import Pagination from "./Pagination";
import { Box, Grid } from "@material-ui/core";

export default function ItemsListBar() {
  const { count } = useSelector(state => state.items)

  return (
    <Grid container alignItems="center">
      <Grid item xs={2}>
        <Typography>
          <b>{`Total: ${count}`}</b>
        </Typography>
      </Grid>
      <Grid item xs={10}>
        <Pagination />
      </Grid>
    </Grid>
  );
}