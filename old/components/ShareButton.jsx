import React from "react";

function ShareButton() {
  const handleShare = () => {
    const url = window.location.href; // 現在のURLを取得（クエリパラメータを含む）

    if (navigator.share) {
      navigator
        .share({
          title: "Share URL",
          url: url,
        })
        .then(() => {
          console.log("Thanks for sharing!");
        })
        .catch((error) => {
          console.error("Error sharing:", error);
        });
    } else if (navigator.clipboard) {
      // Fallback for browsers that do not support the Web Share API
      navigator.clipboard
        .writeText(url)
        .then(() => {
          alert("URL copied to clipboard");
        })
        .catch((error) => {
          console.error("Error copying URL to clipboard:", error);
        });
    } else {
      // Further fallback if clipboard API is not supported
      const textArea = document.createElement("textarea");
      textArea.value = url;
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      try {
        document.execCommand("copy");
        alert("URL copied to clipboard");
      } catch (error) {
        console.error("Error copying URL to clipboard:", error);
        alert("Failed to copy URL");
      }
      document.body.removeChild(textArea);
    }
  };

  return <button onClick={handleShare}>Share this page</button>;
}

export default ShareButton;
