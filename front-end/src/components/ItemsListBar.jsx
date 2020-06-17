import React from 'react';
import { connect } from "react-redux";
import { makeStyles } from '@material-ui/core/styles';
import Typography from '@material-ui/core/Typography';
import Card from '@material-ui/core/Card';
import Pagination from "./Pagination";
import { Box, Grid } from "@material-ui/core";
import DateListItem from "./DateListItem";
import ShowOnlyFilterSelect from "./ShowOnlyFilter";

const useStyles = makeStyles((theme) => ({
  card: {
    padding: theme.spacing(2),
  }
}));

function ItemsListBar(props) {
  const classes = useStyles();
  const { visibleCount, selectedDateItem } = props;

  return (
    <Card className={classes.card}>
      <Grid container spacing={1} alignItems="center" justify="space-between">
        <Grid item xs={5}>
          <Pagination />
        </Grid>
        <Grid item xs={2}>
          <ShowOnlyFilterSelect />
        </Grid>
        <Grid item xs={1}>
          <Typography>
            <b>{`Visible: ${visibleCount}`}</b>
          </Typography>
        </Grid>
        <Grid item xs={4}>
          {selectedDateItem && <DateListItem itemInfo={selectedDateItem} />}
        </Grid>
      </Grid>
    </Card>
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
