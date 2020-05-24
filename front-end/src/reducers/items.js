const initialState = {
  count: 0,
  list: []
}

const tasks = (state = initialState, action) => {
  switch (action.type) {
    case 'SET_LIST': 
      return {
        ...state,
        count: action.count,
        list: action.list,
      }
    default: 
      return state;
  }
}

export default tasks;