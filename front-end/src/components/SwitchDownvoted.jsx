import React from 'react';
import { connect } from "react-redux";
import Switch from '@material-ui/core/Switch';
import { setHideDownvoted } from "../actions";
import { useEffect } from 'react';

function SwitchDownvoted(props) {
  const { switcherState, setSwitcherState } = props;
  // const [state, setState] = React.useState(true);

  const handleChange = (event) => {    
    setSwitcherState(event.target.checked);
  };

  return (
    <Switch
      checked={switcherState}
      onChange={handleChange}
      color="primary"
      name="Hide downvoted"
    />
  );
}

export default connect(
  state => ({
    switcherState: state.filters.hideDownvoted
  }),
  (dispatch) => ({
    setSwitcherState: (bValue) => dispatch(setHideDownvoted(bValue)),
  })
)(SwitchDownvoted);
