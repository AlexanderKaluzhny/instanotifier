import React, { useState, useEffect } from "react";
import { connect, useDispatch} from "react-redux";
import * as requests from "../utils/requests";
import { setItemsList } from "../actions";

function ItemsRequestor(props) {
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);
  const dispatch = useDispatch();

  useEffect(() => {
    const fetchData = async () => {
      setIsError(false);
      setIsLoading(true);
      try {
        const json = await requests.get("/api/v1/notifications/").then(
          requests.getResponseJsonOrError);
        console.log(json);
        dispatch(setItemsList(json.results, json.count));
        
      } catch (error) {
        setIsError(true);
      }
      setIsLoading(false);
    };
    fetchData();
  }, []);

  return null;
}

export default ItemsRequestor;