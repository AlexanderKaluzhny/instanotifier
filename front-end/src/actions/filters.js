export const SET_CURRENT_PAGE = 'SET_CURRENT_PAGE';

export const setCurrentPage = (page) => ({
  type: SET_CURRENT_PAGE,
  currentPage: page,
});