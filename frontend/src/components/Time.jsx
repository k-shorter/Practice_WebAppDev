import React from 'react';

const DateDisplay = ({ dateStr }) => {
  const dateObj = new Date(`${dateStr}Z`);

  // ローカルタイムゾーン（JST）で表示
  const formattedDate = dateObj.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });

  // UTCとして表示
  const utcDate = dateObj.toISOString();

  // 現在の日時の取得
  const now = new Date();

  // 現在の日時のローカルタイムゾーン（JST）で表示
  const formattedNow = now.toLocaleString('ja-JP', { timeZone: 'Asia/Tokyo' });

  // 現在の日時をUTCとして表示
  const utcNow = now.toISOString();

  return (
    <div>
      <h3>Received Date</h3>
      <p>Local Time (JST): {formattedDate}</p>
      <p>UTC Time: {utcDate}</p>
      <h3>Current Date</h3>
      <p>Local Time (JST): {formattedNow}</p>
      <p>UTC Time: {utcNow}</p>
    </div>
  );
};


export default DateDisplay;
