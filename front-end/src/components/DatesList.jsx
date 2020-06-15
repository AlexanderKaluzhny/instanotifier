import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import { useSelector } from 'react-redux';
import { connect } from "react-redux";
import Typography from '@material-ui/core/Typography';
import TablePagination from '@material-ui/core/TablePagination';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import Avatar from '@material-ui/core/Avatar';
import { Grid, colors } from "@material-ui/core";
import { setCurrentDate } from "../actions";
import DateListItem from "./DateListItem";

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

function _DatesList(props) {
  const { datesList } = props;
  const [selectedDate, setSelectedDate] = React.useState(null);

  const handleListItemClick = (date) => {
    setSelectedDate(date);
    props.setDateFilter(date);
  };

  return (
    <List component="nav" dense>
      {datesList.map((item) => (
        <ListItem
          key={item.day_date}
          button
          selected={selectedDate === item.day_date}
          onClick={() => handleListItemClick(item.day_date)}
        >
          <ListItemText
            primary={
              <DateListItem itemInfo={item} />
            }
          />
        </ListItem>
      ))}
    </List>
  );
}

const DatesList = connect(
  null,
  (dispatch) => ({
    setDateFilter: (date) => dispatch(setCurrentDate(date)),
  })
)(_DatesList);

function Pagination(props) {
  const { totalItems, page, setPage, rowsPerPage, setRowsPerPage } = props;

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <TablePagination
      component="div"
      rowsPerPageOptions={[10, 31, 50]}
      count={totalItems}
      page={page}
      onChangePage={handleChangePage}
      rowsPerPage={rowsPerPage}
      onChangeRowsPerPage={handleChangeRowsPerPage}
    />
  );
}

export default function PaginatedDatesList(props) {
  const { datesList } = useSelector(state => state.dates);
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(31);

  return (
    <React.Fragment>
      <DatesList
        datesList={datesList.slice(
          page * rowsPerPage,
          page * rowsPerPage + rowsPerPage
        )}
      />
      <Pagination
        totalItems={datesList.length}
        page={page}
        setPage={setPage}
        rowsPerPage={rowsPerPage}
        setRowsPerPage={setRowsPerPage}
      />
    </React.Fragment>
  );
}