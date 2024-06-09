import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "../styles/global.css";

import { Form, Button, Container, Row, Col } from "react-bootstrap";

const OrganizerTopPage = () => {
  const [eventData, setEventData] = useState({
    event_name: "",
    event_date: "",
    total_cost: 0,
    primary_participant_count: 0,
    secondary_participant_count: 0,
    latitude: 0,
    longitude: 0,
    organizer: {
      user: {
        user_name: "",
      },
    },
  });

  const navigate = useNavigate();

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setEventData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  const handleOrganizerChange = (e) => {
    const { name, value } = e.target;
    setEventData((prevState) => ({
      ...prevState,
      organizer: {
        user: {
          ...prevState.organizer.user,
          [name]: value,
        },
      },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch("http://localhost:8000/events/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(eventData),
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Event created:", data);
        navigate(`/organizer-wait/${data.event_id}`);
      } else {
        console.error("Failed to create event");
      }
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="container">
      <Container>
        <Row className="justify-content-md-center">
          <Col md="6">
            <h1>Create Event</h1>
            <Form onSubmit={handleSubmit}>
              <Form.Group controlId="formEventName">
                <Form.Label>Event Name</Form.Label>
                <Form.Control
                  type="text"
                  name="event_name"
                  value={eventData.event_name}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              <Form.Group controlId="formEventDate">
                <Form.Label>Event Date</Form.Label>
                <Form.Control
                  type="datetime-local"
                  name="event_date"
                  value={eventData.event_date}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              <Form.Group controlId="formTotalCost">
                <Form.Label>Total Cost</Form.Label>
                <Form.Control
                  type="number"
                  name="total_cost"
                  value={eventData.total_cost}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              <Form.Group controlId="formPrimaryParticipantCount">
                <Form.Label>Primary Participant Count</Form.Label>
                <Form.Control
                  type="number"
                  name="primary_participant_count"
                  value={eventData.primary_participant_count}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              <Form.Group controlId="formSecondaryParticipantCount">
                <Form.Label>Secondary Participant Count</Form.Label>
                <Form.Control
                  type="number"
                  name="secondary_participant_count"
                  value={eventData.secondary_participant_count}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              <Form.Group controlId="formLatitude">
                <Form.Label>Latitude</Form.Label>
                <Form.Control
                  type="number"
                  step="0.0001"
                  name="latitude"
                  value={eventData.latitude}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              <Form.Group controlId="formLongitude">
                <Form.Label>Longitude</Form.Label>
                <Form.Control
                  type="number"
                  step="0.0001"
                  name="longitude"
                  value={eventData.longitude}
                  onChange={handleInputChange}
                  required
                />
              </Form.Group>
              <Form.Group controlId="formOrganizerName">
                <Form.Label>Organizer Name</Form.Label>
                <Form.Control
                  type="text"
                  name="user_name"
                  value={eventData.organizer.user.user_name}
                  onChange={handleOrganizerChange}
                  required
                />
              </Form.Group>
              <Button variant="primary" type="submit">
                Create Event
              </Button>
            </Form>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default OrganizerTopPage;
