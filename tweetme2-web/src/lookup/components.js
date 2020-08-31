import React, { useEffect, useState } from "react";

export function LoadTweets(callback) {
  const xhr = new XMLHttpRequest();
  const method = "GET";
  const url = "http://localhost:8000/api/tweets/";
  const responseType = "json";
  xhr.responseType = responseType;
  xhr.open(method, url);

  xhr.onload = function () {
    callback(xhr.response, xhr.status);
  };
  xhr.onerror = function (e) {
    console.log(e);
    callback({ message: "Request error." }, 400);
  };
  // xhr.setRequestHeader("HTTP_X_REQUESTED_WITH", "XMLHttpRequest");
  // xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
  xhr.send();
}
