import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import LayoutTestPage from './pages/LayoutTestPage';
import OrganizerTopPage from './pages/OrganizerTopPage';
import OrganizerWaitPage from './pages/OrganizerWaitPage';
import ParticipantTopPage from './pages/ParticipantTopPage';
import ParticipantWaitPage from './pages/ParticipantWaitPage';
import SearchAndReservePage from './pages/SearchAndReservePage';



const App = () => {
  return (
    <Router>
      <Layout>
        <Routes>

        <Route path="/" element={<LayoutTestPage />} />
        <Route path="/organizer-top" element={<OrganizerTopPage />} />
        <Route path="/organizer-wait/:eventId" element={<OrganizerWaitPage />} />
        <Route path="/participant-top/:eventId" element={<ParticipantTopPage />} />
        <Route path="/participant-wait/:eventId" element={<ParticipantWaitPage />} />
        <Route path="/search-reserve" element={<SearchAndReservePage />} />


        </Routes>
      </Layout>
    </Router>
  );
};

export default App;