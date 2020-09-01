import React, { useEffect, useState } from "react";

import { LoadTweets } from "../lookup";

export function TweetsComponent(props) {
  const textAreaRef = React.createRef();
  const [newTweets, setNewTweets] = useState([]);
  const handleSubmit = (event) => {
    event.preventDefault();
    // console.log(event);
    console.log(textAreaRef.current.value);
    textAreaRef.current.value = "";
    const newVal = textAreaRef.current.value;
    let tempNewTweets = [...newTweets];
    tempNewTweets.unshift({
      content: newVal,
      likes: 0,
      id: 123123,
    });
    setNewTweets(tempNewTweets);
    // console.log(newVal);
  };

  return (
    <div className={props.className}>
      <div className="col-12">
        <form onSubmit={handleSubmit}>
          <textarea
            ref={textAreaRef}
            required={true}
            className="form-control text-dark"
            name="tweet"
          ></textarea>
          <button type="submit" className="btn btn-primary my-3">
            Tweet
          </button>
        </form>
      </div>
      <TweetsList newTweets={newTweets} />
    </div>
  );
}

export function TweetsList(props) {
  const [tweetsInit, setTweetsInit] = useState([]);
  console.log("props.newtweets", props.newTweets);
  useEffect(() => {
    const myCallback = (response, status) => {
      console.log(response, status);
      if (status === 200) {
        setTweetsInit(response);
      } else {
        alert("Error");
      }
    };
    LoadTweets(myCallback);
  }, []);
  return tweetsInit.map((item, index) => {
    return (
      <Tweet
        tweet={item}
        key={`${index}-{item.id}`}
        className="my-5 py-5 border bg-white text-dark"
      />
    );
  });
}

export function ActionBtn(props) {
  const { tweet, action } = props;
  const [likes, setLikes] = useState(tweet.likes ? tweet.likes : 0);
  const [userLike, setUserLike] = useState(
    tweet.userLike === true ? true : false
  );
  const className = props.className
    ? props.className
    : "btn btn-primary btn-sm";
  const actionDisplay = action.display ? action.display : "Action";

  const handleClick = (event) => {
    event.preventDefault();
    if (action.type === "like") {
      if (userLike === true) {
        setLikes(likes - 1);
        setUserLike(false);
      } else {
        setLikes(likes + 1);
        setUserLike(true);
      }
    }
  };

  const display =
    action.type === "like" ? `${tweet.likes} ${actionDisplay}` : actionDisplay;

  return (
    <button className={className} onClick={handleClick}>
      {display}
    </button>
  );
}

export function Tweet(props) {
  const { tweet } = props;
  const className = props.className
    ? props.className
    : "col-10 mx-auto col-md-6";
  return (
    <div className={className}>
      <p>
        {tweet.id} - {tweet.content}
      </p>
      <div className="btn btn-group">
        <ActionBtn tweet={tweet} action={{ type: "like", display: "Likes" }} />
        <ActionBtn
          tweet={tweet}
          action={{ type: "unlike", display: "Unlikes" }}
        />
        <ActionBtn
          tweet={tweet}
          action={{ type: "retweet", display: "Retweet" }}
        />
      </div>
    </div>
  );
}
