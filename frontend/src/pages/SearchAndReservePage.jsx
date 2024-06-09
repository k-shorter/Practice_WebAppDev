import React from 'react';
import { useLocation } from 'react-router-dom';
import { Container, Row, Col, Table } from 'react-bootstrap';

const SearchReservePage = () => {
  const location = useLocation();
  const { bestRestaurants } = location.state || {};

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md="8">
          <h1>Best Restaurants</h1>
          <Table striped bordered hover>
            <thead>
              <tr>
                <th>#</th>
                <th>Name</th>
                <th>Genre</th>
                <th>Budget</th>
                <th>Smoking Allowed</th>
              </tr>
            </thead>
            <tbody>
              {bestRestaurants && bestRestaurants.map((restaurant, index) => (
                <tr key={restaurant.restaurant_id + '-' + index}>
                  <td>{index + 1}</td>
                  <td>{restaurant.restaurant_name}</td>
                  <td>{restaurant.restaurant_details.genre}</td>
                  <td>{restaurant.restaurant_details.budget}</td>
                  <td>{restaurant.restaurant_details.smoking_allowed ? "Yes" : "No"}</td>
                </tr>
              ))}
            </tbody>
          </Table>
        </Col>
      </Row>
    </Container>
  );
};

export default SearchReservePage;
