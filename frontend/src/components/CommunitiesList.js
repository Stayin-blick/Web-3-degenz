import React from 'react';
import CommunityBadge from './CommunityBadge';

const CommunitiesList = ({ communities }) => {
  return (
    <div>
      {communities.map((community) => (
        <CommunityBadge key={community.id} community={community} />
      ))}
    </div>
  );
};

export default CommunitiesList;