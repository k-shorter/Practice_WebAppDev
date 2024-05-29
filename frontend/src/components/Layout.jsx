import React from 'react';
import Header from './Header';
import Footer from './Footer';
import '../styles/global.css';

const Layout = ({ children }) => {
  return (
    <>
      <Header />
      <main className="container">
        {children}
      </main>
      <Footer />
    </>
  );
};

export default Layout;
