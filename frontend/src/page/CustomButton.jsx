import React, { useState } from 'react';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import ToggleButton from 'react-bootstrap/ToggleButton';
import styles from './CustomButton.module.css'; // CSSファイルをインポート
import '../styles/global.css'; // グローバルCSSをインポート

function CustomButton({ onClick }) {
  const [checked1, setChecked1] = useState(false);
  const [checked2, setChecked2] = useState(false);

  const handleToggle1 = (e) => {
    setChecked1(e.currentTarget.checked);
    if (e.currentTarget.checked) {
      setChecked2(false);
    }
    onClick();
  };

  const handleToggle2 = (e) => {
    setChecked2(e.currentTarget.checked);
    if (e.currentTarget.checked) {
      setChecked1(false);
    }
    onClick();
  };

  return (
    <>
      <div className={`mb-2 ${styles.customButtonGroup}`}>
        <ToggleButton
          id="toggle-check-1"
          type="checkbox"
          checked={checked1}
          value="1"
          onChange={handleToggle1}
          className={styles.customButton} // カスタムクラスを追加
        >
          Checked
        </ToggleButton>

        <ToggleButton
          id="toggle-check-2"
          type="checkbox"
          checked={checked2}
          value="1"
          onChange={handleToggle2}
          className={styles.customButton} // カスタムクラスを追加
        >
          Checked
        </ToggleButton>
      </div>
    </>
  );
}

export default CustomButton;
