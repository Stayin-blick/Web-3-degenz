import React from 'react';
import { Container, Row, Col } from 'react-bootstrap';

const CommunitiesHome = () => {
  return (
    <Container>
      <Row>
        {/* Display the middle column on mobile */}
        <Col md={{ span: 6, order: 'last' }} xs={12}>
          {/* Middle Column */}
          <div className="middle-column">
            {/* Your content for the middle column */}
          </div>
        </Col>
        {/* Display the first column on laptop and tablet screens */}
        <Col md={3} xs={0}>
          {/* First Column */}
          <div className="first-column">
            {/* Your content for the first column */}
          </div>
        </Col>
        {/* Display the third column on laptop and tablet screens */}
        <Col md={3} xs={0}>
          {/* Third Column */}
          <div className="third-column">
            {/* Your content for the third column */}
          </div>
        </Col>
      </Row>
    </Container>
  );
};

export default CommunitiesHome;
