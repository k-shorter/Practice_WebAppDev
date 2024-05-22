import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  useLocation,
  useNavigate,
} from "react-router-dom";

import PaymentCalculator from "./components/PaymentCalculator";
import AfterpartyForm from "./components/AfterpartyForm";
import DisplayPayment from "./components/DisplayPayment";
import RegistrationForm from "./components/RegistrationForm";
import ShareButton from "./components/ShareButton";
import LineShareButton from "./components/LineShareButton";
import Getlocation from "./components/Getlocation";
import Timer from "./components/Timer";
import { TimerProvider, useTimer } from "./components/TimerContext";

function useQuery() {
  return new URLSearchParams(useLocation().search);
}

function AppContent() {
  const navigate = useNavigate();
  const query = useQuery();
  const initialAmount = parseFloat(query.get("amount")) || 0;
  const [perPersonAmount, setPerPersonAmount] = useState(initialAmount);
  const [isAfterparty, setIsAfterparty] = useState(false);
  const [name, setName] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("cash");
  const [isAttending, setIsAttending] = useState(false);
  const { targetTime } = useTimer();

  // URLのクエリパラメータを更新する
  useEffect(() => {
    const params = new URLSearchParams();
    params.set("amount", perPersonAmount);
    navigate(`/?${params.toString()}`, { replace: true });
  }, [perPersonAmount, navigate]);

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
      <div>
        <h1>URL共有</h1>
        <ShareButton /> {/* シェアボタンを追加 */}
      </div>
      <div>
        <h1>LINE共有</h1>
        <LineShareButton /> {/* シェアボタンを追加 */}
      </div>
      <div>
        <h1>緯度経度</h1>
        <Getlocation /> {/* シェアボタンを追加 */}
      </div>
      <div>
        <Timer minutes={3} />
        <p>
          {targetTime ? new Date(targetTime).toLocaleTimeString() : "Not set"}
        </p>
      </div>
    </>
  );
}

function App() {
  return (
    <TimerProvider>
      <Router>
        <Routes>
          <Route path="/" element={<AppContent />} />
        </Routes>
      </Router>
    </TimerProvider>
  );
}

export default App;
