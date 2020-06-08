import React from 'react';
import { useSelector } from 'react-redux';
import Typography from '@material-ui/core/Typography';
import { Box } from "@material-ui/core";
import ItemCard from "./ItemCard";

function ItemsList(props) {
  const { listChunk: itemsList, count } = useSelector(state => state.items)

  return (
    <React.Fragment>
      <h4>{`Total: ${count}`} </h4>
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