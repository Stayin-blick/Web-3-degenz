import React from 'react';
import PopularCommunityBadge from './PopularCommunitiesBadge';

const PopularCommunities = ({ communities }) => {
  return (
    <div>
      {communities.map((community) => (
        <PopularCommunityBadge key={community.id} community={community} />
      ))}
    </div>
  );
};

export default PopularCommunities;