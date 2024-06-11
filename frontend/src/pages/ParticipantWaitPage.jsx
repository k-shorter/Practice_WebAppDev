import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Container, Row, Col, Spinner, Alert, Button } from 'react-bootstrap';

const ParticipantWaitPage = () => {
  const { eventId } = useParams();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [reservations, setReservations] = useState([]);

  const fetchReservations = async () => {
    try {
      const response = await fetch(`http://localhost:8000/events/${eventId}/reservations`);
      if (response.ok) {
        const data = await response.json();
        if (data) {
          setReservations(data);
          navigate('/');
        } else {
          setError("No reservations found for this event.");
        }
      } else {
        setError("Failed to fetch reservations");
      }
    } catch (error) {
      setError("Error: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReservations();
  }, [eventId]);

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
              <h1>Reservations for Event {eventId}</h1>
              <Button onClick={fetchReservations}>Check Reservations</Button>
            </div>
          )}
        </Col>
      </Row>
    </Container>
  );
};

export default ParticipantWaitPage;
