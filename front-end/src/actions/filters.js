export const SET_CURRENT_PAGE = "SET_CURRENT_PAGE";
export const SET_CURRENT_DATE = "SET_CURRENT_DATE";

export const setCurrentPage = (page) => ({
  type: SET_CURRENT_PAGE,
  currentPage: page,
});

export const setCurrentDate = (date) => ({
  type: SET_CURRENT_DATE,
  currentDate: date
})