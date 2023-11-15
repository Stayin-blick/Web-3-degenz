// CommunitiesHome.js

import React from 'react';
import { Row, Col } from "react-bootstrap";
import PopularCommunities from '../../components/PopularCommunities';
import CommunitiesList from '../../components/CommunitiesList';
import styles from '../../styles/Communities.module.css';
import SendInvitationForm from '../../components/SendInvitationForm';
import AcceptInvitationForm from '../../components/AcceptInvitationForm';
<<<<<<< HEAD

=======
>>>>>>> 650c768 (creating user community area post edits likes)

const CommunitiesHome = () => {
  return (
    <div className="container mt-4">
      <Row>
        <Col md={8}>
          <h1>Communities Home Page</h1>
        </Col>
        <Col md={4} className="text-right">
          {/* button/icon to link to community create page */}
        </Col>
      </Row>
      <br></br>
      <Row>
        <Col md={4} className="d-none d-md-block">
          <h4>Popular Communities</h4>
          <PopularCommunities />
        </Col>
        <Col md={4}>
          <h4>Communities</h4>
          <CommunitiesList />
        </Col>
        <Col md={4} className="d-none d-md-block">
          <h4>Invites</h4>
          <Row >
            <Col className={styles.invite_form} md={12}>
              <h5>Send</h5>
<<<<<<< HEAD
              {/* sending invites */}
=======
>>>>>>> 650c768 (creating user community area post edits likes)
              <SendInvitationForm />
            </Col>
          </Row>
          <Row>
            <Col className={styles.invite_form} md={12}>
              <h5>Accept</h5>
<<<<<<< HEAD
              {/* Add component for accepting requests to join here */}
=======
>>>>>>> 650c768 (creating user community area post edits likes)
              <AcceptInvitationForm />
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  );
};

export default CommunitiesHome;
