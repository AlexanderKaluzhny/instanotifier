import React from 'react';
import { connect } from "react-redux";
import { useSelector } from 'react-redux';
import Typography from '@material-ui/core/Typography';
import { Box, Grid } from "@material-ui/core";
import ItemCard from "./ItemCard";
import * as requests from "../utils/requests";
import { setItemRating } from "../actions";

function ItemsList(props) {
  const { listChunk: itemsList, count } = useSelector(state => state.items)
  const { onRatingChange } = props;

  return (
    <React.Fragment>
      {itemsList &&
        itemsList.map((item) => (
          <Box my={1} key={item.title}>
            <ItemCard item={item} onRatingChange={onRatingChange} />
            {/* <Typography>{item.title}</Typography> */}
          </Box>
        ))}
    </React.Fragment>
  );
}

function _ItemsListWithApi(props) {
  const { updateItemRating } = props;

  const handleRatingChange = (id, rating) => {
    requests
      .patch(`/api/v1/notifications/${id}/rate/`, {
        rating: rating,
      })
      .then(requests.getResponseJsonOrError)
      .then((json) => updateItemRating(json.id, json.rating));
  }

  return <ItemsList onRatingChange={handleRatingChange} />
}

const ItemsListWithApi = connect(
  null,
  (dispatch) => ({
    updateItemRating: (id, rating) => dispatch(setItemRating(id, rating)),
  })
)(_ItemsListWithApi);


export default ItemsListWithApi;