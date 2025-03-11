import React from "react";

const SubmitButton = ({ handleSubmit }) => {
  return <button onClick={handleSubmit} style={{ marginTop: "10px" }}>Check Code</button>;
};

export default SubmitButton;
