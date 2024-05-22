import React, { useState } from "react";

function AfterpartyForm({ isAfterparty, setIsAfterparty }) {
  // 二次会の開催有無を管理するためのuseStateフック
  //   const [isAfterparty, setIsAfterparty] = useState(false);

  // チェックボックスの状態が変更されたときの処理
  const handleCheckboxChange = (event) => {
    setIsAfterparty(event.target.checked);
  };

  return (
    <form>
      <div>
        <label>
          二次会を開催しますか？
          <input
            type="checkbox"
            checked={isAfterparty}
            onChange={handleCheckboxChange}
          />
        </label>
      </div>
      {isAfterparty && <div>二次会の詳細設定をこちらで行ってください。</div>}
    </form>
  );
}

export default AfterpartyForm;
