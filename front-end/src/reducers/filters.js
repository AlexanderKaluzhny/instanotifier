import * as filtersActions from "../actions/filters";

const initialState = {
  currentPage: 1,
  currentDate: null,
  hideDownvoted: true,
};

const filters = (state = initialState, action) => {
  switch (action.type) {
    case filtersActions.SET_CURRENT_PAGE:
      return {
        ...state,
        currentPage: action.currentPage,
      };
    case filtersActions.SET_CURRENT_DATE:
      return {
        ...state,
        currentPage: 1,
        currentDate: action.currentDate,
      };
    case filtersActions.SET_HIDE_DOWNVOTED:
      return {
        ...state,
        currentPage: 1,
        hideDownvoted: action.hideDownvoted,
      };
    default:
      return state;
  }
};

export default filters;
