import React from 'react';
import { connect } from "react-redux";
import { makeStyles } from '@material-ui/core/styles';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import { setShowOnly } from "../actions";

const useStyles = makeStyles((theme) => ({
}));

function ShowOnlyFilterSelect(props) {
  const classes = useStyles();
  const { filterValue, setFilterValue, downvotedHidden } = props;
  const [alertText, setAlert] = React.useState("");

  const handleChange = (event) => {
    const value = event.target.value;
    setFilterValue(value);
    if (value === "downvoted" && downvotedHidden) {
      setAlert("The `Hide Downvoted` option is enabled. The filter woudn't show any values.")
    }
  };

  return (
    <div>
      <FormControl variant="outlined" className={classes.formControl}>
        <Select
          value={filterValue}
          onChange={handleChange}
          className={classes.selectEmpty}
        >
          <MenuItem value="all">
            Show All
          </MenuItem>
          <MenuItem value="upvoted">Upvoted</MenuItem>
          <MenuItem value="downvoted" disabled={downvotedHidden}>Downvoted</MenuItem>
          <MenuItem value="bookmarked">Bookmarked</MenuItem>
        </Select>
      </FormControl>
    </div>
  );
}

export default connect(
  (state) => ({
    downvotedHidden: state.filters.hideDownvoted,
    filterValue: state.filters.showOnly,
  }),
  (dispatch) => ({
    setFilterValue: (value) => dispatch(setShowOnly(value)),
  })
)(ShowOnlyFilterSelect);
