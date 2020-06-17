import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import clsx from "clsx";
import Typography from "@material-ui/core/Typography";
import Tooltip from '@material-ui/core/Tooltip';
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

function AvatarTooltipped({ children, title, className }) {
  const classes = useStyles();
  return (
    <Tooltip title={title} arrow>
      <Avatar className={clsx(classes.avatar, className)} sizes="1">
        {children}
      </Avatar>
    </Tooltip>
  );
}

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
        <AvatarTooltipped title="Total" className={classes.total}>
          {total}
        </AvatarTooltipped>
        <AvatarTooltipped title="Upvoted" className={classes.upvoted}>
          {upvoted}
        </AvatarTooltipped>
        <AvatarTooltipped title="Downvoted" className={classes.downvoted}>
          {downvoted}
        </AvatarTooltipped>
        <AvatarTooltipped title="Without rating" className="">
          {plain}
        </AvatarTooltipped>
      </Grid>
    </Grid>
  );
}
