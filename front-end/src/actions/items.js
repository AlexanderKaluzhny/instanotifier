export const SET_LIST = 'SET_LIST';

export const setItemsList = (list, count) => dispatch => {
  dispatch({
    type: 'SET_LIST',
    count,
    list
  })
}