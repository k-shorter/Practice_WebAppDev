import React, { useState } from 'react';

const Getlocation = () => {
  const [latitude, setLatitude] = useState(null);
  const [longitude, setLongitude] = useState(null);
  const [error, setError] = useState(null);

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLatitude(position.coords.latitude);
          setLongitude(position.coords.longitude);
        },
        (err) => {
          setError(err.message);
        }
      );
    } else {
      setError("Geolocation is not supported by this browser.");
    }
  };

  return (
    <div>
      <h1>Get Current Location</h1>
      <button onClick={getLocation}>Get Location</button>
      {latitude && longitude ? (
        <div>
          <h2>Latitude: {latitude}</h2>
          <h2>Longitude: {longitude}</h2>
        </div>
      ) : (
        <p>{error}</p>
      )}
    </div>
  );
};

export default Getlocation;
