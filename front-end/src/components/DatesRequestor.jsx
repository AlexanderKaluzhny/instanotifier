import React, { useState, useEffect } from "react";
import queryString from "query-string";
import { connect } from "react-redux";
import { setDatesList } from "../actions";
import * as requests from "../utils/requests";

function DatesRequestor(props) {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const { parseDatesList, urlParams } = props;
  const queryParams = queryString.stringify(urlParams); // TODO: sorting: false

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);
      try {
        const json = await requests
          .get(`/api/v1/dates/?${queryParams}`)
          .then(requests.getResponseJsonOrError);
        console.log(json);
        parseDatesList(json);
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
      show_only: state.filters.showOnly,
    }
  }),
  (dispatch) => ({
    parseDatesList: (json) => dispatch(setDatesList(json)),
  })
)(DatesRequestor);
