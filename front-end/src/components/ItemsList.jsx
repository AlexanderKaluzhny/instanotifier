import React from 'react';
import { useSelector } from 'react-redux';
import Typography from '@material-ui/core/Typography';

function ItemsList(props) {
  const { listChunk: itemsList, count } = useSelector(state => state.items)

  return (
    <React.Fragment>
      <h4>{`Total: ${count}`} </h4>
      <ul>
        {itemsList &&
          itemsList.map(({ title, summary, country, source_name }) => (
            <li key={title}>
              <Typography variant="body1">{title}</Typography>
            </li>
          ))}
      </ul>
    </React.Fragment>
  );
}

export default ItemsList;