import React, { useState } from "react";
import IconWithTitle from "../components/IconWithTitle";
import CustomProgressBar from "../components/CustomProgressBar";
import CustomCard from "../components/CustomCard";
import CustomButtonGroup from "../components/CustomButtonGroup";
import CustomCarousels from "../components/CustomCarousels";
import Keypad from '../components/Keypad';



import "../styles/global.css";

const LayoutTestPage = () => {
  const [input, setInput] = useState('');

  const handleKeyPress = (key) => {
    setInput(prevInput => prevInput + key);
    console.log('Key pressed:', key);
  }
  return(
    <div className="container">
      レイアウトテスト
      <div className="component">
        <p>コンテンツ1</p>
      </div>
      <div className="component">
        <p>コンテンツ2</p>
      </div>
      <div className="widecomponent">
      <div className="input-display">{input}</div>
      <Keypad onKeyPress={handleKeyPress} />
      </div>
    </div>
    );
};

export default LayoutTestPage;
