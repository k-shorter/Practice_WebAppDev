import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route, useNavigate, useLocation } from "react-router-dom";

import PaymentCalculator from "./components/PaymentCalculator";
import AfterpartyForm from "./components/AfterpartyForm";
import DisplayPayment from "./components/DisplayPayment";
import RegistrationForm from "./components/RegistrationForm";

function AppContent() {
  const navigate = useNavigate();
  const location = useLocation();
  const [perPersonAmount, setPerPersonAmount] = useState(0);
  const [isAfterparty, setIsAfterparty] = useState(false);
  const [name, setName] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("cash");
  const [isAttending, setIsAttending] = useState(false);

  // URLから状態を読み込む
  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const amount = parseFloat(params.get("amount")) || 0;
    const afterparty = params.get("afterparty") === "true";
    const newName = params.get("name") || "";
    const newPaymentMethod = params.get("paymentMethod") || "cash";
    const attending = params.get("isAttending") === "true";

    if (perPersonAmount !== amount) setPerPersonAmount(amount);
    if (isAfterparty !== afterparty) setIsAfterparty(afterparty);
    if (name !== newName) setName(newName);
    if (paymentMethod !== newPaymentMethod) setPaymentMethod(newPaymentMethod);
    if (isAttending !== attending) setIsAttending(attending);
  }, [location.search]);

  // 状態の変更をURLに反映する
  // useEffect(() => {
  //   const params = new URLSearchParams(location.search);
  //   const amount = parseFloat(params.get("amount")) || 0;
  //   const afterparty = params.get("afterparty") === "true";
  //   const newName = params.get("name") || "";
  //   const newPaymentMethod = params.get("paymentMethod") || "cash";
  //   const attending = params.get("isAttending") === "true";

  //   // 新しい値と現在の状態が異なる場合のみ更新
  //   if (amount !== perPersonAmount ||
  //       afterparty !== isAfterparty ||
  //       newName !== name ||
  //       newPaymentMethod !== paymentMethod ||
  //       attending !== isAttending) {
  //     const newSearch = `?amount=${perPersonAmount}&afterparty=${isAfterparty}&name=${name}&paymentMethod=${paymentMethod}&isAttending=${isAttending}`;
  //     navigate(newSearch, { replace: true });
  //   }
  // }, [perPersonAmount, isAfterparty, name, paymentMethod, isAttending, navigate, location.search]);

  return (
    <>
      <h1>Hello World!</h1>
      <div>
        <h1>割り勘機能</h1>
        <PaymentCalculator
          perPersonAmount={perPersonAmount}
          setPerPersonAmount={setPerPersonAmount}
          isAfterparty={isAfterparty}
        />
      </div>
      <div>
        <h1>二次会設定機能</h1>
        <AfterpartyForm
          isAfterparty={isAfterparty}
          setIsAfterparty={setIsAfterparty}
        />
      </div>
      <div>
        <h1>参加者トップページ</h1>
        <DisplayPayment perPersonAmount={perPersonAmount} />
        <RegistrationForm
          isAfterparty={isAfterparty}
          name={name}
          setName={setName}
          paymentMethod={paymentMethod}
          setPaymentMethod={setPaymentMethod}
          isAttending={isAttending}
          setIsAttending={setIsAttending}
        />
      </div>
    </>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<AppContent />} />
      </Routes>
    </Router>
  );
}

export default App;
