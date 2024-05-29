import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from 'react-bootstrap/Button'; // Assuming you are using react-bootstrap
import styles from './CustomSubmitButtom.module.css';

function CustomSubmitButtom({ action, method, data, redirectTo }) {
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault(); // Prevent default form submission

    try {
      const response = await fetch(action, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        navigate(redirectTo); // Redirect to the specified page
      } else {
        console.error('Failed to submit form');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className={styles.customSubmitButtonFiled}>
    <Button className={styles.customSubmitButton} type="submit" onClick={handleSubmit}>
      Submit
    </Button>
    </div>
  );
}

export default CustomSubmitButtom;
