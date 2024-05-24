import React from 'react';

const AboutPage = ({ sharedValue, setSharedValue }) => {
  return (
    <div>
      <h1>About Page</h1>
      <p>This is the About Page.</p>
      <p>Shared Value: {sharedValue}</p>
      <button onClick={() => setSharedValue('Updated from About Page')}>
        Update Shared Value
      </button>
    </div>
  );
};

export default AboutPage;
