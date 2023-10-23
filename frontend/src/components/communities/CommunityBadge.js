import React from 'react';
import { Card, Media, OverlayTrigger, Tooltip } from "react-bootstrap";
import { Link } from "react-router-dom";


const CommunityBadge = ({ community }) => {
  return (
    <Card className="community">
      <Card.Body>
      <Link to={`communities/<int:pk>/home_page/${community.id}`}>
        {community.image}
      </Link>
        <a href={`/communities/${community.id}`}>{community.name}</a>
        {community.members}
        {community.privacy}
        {community.last_visited}
      </Card.Body>
    </Card>
  );
};

export default CommunityBadge;
