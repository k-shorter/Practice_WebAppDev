import React from 'react';
import styles from './IconWithTitle.module.css'; // CSSファイルをインポート

const IconWithTitle = ({ iconSrc, title }) => {
  return (
    <div className={styles.container}>
      <img src={iconSrc} alt={title} className={styles.icon} />
      <p className={styles.title}>{title}</p>
    </div>
  );
};

export default IconWithTitle;
