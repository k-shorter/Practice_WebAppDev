import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Table, Spinner, Alert, Form, Button } from 'react-bootstrap';

const OrganizerWaitPage = () => {
  const { eventId } = useParams();
  const navigate = useNavigate();
  const [participants, setParticipants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [budget, setBudget] = useState(0);
  const [bestRestaurants, setBestRestaurants] = useState([]);

  const fetchParticipants = async () => {
    try {
      const response = await fetch(`http://localhost:8000/events/${eventId}/participants`);
      if (response.ok) {
        const data = await response.json();
        setParticipants(data);
      } else {
        setError("Failed to fetch participants");
      }
    } catch (error) {
      setError("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchParticipants();
    const interval = setInterval(fetchParticipants, 5000); // 5秒ごとにデータを取得
    return () => clearInterval(interval); // クリーンアップ
  }, [eventId]);

  const handleBudgetChange = (e) => {
    setBudget(e.target.value);
  };

  const handleSearchBestRestaurants = async () => {
    try {
      const response = await fetch(`http://localhost:8000/search/best_restaurants/?event_id=${eventId}&budget=${budget}`);
      if (response.ok) {
        const data = await response.json();
        setBestRestaurants(data);
        navigate('/search-reserve', { state: { bestRestaurants: data } });
      } else {
        setError("Failed to fetch best restaurants");
      }
    } catch (error) {
      setError("Error: " + error.message);
    }
  };

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md="8">
          {loading ? (
            <Spinner animation="border" />
          ) : error ? (
            <Alert variant="danger">{error}</Alert>
          ) : (
            <div>
              <h1>Participants for Event {eventId}</h1>
              <Table striped bordered hover>
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Genre Preferences</th>
                    <th>Budget</th>
                    <th>Smoking Allowed</th>
                  </tr>
                </thead>
                <tbody>
                  {participants.map((participant, index) => (
                    <tr key={participant.participant_id}>
                      <td>{index + 1}</td>
                      <td>{participant.user.user_name}</td>
                      <td>{participant.preference ? participant.preference.genre : 'N/A'}</td>
                      <td>{participant.preference ? participant.preference.budget : 'N/A'}</td>
                      <td>{participant.preference ? (participant.preference.smoking_allowed ? "Yes" : "No") : 'N/A'}</td>
                    </tr>
                  ))}
                </tbody>
              </Table>
              <Form>
                <Form.Group controlId="formBudget">
                  <Form.Label>Budget</Form.Label>
                  <Form.Control
                    type="number"
                    name="budget"
                    value={budget}
                    onChange={handleBudgetChange}
                    required
                  />
                </Form.Group>
                <Button variant="primary" onClick={handleSearchBestRestaurants}>
                  Search Best Restaurants
                </Button>
              </Form>
            </div>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default OrganizerWaitPage;
