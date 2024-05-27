import React, { useState } from 'react';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ToggleButton from 'react-bootstrap/ToggleButton';
import styles from './DynamicButtonGroup.module.css'; // CSSファイルをインポート

function DynamicButtonGroup({ buttonNames }) {
  const [activeButton, setActiveButton] = useState(buttonNames[0]); // 最初のボタンをデフォルトでアクティブに設定

  const handleButtonClick = (value) => {
    setActiveButton(value);
  };

  return (
    <div className={styles.customButtonGroup}>
      {buttonNames.map((name, index) => (
        <ToggleButton
          key={index}
          id={`toggle-${index}`}
          type="radio"
          variant={activeButton === name ? 'primary' : 'outline-primary'}
          name="radio"
          value={name}
          checked={activeButton === name}
          onChange={() => handleButtonClick(name)}
          className={styles.customButton}
        >
          {name}
        </ToggleButton>
      ))}
    </div>
  );
}

export default DynamicButtonGroup;
