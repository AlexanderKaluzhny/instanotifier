import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import clsx from "clsx";
import Typography from "@material-ui/core/Typography";
import Avatar from "@material-ui/core/Avatar";
import { Grid, colors } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
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
    color: colors.green[500],
    border: `1px solid ${colors.green[500]}`,
    backgroundColor: "transparent",
  },
  downvoted: {
    color: colors.red[500],
    border: `1px solid ${colors.red[500]}`,
    backgroundColor: "transparent",
  },
}));

export default function DateListItem(props) {
  const classes = useStyles();
  const { day_date, total, upvoted, downvoted, plain } = props.itemInfo;
  
  return (
    <Grid container alignItems="center">
      <Grid item xs={5}>
        <Typography align="center" display="block">
          {day_date}
        </Typography>
      </Grid>
      <Grid item xs={7}>
        <Avatar className={clsx(classes.avatar, classes.total)} sizes="1">
          {total}
        </Avatar>
        <Avatar className={clsx(classes.avatar, classes.upvoted)} sizes="1">
          {upvoted}
        </Avatar>
        <Avatar className={clsx(classes.avatar, classes.downvoted)} sizes="1">
          {downvoted}
        </Avatar>
        <Avatar className={clsx(classes.avatar)} sizes="1">
          {plain}
        </Avatar>
      </Grid>
    </Grid>
  );
}
