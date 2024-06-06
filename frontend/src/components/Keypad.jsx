import React, { useState } from 'react';
import styles from './Keypad.module.css';

const Keypad = () => {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');

  const handleClick = (value) => {
      setInput(input + value);
  };

  const handleClear = () => {
      setInput('');
      setResult('');
  };

  const handleBackspace = () => {
      setInput(input.slice(0, -1));
  };

  const handleCalculate = () => {
      try {
          setResult(eval(input)); // evalは安全ではないため、実際のプロジェクトでは別の方法を検討
      } catch {
          setResult('Error');
      }
  };

  return (
      <div className={styles.calculator}>
          <div className={styles.display}>
              <input type="text" value={input} readOnly />
              <div className={styles.result}>{result}</div>
          </div>
          <div className={styles.keypad}>
              <button className="left" onClick={() => handleClick('+')}>+</button>
              <button className="center" onClick={() => handleClick('1')}>1</button>
              <button className="center" onClick={() => handleClick('2')}>2</button>
              <button className="center" onClick={() => handleClick('3')}>3</button>
              <button className="right tall" onClick={handleBackspace}>⌫</button>

              <button className="left" onClick={() => handleClick('-')}>-</button>
              <button className="center" onClick={() => handleClick('4')}>4</button>
              <button className="center" onClick={() => handleClick('5')}>5</button>
              <button className="center" onClick={() => handleClick('6')}>6</button>
              <button className="right" onClick={handleClear}>C</button>

              <button className="left" onClick={() => handleClick('*')}>*</button>
              <button className="center" onClick={() => handleClick('7')}>7</button>
              <button className="center" onClick={() => handleClick('8')}>8</button>
              <button className="center" onClick={() => handleClick('9')}>9</button>

              <button className="right tall" onClick={handleCalculate}>✔</button>

              <button className="left" onClick={() => handleClick('/')}>/</button>
              <button className="center"></button>
              <button className="center" onClick={() => handleClick('0')}>0</button>
              <button className="center"></button>

          </div>
      </div>
  );
};

export default Keypad;
