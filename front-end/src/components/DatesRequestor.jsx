import React, { useState, useEffect } from "react";
import { connect } from "react-redux";
import { setDatesList } from "../actions";
import * as requests from "../utils/requests";

function DatesRequestor(props) {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const { parseDatesList } = props;

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);
      try {
        const json = await requests
          .get(`/api/v1/dates/`)
          .then(requests.getResponseJsonOrError);
        console.log(json);
        parseDatesList(json);
      } catch (error) {
        setIsError(true);
      }
      setIsLoading(false);
    };
    fetchData();
  }, []);

  return null;
}

export default connect(
  null,
  (dispatch) => ({
    parseDatesList: (json) => dispatch(setDatesList(json)),
  })
)(DatesRequestor);
