import React from "react";
import TableRow from "./TableRow";

const QuestionTable = ({ data }) => {
  console.log("Data received by QuestionTable:", data);

  if (!data || data.length === 0) {
    return <p>No data available.</p>;
  }

  return (
    <div>
      <h3>Questions:</h3>
      <table style={{ margin: "20px auto", borderCollapse: "collapse", width: "80%" }}>
        <thead>
          <tr>
            <th>Company</th>
            <th>Question</th>
            <th>Acceptance</th>
            <th>Difficulty</th>
            <th>Link</th>
          </tr>
        </thead>
        <tbody>
          {data.map((row, index) => (
            <TableRow key={index} row={row} />
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default QuestionTable;
