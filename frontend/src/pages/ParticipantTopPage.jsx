import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";

import IconWithTitle from "../components/IconWithTitle";
import CustomProgressBar from "../components/CustomProgressBar";
import CustomCard from "../components/CustomCard";
import CustomButtonGroup from "../components/CustomButtonGroup";
import CustomSubmitButtom from "../components/CustomSubmitButtom";

import "../styles/global.css";

const ParticipantTopPage = () => {
  const [progress, setProgress] = useState(50); // プログレスバーの初期値を設定
  return (
    <div className="container">
      参加者トップ
      <div className="component">
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "14px",
          }}
        >
          <IconWithTitle iconSrc="./src/assets/react.svg" title="回答期限" />
          <>09:45</>
        </div>
        <CustomProgressBar now={progress} />
      </div>
      <div className="component">
        <CustomCard />
      </div>
      <Form>
        <div className="component">
          <Form.Group className="mb-3" controlId="formBasicEmail">
            <Form.Label>
              <IconWithTitle iconSrc="./src/assets/react.svg" title="名前" />
            </Form.Label>
            <Form.Control type="name" placeholder="Enter your name" />
          </Form.Group>
        </div>
        <div className="component">
          <IconWithTitle iconSrc="./src/assets/react.svg" title="参加確認" />
          <CustomButtonGroup buttonNames={["参加", "不参加"]} />
        </div>
        <div className="component">
          <IconWithTitle iconSrc="./src/assets/react.svg" title="支払い方法" />
          <CustomButtonGroup buttonNames={["電子マネー", "現金", "済み"]} />
        </div>
        <div className="component">
        <CustomSubmitButtom
          action="/submit"
          method="POST"
          data={0}
          redirectTo="/submit"
        />
        </div>
      </Form>
    </div>
  );
};

export default ParticipantTopPage;
