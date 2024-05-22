import React, { createContext, useState, useContext } from "react";

const TimerContext = createContext();

export const TimerProvider = ({ children }) => {
  const [targetTime, setTargetTime] = useState(null);

  return (
    <TimerContext.Provider value={{ targetTime, setTargetTime }}>
      {children}
    </TimerContext.Provider>
  );
};

export const useTimer = () => useContext(TimerContext);
