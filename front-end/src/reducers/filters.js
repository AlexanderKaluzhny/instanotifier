import * as filtersActions from "../actions";

const initialState = {
  currentPage: 1,
  currentDate: null,
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
        currentDate: action.currentDate,
      };
    default:
      return state;
  }
};

export default filters;
