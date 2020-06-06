const initialState = {
  datesList: [],
};

const dates = (state = initialState, action) => {
  switch (action.type) {
    case "SET_DATES_LIST":
      return {
        ...state,
        datesList: action.list,
      };
    default:
      return state;
  }
};

export default dates;
