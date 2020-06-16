import React from 'react';
import { connect } from "react-redux";
import Typography from '@material-ui/core/Typography';
import Pagination from "./Pagination";
import { Box, Grid } from "@material-ui/core";
import DateListItem from "./DateListItem";

function ItemsListBar(props) {
  const { visibleCount, selectedDateItem } = props;

  return (
    <Grid container alignItems="center">
      <Grid item xs={1}>
        <Typography>
          <b>{`Visible: ${visibleCount}`}</b>
        </Typography>
      </Grid>
      <Grid item xs={4}>
        {selectedDateItem && <DateListItem itemInfo={selectedDateItem} />}
      </Grid>
      <Grid item xs={6}>
        <Pagination />
      </Grid>
    </Grid>
  );
}

const mapStateToProps = state => {
  const { datesList } = state.dates;
  const { currentDate } = state.filters;
  const selectedDateItem = datesList && currentDate ? datesList.find( ({ day_date }) => day_date === currentDate ) : null

  return {
    visibleCount: state.items.count,
    selectedDateItem,
  };
}

export default connect(
  mapStateToProps,
  null,
)(ItemsListBar);
