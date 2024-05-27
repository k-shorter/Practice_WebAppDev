import React, { useEffect } from 'react';
import { FormGroup, FormControl, FormLabel } from 'react-bootstrap';
import styles from './Slider.module.css'; // CSSファイルをインポート

const Slider = ({ value, setValue, label }) => {
  useEffect(() => {
    updateBackground(value);
  }, [value]);

  const handleSliderChange = (e) => {
    setValue(e.target.value);
  };

  const updateBackground = (value) => {
    const slider = document.querySelector(`.${styles.customRange}`);
    if (slider) {
      slider.style.background = `linear-gradient(to right, #ffc107 ${value}%, #ccc ${value}%)`;
    }
  };

  return (
    <FormGroup controlId="formBasicRange">
      <FormLabel>{label}</FormLabel>
      <FormControl
        type="range"
        value={value}
        min="0"
        max="100"
        onChange={handleSliderChange}
        className={styles.customRange}
      />
    </FormGroup>
  );
};

export default Slider;
