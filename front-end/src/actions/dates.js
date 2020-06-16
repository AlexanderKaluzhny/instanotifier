export const SET_DATES_LIST = "SET_DATES_LIST";
export const UPDATE_DATE_ITEM = "UPDATE_DATE_ITEM"

export const setDatesList = (list) => ({
  type: SET_DATES_LIST,
  list,
});

export const updateDateItem = (dateItem) => ({
  type: UPDATE_DATE_ITEM,
  dateItem,
})