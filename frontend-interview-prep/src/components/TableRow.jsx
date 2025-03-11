import React from "react";

const TableRow = ({ row }) => {
  return (
    <tr>
      <td>{row.company}</td>
      <td>{row.question}</td>
      <td>{row.acceptance}</td>
      <td>{row.difficulty}</td>
      <td>
        <a href={row.question_link} target="_blank" rel="noopener noreferrer">
          Link
        </a>
      </td>
    </tr>
  );
};

export default TableRow;
