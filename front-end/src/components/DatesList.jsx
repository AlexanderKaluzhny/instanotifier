import React from 'react';
import { useSelector } from 'react-redux';
import Typography from '@material-ui/core/Typography';

function DatesList(props) {
  const { datesList } = useSelector(state => state.dates)

  return (
    <React.Fragment>
      <ul>
        {datesList &&
          datesList.map(({ day_date, total, upvoted, downvoted, plain }) => (
            <li key={day_date}>
              <Typography variant="body1">{day_date}</Typography>
            </li>
          ))}
      </ul>
    </React.Fragment>
  );
}

export default DatesList;