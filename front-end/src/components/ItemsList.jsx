import React from 'react';
import { useSelector } from 'react-redux';

function ItemsList(props) {
  const { list: itemsList, count } = useSelector(state => state.items)

  return (
    <React.Fragment>
      <h4>{`Total: ${count}`} </h4>
      <ul>
        {itemsList &&
          itemsList.map(({ title, summary, country, source_name }) => (
            <li key={title}>
              <h5>{title}</h5>
            </li>
          ))}
      </ul>
    </React.Fragment>
  );
}

export default ItemsList;