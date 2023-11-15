import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { Container, Row, Col} from 'react-bootstrap';
import { CommunityInfoBadge } from '../../components/CommunityInfoBadge';
import SendInvitationForm from '../../components/SendInvitationForm';
import CommunityPostCreate from '../../components/CommunityPostCreate';
import CommunityPostsPage from './CommunitiesPostsPage';

const CommunityPage = () => {
  const [preselectedCommunity, setPreselectedCommunity] = useState(null);
  const [postFormData, setPostFormData] = useState({
    title: '',
    content: '',
  });
  const { pk } = useParams();

  useEffect(() => {
    const fetchCommunityDetails = async () => {
      try {
        const response = await axios.get(`/communities/${pk}/info/`);
        setPreselectedCommunity(response.data);
      } catch (error) {
        console.error('Failed to fetch community details.', error);
      }
    };

    if (pk) {
      fetchCommunityDetails();
    }
  }, [pk]);

  const handlePostChange = (e) => {
    const { name, value } = e.target;
    setPostFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handlePostSubmit = async (e) => {
    e.preventDefault();

    try {
      await axios.post(`/communities/${pk}/posts/`, postFormData);

      // You may want to update the state or perform any other actions upon successful post creation.
      setPostFormData({
        title: '',
        content: '',
      });
    } catch (error) {
      console.error('Error Creating Post:', error);
      // Handle the error, show a message, etc.
    }
  };

  return (
    <Container fluid>
      <Row>
        {/* Left Column - Community Info */}
        <Col xs={3}>
          <div>
          <h1>Community Info:</h1>
            <CommunityInfoBadge />
          </div>
        </Col>
        {/* Middle Column */}
        <Col xs={6}>
          {/* Row 1: Post Create Form */}
          <Row className="mb-4">
            <Col>
              <h1>Create Post:</h1>
                <CommunityPostCreate pk={pk} />
            </Col>
          </Row>

          {/* Row 2: Display Community Posts */}
          <Row>
            <Col>
              <h1>Community Feed:</h1>
              {/* Display community posts here */}
              <CommunityPostsPage pk={pk}/>
            </Col>
          </Row>
        </Col>

        {/* Right Column - Send Invitation Form */}
        <Col xs={3}>
        <h1>Invite</h1>
          <SendInvitationForm preselectedCommunity={preselectedCommunity} />
        </Col>
      </Row>
    </Container>
  );
};

export default CommunityPage;
