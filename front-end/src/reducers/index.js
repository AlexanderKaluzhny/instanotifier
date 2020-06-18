import { combineReducers } from "redux";
import items from "./items";
import filters from "./filters";
import dates from "./dates";

export default combineReducers({
  items,
  filters,
  dates,
});
