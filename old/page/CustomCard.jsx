import React from 'react';
import styles from './CustomCard.module.css'; // CSSファイルをインポート

const CustomCard = () => {
  return (
    <div className={styles.card}>
      <p className={styles.label}>累計金額</p>
      <h2 className={styles.amount}>1,800</h2>
    </div>
  );
};

export default CustomCard;
