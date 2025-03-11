import React, { useState } from "react";
import axios from "axios";
import CodeInput from "./components/CodeInput";
import QuestionInput from "./components/QuestionInput";
import SubmitButton from "./components/SubmitButton";
import ResponseDisplay from "./components/ResponseDisplay";

function App() {
  const[code, setCode] = useState("");
  const[question, setQuestion] = useState("");
  const[response, setResponse] = useState("");

  const handleSubmit = async() => {
    try{
      const res = await axios.post("http://127.0.0.1:5000/analyze", { code, question });
      setResponse(res.data.message);
    } catch(error) {
      setResponse("Error analytics code");
    }
  };

  return(
    <div style={{ textAlign: "center", padding: "20px" }}>
    <h2>Code Analyzer</h2>
    <QuestionInput question={question} setQuestion={setQuestion} />
    <br />
    <CodeInput code={code} setCode={setCode} />
    <br />
    <SubmitButton handleSubmit={handleSubmit} />
    <ResponseDisplay response={response} />
    </div>
  );

}

export default App;