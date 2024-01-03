import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';

const CreateCommunityForm = ({ onSuccess }) => {
  const [communityName, setCommunityName] = useState('');
  const [communityImage, setCommunityImage] = useState(null);  // Use null instead of an empty string
  const [communityContent, setCommunityContent] = useState('');
  const [communityPrivacy, setCommunityPrivacy] = useState('public');

  const handleCreateCommunity = async () => {
    try {
      const formData = new FormData();
      formData.append('name', communityName);
      formData.append('image', communityImage);  // Append the image file
      formData.append('content', communityContent);
      formData.append('privacy', communityPrivacy);

      const response = await axios.post('/communities/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      onSuccess(response.data); // Assuming the response contains the newly created community data
    } catch (error) {
      console.error('Error creating community:', error);
    }
  };

  return (
    <Form>
      <Form.Group controlId="communityName">
        <Form.Label>Community Name</Form.Label>
        <Form.Control
          type="text"
          placeholder="Enter community name"
          value={communityName}
          onChange={(e) => setCommunityName(e.target.value)}
        />
      </Form.Group>

      <Form.Group controlId="communityImage">
        <Form.Label>Community Image</Form.Label>
        <Form.Control
          type="file"
          accept="image/*"  // Limit file input to images
          onChange={(e) => setCommunityImage(e.target.files[0])}
        />
      </Form.Group>

      <Form.Group controlId="communityContent">
        <Form.Label>Community Content</Form.Label>
        <Form.Control
          as="textarea"
          placeholder="Enter community content"
          value={communityContent}
          onChange={(e) => setCommunityContent(e.target.value)}
        />
      </Form.Group>

      <Form.Group controlId="communityPrivacy">
        <Form.Label>Privacy</Form.Label>
        <Form.Control
          as="select"
          value={communityPrivacy}
          onChange={(e) => setCommunityPrivacy(e.target.value)}
        >
          <option value="public">Public</option>
          <option value="private">Private</option>
          <option value="hidden">Hidden</option>
        </Form.Control>
      </Form.Group>

      <Button variant="primary" onClick={handleCreateCommunity}>
        Create Community
      </Button>
    </Form>
  );
};

export default CreateCommunityForm;