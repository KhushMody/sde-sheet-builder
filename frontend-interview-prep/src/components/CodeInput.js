import React from "react";

const CodeInput = ({code, setCode}) => {
    return(
        <textarea 
            rows="6"
            cols="50"
            placeholder="Enter your code here..."
            value={code}
            onChange={(e) => setCode(e.target.value)}
        />
    );
};

export default CodeInput;