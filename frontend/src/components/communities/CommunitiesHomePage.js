import React from 'react';
import { Row, Col } from "react-bootstrap";
import PopularCommunities from './PopularCommunities';
import CommunitiesList from './CommunitiesList';
import styles from '../../styles/Communities.module.css'


const CommunitiesHome = () => {
  return (
    <div className="container mt-4">
      {/* add a create community button */}
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
          <Row>
            <Col md={12}>
              <h5>Accept Invites</h5>
              {/* Add component for accepting invites here */}
            </Col>
          </Row>
          <Row>
            <Col md={12}>
              <h5>Accept Requests</h5>
              {/* Add component for accepting requests to join here */}
            </Col>
          </Row>
        </Col>
      </Row>
    </div>
  );
};

export default CommunitiesHome;
