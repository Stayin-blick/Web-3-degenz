import React from 'react';
// import { Container, Row, Col } from 'react-bootstrap';

const CommunitiesHome = () => {
  return (
<div className="container mt-4">
  <h1>Communities Home Page</h1>
  <div className="row">
    <div className="col-md-4 d-none d-md-block">
      {/* Popular Communities Component */}
      <h4>Communities Home Page</h4>
    </div>
    <div className="col-md-4">
      {/* User's Joined Communities Component */}
      <h4>Communities Home Page</h4>
    </div>
    <div className="col-md-4 d-none d-md-block">
      {/* Trending Communities Component */}
      <h4>Communities Home Page</h4>
    </div>
  </div>
</div>

  );
};

export default CommunitiesHome;
