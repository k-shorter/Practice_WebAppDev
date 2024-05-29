import React from 'react';

function CarouselImage({ src, alt ,className}) {
  return (
    <img
    className={`d-block w-100 ${className}`}
      src={src}
      alt={alt}
    />
  );
}

export default CarouselImage;
