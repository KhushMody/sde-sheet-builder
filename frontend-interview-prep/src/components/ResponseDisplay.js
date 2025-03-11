import React from "react";

const ResponseDisplay = ({ response }) => {
  return (
    <div>
      <h3>Response:</h3>
      <pre>{response}</pre>
    </div>
  );
};

export default ResponseDisplay;
