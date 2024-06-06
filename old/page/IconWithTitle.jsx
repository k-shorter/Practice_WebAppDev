import React from 'react';
import styles from './IconWithTitle.module.css'; // CSSファイルをインポート

const IconWithTitle = ({ iconSrc, title }) => {
  return (
    <div className={styles.container}>
      <img src={iconSrc} alt={title} className={styles.icon} />
      <h2 className={styles.title}>{title}</h2>
    </div>
  );
};

export default IconWithTitle;
