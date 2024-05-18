import React from "react";

function LineShareButton() {
  const handleShare = () => {
    const url = window.location.href;
    const lineUrl = `https://social-plugins.line.me/lineit/share?url=${encodeURIComponent(url)}`;
    window.open(lineUrl, '_blank');
  };

  return (
    <button onClick={handleShare}>
      Share on LINE
    </button>
  );
}

export default LineShareButton;

