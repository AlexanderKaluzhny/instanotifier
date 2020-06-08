import React from "react";
import { makeStyles } from '@material-ui/core/styles';
import clsx from 'clsx';
import Card from '@material-ui/core/Card';
import CardHeader from '@material-ui/core/CardHeader';
import CardContent from '@material-ui/core/CardContent';
import CardActions from '@material-ui/core/CardActions';
import Collapse from '@material-ui/core/Collapse';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';
import ExpandMoreIcon from '@material-ui/icons/ExpandMore';
import ThumbUpOutlinedIcon from '@material-ui/icons/ThumbUpOutlined';
import ThumbUpIcon from '@material-ui/icons/ThumbUp';
import ThumbDownIcon from '@material-ui/icons/ThumbDown';
import ThumbDownOutlinedIcon from '@material-ui/icons/ThumbDownOutlined';
import StarBorderOutlinedIcon from '@material-ui/icons/StarBorderOutlined';
import { Grid } from "@material-ui/core";

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

  const { title, summary, short_summary, country, rating, source_name } = props;
  return (
    <Card>
      <CardHeader
        action={
          <React.Fragment>
            <IconButton aria-label="settings">
              <ThumbUpOutlinedIcon />
            </IconButton>
            <IconButton aria-label="settings">
              <ThumbDownOutlinedIcon />
            </IconButton>
            <IconButton aria-label="settings">
              <StarBorderOutlinedIcon />
            </IconButton>
          </React.Fragment>
        }
        title={<Typography variant="h6">{title}</Typography>}
        subheader={country}
      />
      <CardContent>
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
          <Grid item xs={1}>
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