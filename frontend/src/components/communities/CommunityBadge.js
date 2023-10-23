import React from 'react';
import { Card, Container, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";

const CommunityBadge = ({ community }) => {
  return (
    <Card className="community">
      <Card.Body>
        <Container fluid>
          <Row>
            {/* Community image - need to fix image and links*/}
            <Col>
              <Link to={`/communities/${community.id}/home_page/${community.id}`}>
                {community.image}
              </Link>
            </Col>
            {/* Community info */}
            <Col xs={6}>
              <Card.Title>
                <Link to={`/communities/${community.id}`}>
                  {community.name}
                </Link>
              </Card.Title>
              <Card.Subtitle>
                members: {community.members.length}
              </Card.Subtitle>
              <Card.Subtitle>
                privacy: {community.privacy}
              </Card.Subtitle>
              <Card.Subtitle>
                last visited: {community.last_visited}
              </Card.Subtitle>
            </Col>
          </Row>
        </Container>
      </Card.Body>
    </Card>
  );
};

export default CommunityBadge;
