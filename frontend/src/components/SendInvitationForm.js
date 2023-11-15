import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import axios from "axios";

const SendInvitationForm = ({ preselectedCommunity }) => {
  const [formData, setFormData] = useState({
    community: preselectedCommunity ? preselectedCommunity.id : "",
    invitee_username: "",
    accepted: false,
    community_name: preselectedCommunity ? preselectedCommunity.name : "",
    created_at: "",
    id: preselectedCommunity ? preselectedCommunity.id : null,
  });

  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);
  const [userCommunities, setUserCommunities] = useState([]);
  const [userFollowers, setUserFollowers] = useState([]);

  useEffect(() => {
    const fetchUserCommunities = async () => {
      try {
        const response = await axios.get("/communities/");
        setUserCommunities(response.data.results);
      } catch (error) {
        console.error("Failed to fetch user communities.", error);
      }
    };

    const fetchUserFollowers = async () => {
      try {
        const response = await axios.get("/followed-accounts/");
        setUserFollowers(response.data.results);
      } catch (error) {
        console.error("Failed to fetch user followers.", error);
      }
    };

    fetchUserCommunities();
    fetchUserFollowers();
  }, []);

  useEffect(() => {
    console.log('Preselected Community:', preselectedCommunity);
    if (preselectedCommunity) {
      setFormData((prevData) => ({
        ...prevData,
        community: preselectedCommunity.id,
        community_name: preselectedCommunity.name,
        id: preselectedCommunity.id,
      }));
    }
  }, [preselectedCommunity]);

  const handleCommunityChange = async (selectedCommunityId) => {
    try {
      const response = await axios.get(`/communities/${selectedCommunityId}/edit_community`);
      const selectedCommunityDetails = response.data;
      setFormData((prevData) => ({
        ...prevData,
        community_name: selectedCommunityDetails.name,
        id: selectedCommunityDetails.id,
        created_at: new Date().toISOString(),
      }));
    } catch (error) {
      console.error("Failed to fetch community details.", error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      console.log("Form Data Before Sending Invitation:", formData);

      await axios.post("/invitations/create/", {
        community: formData.community,
        invitee_username: formData.invitee_username,
      });

      console.log("Invitation Sent Successfully!");
      setSuccessMessage("Invitation sent successfully!");
      setFormData({
        community: "",
        invitee_username: "",
        accepted: false,
        community_name: "",
        created_at: "",
        id: null,
      });
      setError(null);
    } catch (error) {
      console.error("Error Sending Invitation:", error);
      setError("Failed to send invitation. Please try again later.");
    }
  };

  console.log("User Communities:", userCommunities);
  console.log("User Followers:", userFollowers);

  return (
    <Form onSubmit={handleSubmit}>
      {error && <div className="error-message">{error}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      <Form.Group controlId="community">
        <Form.Label>Select a Community</Form.Label>
        <Form.Control
          as="select"
          name="community"
          value={formData.community}
          onChange={(e) => {
            setFormData({ ...formData, community: e.target.value });
            handleCommunityChange(e.target.value);
          }}
        >
          <option value="">Select a Community</option>
          {userCommunities.map((community) => (
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
          name="invitee_username"
          value={formData.invitee_username}
          onChange={(e) => setFormData({ ...formData, invitee_username: e.target.value })}
        >
          <option value="">Select a Follower</option>
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
