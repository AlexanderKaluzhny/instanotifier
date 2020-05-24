export const SET_CURRENT_PAGE = 'SET_CURRENT_PAGE';

export const setCurrentPage = page => dispatch => {
  dispatch({
    type: SET_CURRENT_PAGE,
    currentPage: page,
  })
}