import React from 'react';
import { Link } from 'react-router-dom';
import { Card } from 'react-bootstrap';
import styles from '../styles/Communities.module.css';

const CommunityInfoBadge = ({ community }) => {
  if (!community) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <Card>
        <Card.Body>
          <div class="d-flex" className={styles.titleContainer}>
            <Card.Title>
              {community.name}
            </Card.Title>
            <Link to={`/communities/${community.id}/edit/`}>
              <i className="fa-regular fa-pen-to-square"></i>
            </Link>
          </div>
          <img className={styles.community_pfp} src={community.image} alt="community pic" />
          <Card.Subtitle className={styles.customSubtitle}>
            Owner: {community.owner_username}
          </Card.Subtitle>
          <Card.Subtitle className={styles.customSubtitle}>
            Moderators: {community.moderators_usernames}
          </Card.Subtitle>
          <Card.Subtitle className={styles.customSubtitle}>
            Members Count: {community.members.length}
          </Card.Subtitle>
          <Card.Subtitle className={styles.customSubtitle}>
            privacy: {community.privacy}
          </Card.Subtitle>
        </Card.Body>
      </Card>
    </div>
  );
};

export default CommunityInfoBadge;
