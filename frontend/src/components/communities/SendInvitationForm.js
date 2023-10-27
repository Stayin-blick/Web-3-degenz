import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import axios from "axios";
import styles from "../../styles/Communities.module.css";

const SendInvitationForm = () => {
  const [formData, setFormData] = useState({
    community: "",
    inviteeUsername: "",
  });

  const [availableCommunities, setAvailableCommunities] = useState([]);
  const [userFollowers, setUserFollowers] = useState([]);

  useEffect(() => {
    // Fetch the list of communities that the user is a member of 
    axios
      .get("/communities/") 
      .then((response) => {
        setAvailableCommunities(response.data.results);
      })
      .catch((error) => {
        // Handle errors
      });

    // Fetch the list of user followers 
    axios
      .get("/followed-accounts/") 
      .then((response) => {
        setUserFollowers(response.data.results);
      })
      .catch((error) => {
        // Handle errors
      });
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // send the invitation 
      await axios.post("/invitations/create/", formData);
      // include reset the form, or show a confirmation message
    } catch (error) {
      // Handle errors, such as duplicate invitations, etc.
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group controlId="community">
        <Form.Label>Select a Community</Form.Label>
        <Form.Control
          as="select"
          name="community"
          onChange={(e) =>
            setFormData({ ...formData, community: e.target.value })
          }
        >
          {availableCommunities.map((community) => (
            <option key={community.id} value={community.id}>
              {community.name}
            </option>
          ))}
        </Form.Control>
      </Form.Group>
      <Form.Group controlId="userFollowers">
        <Form.Label>Select a Follower</Form.Label>
        <Form.Control
          as="select"
          name="userFollowers"
          onChange={(e) =>
            setFormData({ ...formData, inviteeUsername: e.target.value })
          }
        >
          {userFollowers.map((follower) => (
            <option key={follower.id} value={follower.followed_name}>
              {follower.followed_name}
            </option>
          ))}
        </Form.Control>
      </Form.Group>
      <Button variant="primary" type="submit">
        Send Invitation
      </Button>
    </Form>
  );
};

export default SendInvitationForm;
