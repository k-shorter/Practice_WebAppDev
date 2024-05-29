import React, { useEffect, useState } from 'react';

const Timer = () => {
  const [timeLeft, setTimeLeft] = useState(10 * 60); // 10分（600秒）
  const [progress, setProgress] = useState(0); // 初期進行度100%

  useEffect(() => {
    // 現在の時刻を取得
    const currentTime = new Date();
    // 10分後の時刻を計算
    const tenMinutesLater = new Date(currentTime.getTime() + 10 * 60000);

    // カウントダウンを更新する関数
    const updateCountdown = () => {
      const now = new Date();
      const timeLeftMs = tenMinutesLater - now;
      const timeLeftSec = Math.max(0, Math.floor(timeLeftMs / 1000));
      setTimeLeft(timeLeftSec);

      const progressPercentage = (timeLeftSec / 600) * 100;
      setProgress(100-progressPercentage);
    };

    // 1秒ごとにカウントダウンを更新
    const intervalId = setInterval(updateCountdown, 1000);

    // コンポーネントがアンマウントされたときにインターバルをクリア
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div>
      <p>現在時刻から10分後の時間までのカウントダウン: {Math.floor(timeLeft / 60)}分 {timeLeft % 60}秒</p>
      <div style={{ border: '1px solid #000', width: '100%', height: '20px', position: 'relative', backgroundColor: '#ddd' }}>
        <div
          style={{
            width: `${progress}%`,
            height: '100%',
            backgroundColor: '#4caf50',
            transition: 'width 1s linear',
            position: 'relative'
          }}
        >
          <img
            src="../public/vite.svg" // ここに任意の画像のURLを入力してください
            alt="Progress"
            style={{
              position: 'absolute',
              right: 0,
              top: '-10px',
              transform: 'translateX(50%)',
              width: '20px',
              height: '20px'
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default Timer;
