import React from 'react';
import Nav from 'react-bootstrap/Nav';
import image1 from '../assets/image1.png';
import image2 from '../assets/image2.png';
import image3 from '../assets/image3.png';
import styles from './CustomTab.module.css'; // CSSファイルをインポート

function CustomTab({ activeIndex, onTabClick }) {
  return (
    <Nav variant="tabs" activeKey={activeIndex} onSelect={(selectedKey) => onTabClick(parseInt(selectedKey))}>
      <Nav.Item>
        <Nav.Link eventKey={0} className={activeIndex === 0 ? styles.active : styles.notactive}>
          <img src={image1} alt="First slide" className={styles.tabImage} />
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link eventKey={1} className={activeIndex === 1 ? styles.active : styles.notactive}>
          <img src={image2} alt="Second slide" className={styles.tabImage} />
        </Nav.Link>
      </Nav.Item>
      <Nav.Item>
        <Nav.Link eventKey={2} className={activeIndex === 2 ? styles.active : styles.notactive}>
          <img src={image3} alt="Third slide" className={styles.tabImage} />
        </Nav.Link>
      </Nav.Item>
    </Nav>
  );
}

export default CustomTab;
