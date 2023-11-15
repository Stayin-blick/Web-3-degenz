import React, { createContext, useContext, useState } from "react";

const CommunityDataContext = createContext();
const SetCommunityDataContext = createContext();

export const useCommunityData = () => useContext(CommunityDataContext);
export const useSetCommunityData = () => useContext(SetCommunityDataContext);

export const CommunityDataProvider = ({ children }) => {
  const [communityData, setCommunityData] = useState({
    communityInfo: null,
    invites: [], 
    posts: [],
  });

  const setCommunityInfo = (communityInfo) => {
    setCommunityData((prevData) => ({
      ...prevData,
      communityInfo,
    }));
  };

  const acceptInvite = (inviteId) => {
    // Implement the logic to accept an invite
    // Update invites data in communityData
    setCommunityData((prevData) => ({
      ...prevData,
      invites: prevData.invites.filter((invite) => invite.id !== inviteId),
    }));
  };

  const fetchCommunityPosts = (communityId) => {
    // Implement the logic to fetch community posts
    // Update posts data in communityData
    const fetchedPosts = []; // Replace with actual fetching logic
    setCommunityData((prevData) => ({
      ...prevData,
      posts: fetchedPosts,
    }));
  };

  const createPost = (postData) => {
    // Implement the logic to create a new post
    // Update posts data in communityData
    setCommunityData((prevData) => ({
      ...prevData,
      posts: [...prevData.posts, postData],
    }));
  };

  return (
    <CommunityDataContext.Provider
      value={{ ...communityData, setCommunityInfo, acceptInvite, fetchCommunityPosts, createPost }}
    >
      <SetCommunityDataContext.Provider value={setCommunityData}>
        {children}
      </SetCommunityDataContext.Provider>
    </CommunityDataContext.Provider>
  );
};
