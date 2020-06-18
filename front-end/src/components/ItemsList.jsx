import React from 'react';
import { connect } from "react-redux";
import Typography from '@material-ui/core/Typography';
import { Box, Grid } from "@material-ui/core";
import ItemCard from "./ItemCard";
import * as requests from "../utils/requests";
import { setItemRating, updateDateItem, setItemBookmark } from "../actions";

function ItemsList(props) {
  const { itemsList, onRatingChange, onBookmarkChange } = props;

  return (
    <React.Fragment>
      {itemsList &&
        itemsList.map((item) => (
          <Box mb={1} key={item.id}>
            <ItemCard
              item={item}
              onRatingChange={(newRating) => onRatingChange(item, newRating)}
              onBookmarkChange={(isBookmarked) => onBookmarkChange(item, isBookmarked)}
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
  const { updateItemRating, setDateItemContent, updateItemBookmark } = props;

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

  const handleBookmarkChange = (item, bValue) => {
    requests.patch(`/api/v1/notifications/${item.id}/bookmark/`, {
      is_bookmarked: bValue,
    })
    .then(requests.getResponseJsonOrError)
    .then((json) => updateItemBookmark(json.id, json.is_bookmarked))
    .then(requestUpdatedDate(item.day_date))
    .then(requests.getResponseJsonOrError)
    .then(jsonList => setDateItemContent(jsonList[0]));
  }

  const { itemsList } = props;

  return (
    <ItemsList
      onRatingChange={handleRatingChange}
      onBookmarkChange={handleBookmarkChange}
      itemsList={itemsList}
    />
  );
}

const ItemsListWithApi = connect(
  (state) => ({
    itemsList: state.items.listChunk,
  }),
  (dispatch) => ({
    updateItemRating: (id, rating) => dispatch(setItemRating(id, rating)),
    updateItemBookmark: (id, isBookmarked) =>  dispatch(setItemBookmark(id, isBookmarked)),
    setDateItemContent: (dateItem) => dispatch(updateDateItem(dateItem)),
  })
)(_ItemsListWithApi);


export default ItemsListWithApi;