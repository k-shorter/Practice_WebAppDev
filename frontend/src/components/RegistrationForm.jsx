import React from "react";

function RegistrationForm({
  name,
  setName,
  paymentMethod,
  setPaymentMethod,
  isAttending,
  setIsAttending,
  isAfterparty,
}) {
  const handleSubmit = (event) => {
    event.preventDefault();
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
            onChange={(e) => setName(e.target.value)} // 状態更新関数を確実に呼び出す
          />
        </label>
      </div>
      <div>
        <label>
          支払い方法:
          <select
            value={paymentMethod}
            onChange={(e) => setPaymentMethod(e.target.value)} // 状態更新関数を確実に呼び出す
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
              onChange={(e) => setIsAttending(e.target.checked)} // 状態更新関数を確実に呼び出す
            />
          </label>
        </div>
      )}
      <button type="submit">送信</button>
    </form>
  );
}

export default RegistrationForm;
