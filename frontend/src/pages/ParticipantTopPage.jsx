import React, { useState } from 'react';
import { useParams } from 'react-router-dom';
import { Container, Row, Col, Form, Button, Alert } from 'react-bootstrap';

const AddParticipant = () => {
  const { eventId } = useParams();
  const [newParticipant, setNewParticipant] = useState({
    user: { user_name: '' },
    event_id: eventId,
    is_attending: true,
    payment: { payment_method_id: 1, payment_date: new Date().toISOString(), payment_status: 1, updated_at: new Date().toISOString() },
    preference: { genre: '', smoking_allowed: false, budget: 0, additional_info: '' },
  });
  const [successMessage, setSuccessMessage] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  const handleUserChange = (e) => {
    const { name, value } = e.target;
    setNewParticipant((prevState) => ({
      ...prevState,
      user: {
        ...prevState.user,
        [name]: value,
      },
    }));
  };

  const handlePreferenceChange = (e) => {
    const { name, value } = e.target;
    setNewParticipant((prevState) => ({
      ...prevState,
      preference: {
        ...prevState.preference,
        [name]: value,
      },
    }));
  };

  const handleCheckboxChange = (e) => {
    const { name, checked } = e.target;
    setNewParticipant((prevState) => ({
      ...prevState,
      preference: {
        ...prevState.preference,
        [name]: checked,
      },
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/participants/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newParticipant),
      });
      if (response.ok) {
        const data = await response.json();
        setSuccessMessage('Participant added successfully!');
        setErrorMessage(null);
        // Reset form
        setNewParticipant({
          user: { user_name: '' },
          event_id: eventId,
          is_attending: true,
          payment: { payment_method_id: 1, payment_date: new Date().toISOString(), payment_status: 1, updated_at: new Date().toISOString() },
          preference: { genre: '', smoking_allowed: false, budget: 0, additional_info: '' },
        });
      } else {
        const errorData = await response.json();
        setErrorMessage(`Failed to add participant: ${errorData.detail}`);
        setSuccessMessage(null);
      }
    } catch (error) {
      setErrorMessage(`Error: ${error.message}`);
      setSuccessMessage(null);
    }
  };

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md="8">
          <h2>Add Participant</h2>
          {successMessage && <Alert variant="success">{successMessage}</Alert>}
          {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="formUserName">
              <Form.Label>User Name</Form.Label>
              <Form.Control
                type="text"
                name="user_name"
                value={newParticipant.user.user_name}
                onChange={handleUserChange}
                required
              />
            </Form.Group>
            <Form.Group controlId="formGenre">
              <Form.Label>Genre</Form.Label>
              <Form.Control
                type="text"
                name="genre"
                value={newParticipant.preference.genre}
                onChange={handlePreferenceChange}
                required
              />
            </Form.Group>
            <Form.Group controlId="formSmokingAllowed">
              <Form.Label>Smoking Allowed</Form.Label>
              <Form.Check
                type="checkbox"
                name="smoking_allowed"
                checked={newParticipant.preference.smoking_allowed}
                onChange={handleCheckboxChange}
              />
            </Form.Group>
            <Form.Group controlId="formPreferenceBudget">
              <Form.Label>Preference Budget</Form.Label>
              <Form.Control
                type="number"
                name="budget"
                value={newParticipant.preference.budget}
                onChange={handlePreferenceChange}
                required
              />
            </Form.Group>
            <Form.Group controlId="formAdditionalInfo">
              <Form.Label>Additional Info</Form.Label>
              <Form.Control
                type="text"
                name="additional_info"
                value={newParticipant.preference.additional_info}
                onChange={handlePreferenceChange}
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Add Participant
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
};

export default AddParticipant
