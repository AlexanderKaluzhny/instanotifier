import * as datesActions from "../actions/dates";

const initialState = {
  datesList: [],
};

const dates = (state = initialState, action) => {
  switch (action.type) {
    case datesActions.SET_DATES_LIST:
      return {
        ...state,
        datesList: action.list,
      };
    case datesActions.UPDATE_DATE_ITEM:
      return {
        ...state,
        datesList: state.datesList.map((item) =>
          item.day_date === action.dateItem.day_date ? action.dateItem : item
        ),
      };
    default:
      return state;
  }
};

export default dates;
