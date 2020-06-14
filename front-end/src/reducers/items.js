import * as itemActions from "../actions/items";

const initialState = {
  count: 0,
  listChunk: [],
  pageSize: 20,
};

const items = (state = initialState, action) => {
  switch (action.type) {
    case itemActions.SET_LIST:
      return {
        ...state,
        count: action.count,
        listChunk: action.listChunk,
      };
    case itemActions.SET_RATING:
      return {
        ...state,
        listChunk: state.listChunk.map((item) =>
          item.id === action.id ? { ...item, rating: action.rating } : item
        ),
      };
    default:
      return state;
  }
};

export default items;
