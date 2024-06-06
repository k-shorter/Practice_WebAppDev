import React, { useState } from "react";
import Carousel from "react-bootstrap/Carousel";
import CarouselImage from "./CarouselImage"; // 画像コンポーネントのインポート
import image1 from "../assets/image1.png";
import image2 from "../assets/image2.png";
import image3 from "../assets/image3.png";
import CustomTab from "./CustomTab"; // タブコンポーネントのインポート
import styles from "./CustomCarousels.module.css"; // CSSファイルをインポート

function CustomCarousels() {
  const [index, setIndex] = useState(0);

  const handleSelect = (selectedIndex) => {
    setIndex(selectedIndex);
    console.log(selectedIndex);
  };

  return (
    <div>
      <CustomTab activeIndex={index} onTabClick={handleSelect} />
      <div className={styles.carouselWrapper}>
        <Carousel
          activeIndex={index}
          onSelect={handleSelect}
          interval={null}
          controls={false} /* 左右の矢印を非表示にする */
          indicators={false} /* 下のインジケーターを非表示にする */
        >
          <Carousel.Item className={styles.carouselItem}>
            <CarouselImage
              src={image1}
              alt="First slide"
              className={styles.carouselImage}
            />
            <Carousel.Caption>
              <h3>First slide label</h3>
              <p>Nulla vitae elit libero, a pharetra augue mollis interdum.</p>
            </Carousel.Caption>
          </Carousel.Item>
          <Carousel.Item className={styles.carouselItem}>
            <CarouselImage
              src={image2}
              alt="Second slide"
              className={styles.carouselImage}
            />
            <Carousel.Caption>
              <h3>Second slide label</h3>
              <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</p>
            </Carousel.Caption>
          </Carousel.Item>
          <Carousel.Item className={styles.carouselItem}>
            <CarouselImage
              src={image3}
              alt="Third slide"
              className={styles.carouselImage}
            />
            <Carousel.Caption>
              <h3>Third slide label</h3>
              <p>
                Praesent commodo cursus magna, vel scelerisque nisl consectetur.
              </p>
            </Carousel.Caption>
          </Carousel.Item>
        </Carousel>
      </div>
    </div>
  );
}

export default CustomCarousels;
