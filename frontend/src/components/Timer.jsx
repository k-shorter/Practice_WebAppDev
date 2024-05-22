import React, { useState, useEffect } from "react";
import { useTimer } from "./TimerContext";

const Timer = ({ minutes }) => {
  const { targetTime, setTargetTime } = useTimer();
  const [timeLeft, setTimeLeft] = useState({ minutes: 0, seconds: 0 });

  useEffect(() => {
    if (!targetTime) {
      const newTargetTime = new Date().getTime() + minutes * 60000;
      setTargetTime(newTargetTime);
    }
  }, [minutes, targetTime, setTargetTime]);

  useEffect(() => {
    const calculateTimeLeft = () => {
      const now = new Date().getTime();
      const difference = targetTime - now;
      let timeLeft = {};

      if (difference > 0) {
        timeLeft = {
          minutes: Math.floor((difference / 1000 / 60) % 60),
          seconds: Math.floor((difference / 1000) % 60),
        };
      } else {
        timeLeft = {
          minutes: 0,
          seconds: 0,
        };
      }
      return timeLeft;
    };

    const timer = setInterval(() => {
      setTimeLeft(calculateTimeLeft());
    }, 1000);

    return () => clearInterval(timer);
  }, [targetTime]);

  return (
    <div>
      <h1>Timer</h1>
      <span>{String(timeLeft.minutes).padStart(2, "0")}:</span>
      <span>{String(timeLeft.seconds).padStart(2, "0")}</span>
      {timeLeft.minutes === 0 && timeLeft.seconds === 0 && (
        <span> Time's up!</span>
      )}
    </div>
  );
};

export default Timer;
