export const SET_CURRENT_PAGE = "SET_CURRENT_PAGE";
export const SET_CURRENT_DATE = "SET_CURRENT_DATE";
export const SET_HIDE_DOWNVOTED = "SET_HIDE_DOWNVOTED";
export const SET_SHOW_ONLY = "SET_SHOW_ONLY_FILTER";

export const setCurrentPage = (page) => ({
  type: SET_CURRENT_PAGE,
  currentPage: page,
});

export const setCurrentDate = (date) => ({
  type: SET_CURRENT_DATE,
  currentDate: date,
});

export const setHideDownvoted = (bValue) => ({
  type: SET_HIDE_DOWNVOTED,
  hideDownvoted: bValue,
});

export const setShowOnly = (value) => ({
  type: SET_SHOW_ONLY,
  showOnly: value
})