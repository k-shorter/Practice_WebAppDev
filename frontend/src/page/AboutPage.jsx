import React from 'react';
import { Form, Button, FormGroup, FormControl, FormLabel } from 'react-bootstrap';

const AboutPage = () => {
  return (
    <div className="container">
      <h1>About Page</h1>
      <Form>
        <FormGroup controlId="formBasicRange">
          <FormLabel>シークバー</FormLabel>
          <FormControl type="range" />
        </FormGroup>
        <FormGroup controlId="formBasicCheckbox">
          <Form.Check type="checkbox" label="チェックボックス" />
        </FormGroup>
        <FormGroup controlId="formBasicName">
          <FormLabel>名前</FormLabel>
          <FormControl type="text" placeholder="名前を入力してください" />
        </FormGroup>
        <FormGroup controlId="formBasicRadio">
          <Form.Check type="radio" label="Yes" name="formRadio" id="formRadio1" />
          <Form.Check type="radio" label="No" name="formRadio" id="formRadio2" />
        </FormGroup>
        <Button variant="primary" type="submit">
          送信
        </Button>
      </Form>
      <div className="mt-3">
        <h3>金額: ¥2000</h3>
      </div>
    </div>
  );
};

export default AboutPage;
