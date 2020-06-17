import * as filtersActions from "../actions/filters";

const initialState = {
  currentPage: 1,
  currentDate: null,
  hideDownvoted: true,
  showOnly: "all",
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
    case filtersActions.SET_SHOW_ONLY:
      return {
        ...state, 
        currentPage: 1,
        showOnly: action.showOnly
      }
    default:
      return state;
  }
};

export default filters;
