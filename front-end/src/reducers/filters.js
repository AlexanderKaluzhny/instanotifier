import * as filtersActions from "../actions";

const initialState = {
  currentPage: 1,
}

const filters = (state = initialState, action) => {
  switch (action.type) {
    case (filtersActions.SET_CURRENT_PAGE):
      return {
        ...state,
        currentPage: action.currentPage
      }
    default:
      return state
  }
}

export default filters;