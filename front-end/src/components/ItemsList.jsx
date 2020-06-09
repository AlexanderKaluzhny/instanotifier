import React from 'react';
import { useSelector } from 'react-redux';
import Typography from '@material-ui/core/Typography';
import Pagination from "./Pagination";
import { Box, Grid } from "@material-ui/core";
import ItemCard from "./ItemCard";

function ItemsList(props) {
  const { listChunk: itemsList, count } = useSelector(state => state.items)

  return (
    <React.Fragment>
      <Grid container alignItems="center">
        <Grid item xs={2}>
          <Typography><b>{`Total: ${count}`}</b></Typography>
        </Grid>
        <Grid item xs={10}>
          <Pagination />
        </Grid>
      </Grid>
      {itemsList &&
        itemsList.map((item) => (
          <Box my={1} key={item.title}>
            <ItemCard {...item} />
            {/* <Typography>{item.title}</Typography> */}
          </Box>
        ))}
    </React.Fragment>
  );
}

export default ItemsList;