import React from 'react';
import clsx from "clsx";
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

const useStyles = makeStyles((theme) => ({
  root: {
    display: 'flex',
    '& > *': {
      margin: theme.spacing(1),
    },
  },
  avatar: {
    width: "2rem",
    height: "2rem",
    fontSize: "1rem",
    display: "inline-flex",
    marginLeft: "1em",
  },
  total: {
    color: theme.palette.getContrastText(colors.blue[500]),
    backgroundColor: colors.blue[500],
  },
  upvoted: {
    color: '#fff',
    backgroundColor: colors.green[500],
  },
  downvoted: {
    color: '#fff',
    backgroundColor: colors.red[500],
  },
}));


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
  const classes = useStyles();
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
          <ListItemText
            primary={
              <Grid container alignItems="center">
                <Grid item xs={5}>
                  <Typography align="center" display="block">{day_date}</Typography>
                </Grid>
                <Grid item xs={7}>
                  <Avatar
                    className={clsx(classes.avatar, classes.total)}
                    sizes="1"
                  >
                    {total}
                  </Avatar>
                  <Avatar
                    className={clsx(classes.avatar, classes.upvoted)}
                    sizes="1"
                  >
                    {upvoted}
                  </Avatar>
                  <Avatar
                    className={clsx(classes.avatar, classes.downvoted)}
                    sizes="1"
                  >
                    {downvoted}
                  </Avatar>
                  <Avatar className={clsx(classes.avatar)} sizes="1">
                    {plain}
                  </Avatar>
                </Grid>
              </Grid>
            }
          />
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