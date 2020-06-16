import React from 'react';
import { connect } from "react-redux";
import { useSelector } from 'react-redux';
import Typography from '@material-ui/core/Typography';
import { Box, Grid } from "@material-ui/core";
import ItemCard from "./ItemCard";
import * as requests from "../utils/requests";
import { setItemRating, updateDateItem } from "../actions";

function ItemsList(props) {
  const { itemsList, onRatingChange } = props;

  return (
    <React.Fragment>
      {itemsList &&
        itemsList.map((item) => (
          <Box my={1} key={item.id}>
            <ItemCard
              item={item}
              onRatingChange={(newRating) => onRatingChange(item, newRating)}
            />
          </Box>
        ))}
    </React.Fragment>
  );
}

const requestUpdatedDate = (date) => () => {
  return requests.get(`/api/v1/dates/?date=${date}`);
}

function _ItemsListWithApi(props) {  
  const { updateItemRating, setDateItemContent } = props;

  const handleRatingChange = (item, newRating) => {
    requests
      .patch(`/api/v1/notifications/${item.id}/rate/`, {
        rating: newRating,
      })
      .then(requests.getResponseJsonOrError)
      .then((json) => updateItemRating(json.id, json.rating))
      .then(requestUpdatedDate(item.day_date))
      .then(requests.getResponseJsonOrError)
      .then(jsonList => setDateItemContent(jsonList[0]));
  }

  const { itemsList } = props;

  return <ItemsList onRatingChange={handleRatingChange} itemsList={itemsList} />
}

const ItemsListWithApi = connect(
  (state) => ({
    itemsList: state.items.listChunk,
  }),
  (dispatch) => ({
    updateItemRating: (id, rating) => dispatch(setItemRating(id, rating)),
    setDateItemContent: (dateItem) => dispatch(updateDateItem(dateItem)),
  })
)(_ItemsListWithApi);


export default ItemsListWithApi;