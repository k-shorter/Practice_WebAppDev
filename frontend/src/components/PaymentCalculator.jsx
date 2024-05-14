import React, { useState } from 'react';

function PaymentCalculator({ perPersonAmount, setPerPersonAmount }) {
  // 状態を管理するためのuseStateフック
  const [totalAmount, setTotalAmount] = useState(0);
  const [numberOfParticipants, setNumberOfParticipants] = useState(1);
//   const [perPersonAmount, setPerPersonAmount] = useState(0);

  // 合計金額または参加人数が変更されたときの処理
  const handleAmountChange = (e) => {
    const newTotal = parseFloat(e.target.value);
    setTotalAmount(newTotal);
    updatePerPersonAmount(newTotal, numberOfParticipants);
  };

  const handleParticipantsChange = (e) => {
    const newParticipants = parseInt(e.target.value, 10);
    setNumberOfParticipants(newParticipants);
    updatePerPersonAmount(totalAmount, newParticipants);
  };

  const updatePerPersonAmount = (total, participants) => {
    if (!isNaN(total) && !isNaN(participants) && participants > 0) {
      setPerPersonAmount((total / participants).toFixed(2));
    } else {
      setPerPersonAmount(0);
    }
    console.log(perPersonAmount)
  };

  return (
    <form>
      <div>
        <label>
          合計金額:
          <input
            type="number"
            value={totalAmount}
            onChange={handleAmountChange}
            min="0"
            step="100"
          />
        </label>
      </div>
      <div>
        <label>
          参加人数:
          <input
            type="number"
            value={numberOfParticipants}
            onChange={handleParticipantsChange}
            min="1"
            step="1"
          />
        </label>
      </div>
      <div>
        一人当たりの支払額: {perPersonAmount} 円
      </div>
    </form>
  );
}

export default PaymentCalculator;
