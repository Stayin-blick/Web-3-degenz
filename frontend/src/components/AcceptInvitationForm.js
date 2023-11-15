import React, { useState, useEffect } from "react";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import axios from "axios";

const AcceptInvitationForm = () => {
  const [formData, setFormData] = useState({
    community: "",
    accept: "",
  });

  const [invitations, setInvitations] = useState([]);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  useEffect(() => {
    // Fetch the list of invitations that the user has received
    axios
      .get("/invitations/")
      .then((response) => {
        console.log(response)
        // Check if the response has a results array
        const invitationResults = response.data.results || [];

        setInvitations(invitationResults);
      })
      .catch((error) => {
        setError("Failed to fetch invitations.");
      });
  }, []);

  const handleAccept = async (invitationId) => {
    try {
      // Send the acceptance
      await axios.patch(`/invitations/${invitationId}/accept/`);
      setSuccessMessage("Invitation accepted!");
      setInvitations(invitations.filter((invitation) => invitation.id !== invitationId));
      setError(null);
    } catch (error) {
      if (error.response && error.response.data) {
        setError(error.response.data.detail);
      } else {
        setError("Failed to accept invitation.");
      }
    }
  };

  return (
    <div>
      {invitations.length === 0 ? (
        <p>No new invitations</p>
      ) : (
        <Form>
          {error && <div className="error-message">{error}</div>}
          {successMessage && <div className="success-message">{successMessage}</div>}
          <Form.Group controlId="exampleForm.ControlSelect1">
            <Form.Label>Choose a community to accept the invitation</Form.Label>
            <Form.Control as="select" onChange={(e) => setFormData(prevState => ({ ...prevState, community: e.target.value }))}>
              <option value="">Select a Community</option>
              {invitations.map((invitation) => (
                <option key={invitation.id} value={invitation.id}>
                  {invitation.community_name}
                </option>
              ))}
            </Form.Control>
          </Form.Group>
          <Button variant="primary" onClick={() => handleAccept(formData.community)}>
            Accept Invitation
          </Button>
        </Form>
      )}
    </div>
  );
};

export default AcceptInvitationForm;
