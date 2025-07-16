import React, { useState } from "react";
import axios from "axios";
import QuestionInput from "./components/QuestionInput";
import SubmitButton from "./components/SubmitButton";
import QuestionTable from "./components/QuestionTable";
import './App.css';

function App() {
  const [question, setQuestion] = useState("");
  const [responseData, setResponseData] = useState([]);
  const useProduction = true; // Toggle to true when needed
  const DEV_BASE_URL = process.env.REACT_APP_API_BASE_URL; 
  const API_URL      = DEV_BASE_URL 
    ? `${DEV_BASE_URL}/api/analyze`
    : "/api/analyze";

  const handleSubmit = async () => {
    try {
      const res = await axios.post(
        API_URL,
        { question },
        { withCredentials: false }
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
