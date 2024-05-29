import React from "react";
import ProgressBar from "react-bootstrap/ProgressBar";
import styles from "./CustomProgressBar.module.css"; // CSSファイルをインポート
import progressImage from "../assets/react.svg"; // 画像をインポート

const CustomProgressBar = ({ now }) => {
  const progressBarStyle = {
    backgroundColor: "var(--primary-color)", // 直接色を指定
  };

  return (
    <div className={styles.progressContainer}>
      <div className={`progress ${styles.progressBar}`}>
        <div
          role="progressbar"
          className="progress-bar"
          style={{ width: `${now}%`, backgroundColor: "var(--primary-color)" }}
          aria-valuenow={now}
          aria-valuemin="0"
          aria-valuemax="100"
        ></div>
      </div>
      <img
        src={progressImage} // 画像のパスを指定
        alt="Progress Indicator"
        className={styles.progressImage}
        style={{ left: `calc(${now}% - 12px)` }} // 画像の位置を調整
      />
    </div>
  );
};

export default CustomProgressBar;
