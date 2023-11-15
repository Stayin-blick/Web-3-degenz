import React, { useState, useEffect } from "react";
import { Card } from "react-bootstrap";
import styles from "../styles/Communities.module.css";
import { useParams } from "react-router-dom";
import axios from "axios";

export const CommunityInfoBadge = () => {
  const { pk } = useParams();
  const [community, setCommunity] = useState(null);

  useEffect(() => {
    const fetchCommunityData = async () => {
      try {
        const response = await axios.get(`/communities/${pk}/info/`);
        setCommunity(response.data);
        console.log(response);
      } catch (error) {
        console.error("Error fetching community data:", error);
      }
    };

    fetchCommunityData();
  }, [pk]);

  if (!community) {
    return <p>Loading...</p>;
  }

  return (
    <div>
      <Card>
        <Card.Body>
          <Card.Title>{community.name}</Card.Title>
          <img
            className={styles.community_pfp}
            src={community.image}
            alt="community pic"
          />
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
