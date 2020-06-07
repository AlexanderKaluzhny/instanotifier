import React from 'react';
import { useSelector } from 'react-redux';
import { connect } from "react-redux";
import Typography from '@material-ui/core/Typography';
import TablePagination from '@material-ui/core/TablePagination';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import { setCurrentDate } from "../actions";

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

const DatesList = connect(
  null,
  (dispatch) => ({
    setDateFilter: (date) => dispatch(setCurrentDate(date)),
  })
)(DatesListComponent);

function DatesListComponent(props) {
  const { datesList } = props;
  const [selectedDate, setSelectedDate] = React.useState(null);

  const handleListItemClick = (date) => {
    setSelectedDate(date);
    props.setDateFilter(date);
  };

  return (
    <List component="nav" dense>
      {datesList.map(({ day_date, total, upvoted, downvoted, plain }) => (
        <ListItem
          key={day_date}
          button
          selected={selectedDate === day_date}
          onClick={() => handleListItemClick(day_date)}
        >
          <ListItemText primary={day_date} />
        </ListItem>
      ))}
    </List>
  );
}

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