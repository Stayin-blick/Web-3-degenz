import React, { useEffect, useState } from 'react';
import axios from 'axios';
import CommunityBadge from './CommunityBadge';

const CommunitiesList = () => {
  const [communities, setCommunities] = useState([]);

  useEffect(() => {
    // Fetch the list of communities
    axios.get('/communities/').then((response) => {
      console.log(response.data);
      setCommunities(response.data.results);
    });
  }, []);

  return (
    <div>
      <div>
        {communities.map((community) => (
          <CommunityBadge key={community.id} community={community} />
        ))}
      </div>
    </div>
  );
};

export default CommunitiesList;
