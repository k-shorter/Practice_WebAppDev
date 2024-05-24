import React from 'react';
import { useNavigate } from 'react-router-dom';

const HomePage = ({ sharedValue, setSharedValue }) => {
  const navigate = useNavigate();

  const goToAboutPage = () => {
    navigate('/about');
  };

  return (
    <div>
      <h1>Home Page</h1>
      <p>Welcome to the Home Page!</p>
      <p>Shared Value: {sharedValue}</p>
      <button onClick={() => setSharedValue('Updated from Home Page')}>
        Update Shared Value
      </button>
      <button onClick={goToAboutPage}>Go to About Page</button>
    </div>
  );
};

export default HomePage;
