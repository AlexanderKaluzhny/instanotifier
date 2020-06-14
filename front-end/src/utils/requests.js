import { csrfSafeMethod, getCookie } from "./csrf";

async function _fetch(url, options) {
  if (!csrfSafeMethod(options.method)) {
    options.headers["X-CSRFToken"] = getCookie("csrftoken");
  }

  return fetch(url, options);
}

function parseJSON(response) {
  return new Promise((resolve) => {
    const jsonPromise = response.json();
    return jsonPromise.then(
      (json) => {
        return resolve({
          status: response.status,
          statusText: response.statusText,
          ok: response.ok,
          json,
        });
      },
      (rejectObj) => {
        return resolve({
          status: response.status,
          statusText: response.statusText,
          ok: response.ok,
          json: {},
        });
      }
    );
  });
}

export const getResponseJsonOrError = (response) => {
  // source: https://github.com/github/fetch/issues/203#issuecomment-266034180

  return new Promise((resolve, reject) => {
    parseJSON(response)
      .then((parsedResponse) => {
        if (parsedResponse.ok) {
          return resolve(parsedResponse.json);
        }
        return reject({
          errorStatus: parsedResponse.status,
          errorStatusText: parsedResponse.statusText,
          json: parsedResponse.json,
        });
      })
      .catch((error) =>
        reject({
          networkError: error,
        })
      );
  });
};

export const patch = (url, data, fetchOptions) => {
  const options = fetchOptions || {};

  options.body = JSON.stringify(data);
  options.headers = options.headers || {};
  options.headers["Content-Type"] = "application/json";
  options.method = "PATCH";

  return _fetch(url, options);
};

export const post = (url, data, fetchOptions) => {
  const options = fetchOptions || {};

  options.body = JSON.stringify(data);
  options.headers = options.headers || {};
  options.headers["Content-Type"] = "application/json";
  options.method = "POST";

  return _fetch(url, options);
};

export const get = (url, data, fetchOptions) => {
  const options = fetchOptions || {};

  options.headers = options.headers || {};
  options.headers["Content-Type"] = "application/json";
  options.method = "GET";

  return _fetch(url, options);
};
