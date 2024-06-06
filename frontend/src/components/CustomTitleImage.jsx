import React, { useState } from "react";
import styles from "./CustomTitleImage.module.css"; // CSSファイルをインポート

const CustomTitleImage = ({ title = "test", imageUrl = "/vite.svg" }) => {
  const [selectedCard, setSelectedCard] = useState(null);

  const handleCardClick = (index) => {
    setSelectedCard(index);
  };

  return (
    <div className={styles.cards}>
      {[0, 1, 2].map((index) => (
        <div
          key={index}
          className={`${styles.card} ${
            selectedCard === index ? styles.cardSelected : ""
          }`}
          onClick={() => handleCardClick(index)}
        >
          {selectedCard === index ? (
            <div>
              <img className={styles.selectedImg} src={imageUrl} alt={title} />
              <div className={styles.titleSelected}>S {title}</div>
            </div>
          ) : (
            <>
              <div className={styles.title}>{title}</div>
              <img className={styles.img} src={imageUrl} alt={title} />
            </>
          )}
        </div>
      ))}
    </div>
  );
};

export default CustomTitleImage;
