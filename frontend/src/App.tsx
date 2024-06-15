import React, { useState, useEffect } from "react";
import "./App.css";

function App() {
  const [data, setData] = useState(null);
  const [videoLink, setVideoLink] = useState("");

  useEffect(() => {
    // initial data fetch
  }, []);

  const handleInputChange = (event) => {
    setVideoLink(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("Submitting video link:", videoLink);
    // send the videoLink to your backend for processing
  };

  return (
    <div>
      <h1>AnalyzeYT</h1>
      <form onSubmit={handleSubmit}>
        <label>
          YouTube Video Link:
          <input type="text" value={videoLink} onChange={handleInputChange} />
        </label>
        <button type="submit">Submit</button>
      </form>
      {data ? (
        <pre>{JSON.stringify(data, null, 2)}</pre>
      ) : (
        <p>Loading data...</p>
      )}
    </div>
  );
}

export default App;
