import React, { useEffect, useState } from 'react';
import axios from 'axios';

const CommunitiesList = () => {
  const [communities, setCommunities] = useState([]);

  useEffect(() => {
    // Fetch the list of communities
    axios.get('/communities/').then((response) => {
      setCommunities(response.data);
    });
  }, []);

  return (
    <div>
      <h1>Communities</h1>
      <ul>
        {communities.map((community) => (
          <li key={community.id}>
            <a href={`/community/${community.id}`}>{community.name}</a>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CommunitiesList;
