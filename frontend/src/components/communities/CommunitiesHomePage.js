import React from 'react';
// import styles from '../styles/Communities.module.css'
import PopularCommunities from './PopularCommunities';
import CommunitiesList from './CommunitiesList';

const CommunitiesHome = () => {
  return (
<div className="container mt-4">
  <h1>Communities Home Page</h1>
  <br></br>
  <div className="row">
    <div className="col-md-4 d-none d-md-block">
      {/* Popular Communities */}
      <h4>Popular Communities</h4>
      < PopularCommunities />
      {/* < PopularCommunities /> */}
    </div>
    <div className="col-md-4">
      {/* User's Joined Communities Component */}
      <h4>Communities</h4>
      < CommunitiesList />
    </div>
    <div className="col-md-4 d-none d-md-block">
      {/* Trending Communities Component */}
      <h4>Trending Communities</h4>
    </div>
  </div>
</div>

  );
};

export default CommunitiesHome;