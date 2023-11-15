import React, { useEffect, useState } from 'react';
import axios from 'axios';
import PopularCommunityBadge from './PopularCommunitiesBadge';

const PopularCommunitiesList = () => {
  const [communities, setCommunities] = useState([]);

  useEffect(() => {
    // Fetch the list of communities
    axios.get('/communities/').then((response) => {
      // Sort the communities by the number of members in descending order
      const sortedCommunities = response.data.results.sort((a, b) => b.members.length - a.members.length);
      setCommunities(sortedCommunities);
    });
  }, []);

  return (
    <div>
      <div>
        {communities.map((community) => (
          <PopularCommunityBadge key={community.id} community={community} />
        ))}
      </div>
    </div>
  );
};

export default PopularCommunitiesList;
