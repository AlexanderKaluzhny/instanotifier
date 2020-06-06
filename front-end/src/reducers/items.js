const initialState = {
  count: 0,
  listChunk: [],
  pageSize: 50,
}

const tasks = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_LIST': 
      return {
        ...state,
        count: action.count,
        listChunk: action.listChunk,
      }
    default: 
      return state;
  }
}

export default tasks;