import { combineReducers } from "redux";
import items from './items';
import filters from './filters';

export default combineReducers({
  items,
  filters,
})