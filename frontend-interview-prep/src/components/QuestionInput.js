import React from "react";

const QuestionInput = ({question, setQuestion}) => {
    return(
        <input 
            type="text"
            placeholder="Enter your question here..."
            value={question}
            onChange={(e)=> setQuestion(e.target.value)}
            style={{width: "50%", padding: "8px", marginTop: "10px"}}
        />
    );
}; 

export default QuestionInput;