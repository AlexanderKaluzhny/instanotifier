import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';
import Chip from '@material-ui/core/Chip';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ThumbUpOutlinedIcon from '@material-ui/icons/ThumbUpOutlined';
import ThumbUpIcon from '@material-ui/icons/ThumbUp';
import ThumbDownIcon from '@material-ui/icons/ThumbDown';
import ThumbDownOutlinedIcon from '@material-ui/icons/ThumbDownOutlined';
import StarBorderOutlinedIcon from '@material-ui/icons/StarBorderOutlined';
import StarOutlinedIcon from '@material-ui/icons/StarOutlined';
import { Grid, Box, colors } from "@material-ui/core";

const useStyles = makeStyles((theme) => ({
  expand: {
    transform: 'rotate(0deg)',
    margin: 'auto',
    transition: theme.transitions.create('transform', {
      duration: theme.transitions.duration.shortest,
    }),
  },
  expandOpen: {
    transform: 'rotate(180deg)',
  },
}));

export default function ItemCard(props) {
  const [expanded, setExpanded] = React.useState(false);
  const classes = useStyles();

  const handleExpandClick = () => {
    setExpanded(!expanded);
  };
  const { onRatingChange, onBookmarkChange } = props;
  const {
    id,
    title,
    summary,
    short_summary,
    country,
    budget,
    rating,
    source_name,
    is_bookmarked,
  } = props.item;
  const formattedBudget = (!!budget.name ? `${budget.name}: ${budget.value}` : "");

  const getUpvoteButton = () => {
    if (rating === 1) {
      return (
        <IconButton onClick={() => onRatingChange("default")}>
          <ThumbUpIcon color="primary" />
        </IconButton>
      );
    }
    return (
      <IconButton onClick={() => onRatingChange("upvoted")}>
        <ThumbUpOutlinedIcon />
      </IconButton>
    );
  }

  const getDownvoteButton = () => {
    if (rating === -1) {
      return (
        <IconButton onClick={() => onRatingChange("default")}>
          <ThumbDownIcon color="primary" />
        </IconButton>
      );
    }

    return (
      <IconButton onClick={() => onRatingChange("downvoted")}>
        <ThumbDownOutlinedIcon />
      </IconButton>
    );
  }

  const getBookmarkButton = () =>{
    if (is_bookmarked) {
      return (
        <IconButton onClick={() => onBookmarkChange(false)}>
          <StarOutlinedIcon style={{ color: colors.amber[500] }} />
        </IconButton>
      );
    }

    return (
      <IconButton onClick={() => onBookmarkChange(true)}>
        <StarBorderOutlinedIcon />
      </IconButton>
    );
  }

  return (
    <Card>
      <Box p={2}>
        <Grid container>
          <Grid item xs={6} sm={3}>
            <Typography align="left" variant="body1">
              {country}
            </Typography>
          </Grid>
          <Grid item xs={6} sm={3}>
            {formattedBudget && (
              <Chip
                size="small"
                label={formattedBudget}
                color="secondary"
                variant="outlined"
              />
            )}
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography align="right">{source_name}</Typography>
          </Grid>
        </Grid>
      </Box>
      <CardHeader
        style={{ paddingTop: 0 }}
        action={
          <React.Fragment>
            {getUpvoteButton()}
            {getDownvoteButton()}
            {getBookmarkButton()}
          </React.Fragment>
        }
        title={<Typography variant="h6">{title}</Typography>}
      />
      <CardContent style={{ paddingTop: 0, paddingBottom: "1em" }}>
        <Grid container>
          <Grid item xs={11}>
            {!expanded && (
              <Typography variant="body1" component="p">
                <div
                  className="content"
                  dangerouslySetInnerHTML={{ __html: short_summary }}
                ></div>
              </Typography>
            )}
            {expanded && (
              <Typography>
                <div
                  className="content"
                  dangerouslySetInnerHTML={{ __html: summary }}
                ></div>
              </Typography>
            )}
          </Grid>
          <Grid item xs={1} style={{ textAlign: "center" }}>
            <IconButton
              className={clsx(classes.expand, {
                [classes.expandOpen]: expanded,
              })}
              onClick={handleExpandClick}
            >
              <ExpandMoreIcon />
            </IconButton>
          </Grid>
        </Grid>
      </CardContent>
      {/* <CardActions disableSpacing>
        <IconButton aria-label="add to favorites"></IconButton>
      </CardActions> */}
    </Card>
  );
}