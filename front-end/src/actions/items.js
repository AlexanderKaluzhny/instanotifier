export const SET_LIST = "SET_LIST";

export const setItemsList = (listChunk, count) => ({
  type: "SET_LIST",
  count,
  listChunk,
});
