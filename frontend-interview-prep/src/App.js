import React, { useState } from "react";
import axios from "axios";
import QuestionInput from "./components/QuestionInput";
import SubmitButton from "./components/SubmitButton";
import QuestionTable from "./components/QuestionTable";
import './App.css';

function App() {
  const [question, setQuestion] = useState("");
  const [responseData, setResponseData] = useState([]);

  const handleSubmit = async () => {
    try {
      const res = await axios.post(
        "http://127.0.0.1:5000/analyze",
        { question },
        { withCredentials: true }
      );

      if (res.data.data) {
        setResponseData(res.data.data);
      } else {
        console.error("No data received");
        setResponseData([]);
      }
    } catch (error) {
      console.error("Error:", error.response ? error.response.data : error.message);
      setResponseData([]);
    }
  };

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h2>SDE Sheet Builder</h2>
      <QuestionInput question={question} setQuestion={setQuestion} />
      <br />
      <SubmitButton handleSubmit={handleSubmit} />
      <QuestionTable data={responseData} />
    </div>
  );
}

export default App;
