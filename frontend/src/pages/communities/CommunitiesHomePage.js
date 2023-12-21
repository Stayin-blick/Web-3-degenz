import React, { useEffect, useState } from 'react';
import { Row, Col } from "react-bootstrap";
import PopularCommunities from '../../components/PopularCommunities';
import CommunitiesList from '../../components/CommunitiesList';
import styles from '../../styles/Communities.module.css';
import SendInvitationForm from '../../components/SendInvitationForm';
import AcceptInvitationForm from '../../components/AcceptInvitationForm';
import axios from 'axios';

const CommunitiesHome = () => {
  const [communities, setCommunities] = useState([]);

  useEffect(() => {
    // Fetch the list of communities
    axios.get('/communities/').then((response) => {
      setCommunities(response.data.results);
    });
  }, []);

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
          <PopularCommunities communities={communities} />
        </Col>
        <Col md={4}>
          <h4>Communities</h4>
          <CommunitiesList communities={communities} />
        </Col>
        <Col md={4} className="d-none d-md-block">
          <h4>Invites</h4>
          <Row className="my-3">
            <Col className={` ${styles.invite_form} p-3`} md={12}>
              <h5>Send</h5>
              <SendInvitationForm communities={communities} />
            </Col>
          </Row>
          <Row className="my-3">
            <Col className={` ${styles.invite_form} p-3`} md={12}>
              <h5>Accept</h5>
              <AcceptInvitationForm />
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  );
};

export default CommunitiesHome;
