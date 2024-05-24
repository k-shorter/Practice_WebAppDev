import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import HomePage from './page/HomePage';
import AboutPage from './page/AboutPage';
import ContactPage from './page/ContactPage';

const App = () => {
  const [sharedValue, setSharedValue] = useState('Initial Value');

  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li>
              <Link to="/">Home</Link>
            </li>
            <li>
              <Link to="/about">About</Link>
            </li>
            <li>
              <Link to="/contact">Contact</Link>
            </li>
          </ul>
        </nav>

        <Routes>
          <Route path="/" element={<HomePage sharedValue={sharedValue} setSharedValue={setSharedValue} />} />
          <Route path="/about" element={<AboutPage sharedValue={sharedValue} setSharedValue={setSharedValue} />} />
          <Route path="/contact" element={<ContactPage />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
