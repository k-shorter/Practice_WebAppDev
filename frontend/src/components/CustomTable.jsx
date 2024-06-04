import React, { useState } from 'react';
import styles from './CustomTable.module.css';

const CustomTable = ({ data }) => {
  const [tableData, setTableData] = useState(data);

  const handleCheckboxChange = (index) => {
    const newData = [...tableData];
    newData[index].paid = !newData[index].paid;
    setTableData(newData);
  };

  return (
    <div className={styles.tableContainer}>
      <table className={styles.table}>
        <tbody>
          {tableData.map((row, rowIndex) => (
            <tr key={rowIndex}>
              <td>{row.name}</td>
              <td>
                <div className={styles.card}>
                  {row.attendance ? "参加　" : "不参加"}
                  <input
                    type="checkbox"
                    checked={row.attendance}
                    readOnly
                  />
                </div>
              </td>
              <td>
                <div className={styles.card}>
                {row.paid ? "支払い済" : "未支払い"}
                  <input
                    type="checkbox"
                    checked={row.paid}
                    onChange={() => handleCheckboxChange(rowIndex)}
                  />
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default CustomTable;
