import React, { useState } from "react";
import {
  Form,
  Button,
  FormGroup,
  FormControl,
  FormLabel,
} from "react-bootstrap";
import CustomProgressBar from "./CustomProgressBar";
import CustomCard from "./CustomCard";
import CustomButton from "./CustomButton";
import IconWithTitle from "./IconWithTitle";
import DynamicButtonGroup from "./DynamicButtonGroup";


const ContactPage = () => {
  const [progress, setProgress] = useState(30); // プログレスバーの初期値を設定

  return (
    <div className="container">
      <Form>
        <FormGroup controlId="Timer">
          <IconWithTitle iconSrc="./src/assets/react.svg" title="回答期限" />
          <CustomProgressBar now={progress} />
        </FormGroup>

        <FormGroup controlId="PerAmount">
          <CustomCard />
        </FormGroup>

        <FormGroup controlId="PaymentMethod">
          <IconWithTitle iconSrc="./src/assets/react.svg" title="支払い方法" />
          <CustomButton />
        </FormGroup>

        <FormGroup controlId="formBasicName">
          <IconWithTitle iconSrc="./src/assets/react.svg" title="名前" />
          <FormControl type="text" placeholder="名前を入力してください" />
        </FormGroup>

        <FormGroup controlId="sd">
        <DynamicButtonGroup buttonNames={['Option 1', 'Option 2', 'Option 3']} />
        </FormGroup>



        <Button variant="primary" type="submit">
          送信
        </Button>
      </Form>

    </div>
  );
};

export default ContactPage;
