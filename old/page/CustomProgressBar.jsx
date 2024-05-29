import React from 'react';
import ProgressBar from 'react-bootstrap/ProgressBar';
import styles from './CustomProgressBar.module.css'; // CSSファイルをインポート

const CustomProgressBar = ({ now }) => {
  return (
    <div className={styles.progressContainer}>
      <ProgressBar now={now} className={styles.progressBar} variant="warning" />
      <img
        src="./src/assets/react.svg" // 画像のパスを指定
        alt="Progress Indicator"
        className={styles.progressImage}
        style={{ left: `calc(${now}% - 12px)` }} // 画像の位置を調整
      />
    </div>
  );
};

export default CustomProgressBar;
