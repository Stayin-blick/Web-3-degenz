import React, { useState, useEffect } from 'react';
import axios from 'axios';

const EditCommunityForm = ({ communityId }) => {
  const [communityData, setCommunityData] = useState({
    name: '',
    privacy: '',
    owner: '',
    moderators: [],
    members: [],
    content: '',
    image: '',
  });

  const [allUsers, setAllUsers] = useState([]);

  useEffect(() => {
    // Fetch community data and update state
    axios.get(`/communities/${communityId}/info/`)
      .then(response => {
        setCommunityData(response.data);

        
        return axios.get('/users/');
      })
      .then(response => {
        setAllUsers(response.data.results);
      })
      .catch(error => {
        console.error('Error fetching community data', error);
      });
  }, [communityId]);

  const handleInputChange = (e) => {
    setCommunityData({
      ...communityData,
      [e.target.name]: e.target.value,
    });
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();

    // Send updated data to the backend
    axios.put(`/communities/${communityId}/edit/`, communityData)
      .then(response => {
        console.log('Community updated successfully', response.data);
        // Handle success, e.g., redirect or show a success message
      })
      .catch(error => {
        console.error('Error updating community', error);
        // Handle error, e.g., show an error message
      });
  };

  return (
    <form onSubmit={handleFormSubmit}>
      {/* Render form inputs based on your community model fields */}
      <label htmlFor="name">Community Name:</label>
      <input
        type="text"
        id="name"
        name="name"
        value={communityData.name}
        onChange={handleInputChange}
      />

      <label htmlFor="privacy">Privacy:</label>
      <select
        id="privacy"
        name="privacy"
        value={communityData.privacy}
        onChange={handleInputChange}
      >
        <option value="public">Public</option>
        <option value="private">Private</option>
        <option value="hidden">Hidden</option>
      </select>

      <label htmlFor="owner">Owner:</label>
      <input
        type="text"
        id="owner"
        name="owner"
        value={communityData.owner}
        onChange={handleInputChange}
      />

      <label htmlFor="moderators">Moderators:</label>
      {/* Assuming you want a multi-select for moderators */}
      <select
        id="moderators"
        name="moderators"
        multiple
        value={communityData.moderators}
        onChange={handleInputChange}
      >
        {/* Map over your moderators and create options */}
        {allUsers.map(user => (
          <option key={user.id} value={user.id}>
            {user.username}
          </option>
        ))}
      </select>

      <label htmlFor="members">Members:</label>
      {/* Assuming you want a multi-select for members */}
      <select
        id="members"
        name="members"
        multiple
        value={communityData.members}
        onChange={handleInputChange}
      >
        {/* Map over your members and create options */}
        {allUsers.map(user => (
          <option key={user.id} value={user.id}>
            {user.username}
          </option>
        ))}
      </select>

      <label htmlFor="content">Content:</label>
      <textarea
        id="content"
        name="content"
        value={communityData.content}
        onChange={handleInputChange}
      />

      <label htmlFor="image">Image URL:</label>
      <input
        type="text"
        id="image"
        name="image"
        value={communityData.image}
        onChange={handleInputChange}
      />


      <button type="submit">Save Changes</button>
    </form>
  );
};

export default EditCommunityForm;
