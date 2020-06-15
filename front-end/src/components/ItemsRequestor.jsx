import React, { useState, useEffect } from "react";
import queryString from "query-string";
import { connect } from "react-redux";
import { setItemsList } from "../actions";
import * as requests from "../utils/requests";

function ItemsRequestor(props) {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const { parseItemsList, urlParams } = props;
  const queryParams = queryString.stringify(urlParams); // TODO: sorting: false

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);
      try {
        const json = await requests.get(`/api/v1/notifications/?${queryParams}`).then(
          requests.getResponseJsonOrError);
        console.log(json);
        parseItemsList(json);
      } catch (error) {
        setIsError(true);
      }
      setIsLoading(false);
    };
    fetchData();
  }, [queryParams]);

  return null;
}

export default connect(
  state => ({
    urlParams: {
      page: state.filters.currentPage,
      published_parsed__date: state.filters.currentDate,
      exclude_downvoted: state.filters.hideDownvoted
    }
  }),
  dispatch => ({
    parseItemsList: ({ results, count }) => dispatch(setItemsList(results, count)), 
  })
)(ItemsRequestor);
