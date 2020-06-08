const initialState = {
  count: 0,
  listChunk: [],
  pageSize: 20,
};

const items = (state = initialState, action) => {
  switch (action.type) {
    case "SET_LIST":
      return {
        ...state,
        count: action.count,
        listChunk: action.listChunk,
      };
    default:
      return state;
  }
};

export default items;
