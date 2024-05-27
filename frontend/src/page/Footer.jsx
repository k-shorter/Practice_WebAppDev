import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

const Footer = () => {
  return (
    <footer className={styles.footer}>
      <div className="container">
        <div className={styles.linkContainer}>
          <p className={styles.text}><Link className={styles.link} to="/contact">Contact Us</Link></p>
          <p className={styles.text}><Link className={styles.link} to="/privacy">Privacy policy</Link></p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
