import React from 'react';
import { Link } from 'react-router-dom';
import styles from './Footer.module.css';

const Footer = () => {
    return (
        <footer className={styles.footer}>
            <p className={styles.text}><Link className={styles.link} to="/privacy">Privacy policy</Link></p>
            <p className={styles.text}>&copy; 2024 Makasete</p>
        </footer>
    );
};

export default Footer;
