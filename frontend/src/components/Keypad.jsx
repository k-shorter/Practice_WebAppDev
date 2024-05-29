import React from 'react';
import styles from './Keypad.module.css';

function Keypad({ onKeyPress }) {
  const buttons = [
    '','1', '2', '3','',
    '','4', '5', '6','',
    '','7', '8', '9','',
    '','*', '0', '#','',
  ];

  return (
    <div className={styles.keypad}>
      {buttons.map((button) => (
        <div 
          key={button} 
          className={styles.button}
          onClick={() => onKeyPress(button)}
        >
          <span>{button}</span>
        </div>
      ))}
    </div>
  );
}

export default Keypad;
