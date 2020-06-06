import React from 'react';
import MuiPagination from "@material-ui/lab/Pagination";
import { connect } from "react-redux";

function Pagination(props) {
  return <MuiPagination count={props.totalPages} color="primary" />
}

export default connect(
  state => ({
    totalPages: Math.floor(state.items.count / state.items.pageSize) + (
      state.items.count % state.items.pageSize > 0 ? 1 : 0
    )
  }),
  null
)(Pagination);