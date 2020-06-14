export const SET_LIST = "SET_LIST";
export const SET_RATING = "SET_RATING";

export const setItemsList = (listChunk, count) => ({
  type: SET_LIST,
  count,
  listChunk,
});

export const setItemRating = (id, rating) => ({
  type: SET_RATING,
  id, 
  rating
})