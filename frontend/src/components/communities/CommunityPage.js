import React from 'react';
import { Container, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";

const CommunityHomepage = ({ community }) => {
  return (
    <Container>
      <Row>
        {/* Left Column - Community Info (Hidden on sm screens) */}
        <Col md={3} className="d-none d-md-block">
          {/* Display community information, founder, moderators, etc. */}
        </Col>

        {/* Middle Column - Community Posts */}
        <Col sm={12} md={6}>
            <Row>
                {/* create post */}
            </Row>
            <Row>
                {/* Display community posts here */}
            </Row>
        </Col>

        {/* Right Column - Members and Invite (Hidden on sm screens) */}
        <Col md={3} className="d-none d-md-block">
          {/* Members List */}
          <Row>
            {/* Display the list of community members */}
          </Row>

          <Row>
            {/* Search bar to invite users */}
          </Row>
        </Col>
      </Row>
    </Container>
  );
};

export default CommunityHomepage;
