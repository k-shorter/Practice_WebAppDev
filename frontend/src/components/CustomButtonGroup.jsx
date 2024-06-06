import React, { useState } from "react";
import ToggleButton from "react-bootstrap/ToggleButton";
import styles from "./CustomButtonGroup.module.css"; // CSSファイルをインポート

function CustomButtonGroup({ buttonNames }) {
  const [activeButton, setActiveButton] = useState(buttonNames[0]); // 最初のボタンをデフォルトでアクティブに設定

  const handleButtonClick = (value) => {
    setActiveButton(value);
    console.log(value);
  };

  return (
    <div className={styles.customButtonGroup}>
      {buttonNames.map((name, index) => (
        <ToggleButton
          key={index}
          id={`toggle-${name}-${index}`}
          type="radio"
          name="radio"
          value={name}
          checked={activeButton === name}
          onChange={() => handleButtonClick(name)}
          className={`${styles.customButton} ${
            activeButton === name ? styles.active : ""
          }`}
        >
          {name}
        </ToggleButton>
      ))}
    </div>
  );
}

export default CustomButtonGroup;
