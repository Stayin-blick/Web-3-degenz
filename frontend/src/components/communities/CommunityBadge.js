import React from 'react';
import { Card, Container, Row, Col } from "react-bootstrap";
import { Link } from "react-router-dom";
import styles from '../../styles/Communities.module.css';

const CommunityBadge = ({ community }) => {
  console.log(community);

  return (
    <Card className={styles.customCardSpacing}>
      <Card.Body className="d-flex justify-content-center align-items-center">
        <Container fluid>
          <Row className="justify-content-center align-items-center">
            {/* Community image */}
            <Col xs={3} className="d-flex justify-content-center">
              <Link to={`/communities/${community.id}/homepage/`}>
                <img className={styles.community_pfp} src={community.image} alt='community pic' />
              </Link>
            </Col>
            {/* Community info */}
            <Col xs={9}>
              <div className="d-flex flex-column align-items-start">
                <Card.Title>
                  <Link to={`/communities/${community.id}/homepage/`}>
                    {community.name}
                  </Link>
                </Card.Title>
                <Card.Subtitle className={styles.customSubtitle}>
                  members: {community.members.length}
                </Card.Subtitle>
                <Card.Subtitle className={styles.customSubtitle}>
                  privacy: {community.privacy}
                </Card.Subtitle>
                <Card.Subtitle className={styles.customSubtitle}>
                  last visited: {community.last_visited}
                </Card.Subtitle>
              </div>
            </Col>
          </Row>
        </Container>
      </Card.Body>
    </Card>
  );
};

export default CommunityBadge;
