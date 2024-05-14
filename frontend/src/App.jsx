import React, { useState } from 'react';

import PaymentCalculator from "./components/PaymentCalculator"; // コンポーネントのパスを適切に設定
import AfterpartyForm from "./components/AfterpartyForm"; // コンポーネントのパスを適切に設定
import DisplayPayment from './components/DisplayPayment';
import RegistrationForm from "./components/RegistrationForm"; // コンポーネントのパスを適切に設定


function App() {
  const [perPersonAmount, setPerPersonAmount] = useState(0);
  const [isAfterparty, setIsAfterparty] = useState(false);


  return (
    <>
      <h1>Hello World!</h1>
      <div>
        <h1>割り勘機能</h1>
        <PaymentCalculator perPersonAmount={perPersonAmount} setPerPersonAmount={setPerPersonAmount} />
      </div>
      <div>
        <h1>二次会設定機能</h1>
        <AfterpartyForm isAfterparty={isAfterparty} setIsAfterparty={setIsAfterparty}/>
      </div>
      <div>
        <h1>参加者トップページ</h1>
        <DisplayPayment perPersonAmount={perPersonAmount} />
        <RegistrationForm isAfterparty={isAfterparty}/>
      </div>
    </>
  );
}

export default App;
