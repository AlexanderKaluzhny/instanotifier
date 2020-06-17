export const SET_LIST = "SET_LIST";
export const SET_RATING = "SET_RATING";
export const SET_BOOKMARK = "SET_BOOKMARK";

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

export const setItemBookmark = (id, isBookmarked) => ({
  type: SET_BOOKMARK,
  id,
  isBookmarked
})