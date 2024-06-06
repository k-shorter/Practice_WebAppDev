import React, { useState } from "react";
import IconWithTitle from "../components/IconWithTitle";
import CustomProgressBar from "../components/CustomProgressBar";
import CustomCard from "../components/CustomCard";
import CustomButtonGroup from "../components/CustomButtonGroup";
import CustomCarousels from "../components/CustomCarousels";
import Keypad from "../components/Keypad";

import Button from 'react-bootstrap/Button';

import CustomTitleImage from "../components/CustomTitleImage";
import CustomModal from "../components/CustomModal";
import CustomTable from "../components/CustomTable";

import "../styles/global.css";

const LayoutTestPage = () => {
  const [input, setInput] = useState("");
  const [modalShow, setModalShow] = useState(false);
  const [tableVisible, setTableVisible] = useState(false); // テーブルの表示状態を管理
  const data = [
    { name: "Alice", attendance: true, paid: true },
    { name: "Bob", attendance: false, paid: false },
    { name: "Charlie", attendance: true, paid: false }
  ];

  const handleKeyPress = (key) => {
    setInput((prevInput) => prevInput + key);
    console.log("Key pressed:", key);
  };

  const handleTableTouch = () => {
    setTableVisible(!tableVisible); // テーブルの表示状態をトグル
  };

  const numbers = Array.from({ length: 19 }, (_, i) => i - 9);

  return (
    <div className="container">
      レイアウトテスト
      <div className="component">
        <p>コンテンツ1</p>
      </div>
      <div className="component">
        <p>コンテンツ2</p>
      </div>
      {/* <div className="widecomponent">
      <div className="input-display">{input}</div>
      <Keypad onKeyPress={handleKeyPress} />
      </div> */}
      <div className="component">
        <div className="row">
          <div className="left">
            <p>コンテンツ2</p>
            <CustomTitleImage />
          </div>
          <div className="right">
            <img src={"/vite.svg"} />
          </div>
        </div>
      </div>
      <div className="component">
        <Button variant="primary" onClick={() => setModalShow(true)}>
          Launch vertically centered modal
        </Button>
        <CustomModal
          show={modalShow}
          onHide={() => setModalShow(false)}
        />
      </div>
      {/* <div
        className={`${"component"} ${tableVisible ? "visibleTable" : "hiddenTable"}`}
        onTouchStart={handleTableTouch}
      >
        <CustomTable data={data} />
      </div> */}
      <CustomTable data={data} />

        <select id="number" name="number">
          {numbers.map((number) => (
            <option key={number} value={number}>
              {number}
            </option>
          ))}
        </select>

    </div>
  );
};

export default LayoutTestPage;
