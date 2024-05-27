import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Header.module.css';

const Header = () => {
  return (
    <header className={styles.header}>
        <div className={styles.logo}>ロゴマーク</div>
    </header>
  );
};

export default Header;
