import React, { useState } from "react";

function RegistrationForm({ isAfterparty }) {
  // 状態を管理するためのuseStateフック
  const [name, setName] = useState("");
  const [paymentMethod, setPaymentMethod] = useState("cash");
  const [isAttending, setIsAttending] = useState(false);

  // フォーム送信時の処理
  const handleSubmit = (event) => {
    event.preventDefault(); // デフォルトのフォーム送信を防ぐ
    console.log(
      `Name: ${name}, Payment Method: ${paymentMethod}, Attending Afterparty: ${isAttending}`
    );
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>
          名前:
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
        </label>
      </div>
      <div>
        <label>
          支払い方法:
          <select
            value={paymentMethod}
            onChange={(e) => setPaymentMethod(e.target.value)}
          >
            <option value="cash">現金</option>
            <option value="card">電子マネー</option>
            <option value="transfer">振込</option>
          </select>
        </label>
      </div>
      {isAfterparty && (
        <div>
          <label>
            二次会の参加:
            <input
              type="checkbox"
              checked={isAttending}
              onChange={(e) => setIsAttending(e.target.checked)}
            />
          </label>
        </div>
      )}
      <button type="submit">送信</button>
    </form>
  );
}

export default RegistrationForm;
