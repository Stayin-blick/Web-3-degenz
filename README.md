Web 3 Degenz - Backend Overview
Web 3 Degenz is a social platform designed to connect users, facilitate online interactions, and build relationships within a decentralized web environment. The backend infrastructure of this platform is organized into several Django apps, each handling specific functionalities to ensure a scalable and maintainable architecture.

App Overview
Comments App
Models

Comment: Represents a comment on a post, related to User and Post models.
Serializers

CommentSerializer: Serializes Comment models for list views.
CommentDetailSerializer: Extends CommentSerializer for detail views.
Views

CommentList: Lists all comments and handles comment creation.
CommentDetail: Manages retrieving, updating, and deleting a comment if the user is the owner.
URLs

Patterns defined for comment-related views.
Permissions and Filters

Permissions set to control access, allowing read-only access for unauthenticated users.
Filtering applied to CommentList based on the associated post.
Community App
Models

Community: Represents a community with fields such as owner, moderators, members, content, image, and privacy.
CommunityPost: Represents a post within a community with fields like owner, community, title, and content.
Serializers

CommunitySerializer: Serializes the Community model.
CommunityPostSerializer: Serializes the CommunityPost model.
Views

CommunityListCreateView: Allows listing and creating communities.
CommunityDetailView: Manages retrieving, updating, and deleting a specific community.
CommunityInfoView: Provides information about a community.
CommunityPostListCreateView: Allows listing and creating community posts.
CommunityPostDetailView: Manages retrieving, updating, and deleting a specific community post.
UserPostDeleteView: Allows deleting a community post if the user is the owner.
URLs

Patterns defined for community-related views.
Permissions and Filters

Permissions set to control access, allowing read-only access for unauthenticated users and restricting certain operations to community owners, moderators, or members.
Followers App
Models

Follower: Represents a follower-followed relationship.
Serializers

FollowerSerializer: Serializes the Follower model.
Views

FollowerList: Lists all followers and handles follower creation.
FollowerDetail: Manages retrieving and unfollowing a user.
URLs

Patterns defined for follower-related views.
Permissions and Filters

Permissions set to control access, allowing read-only access for unauthenticated users.
Unique constraints handled in the create method.
Invitation App
Models

Invitation: Represents an invitation to join a community.
Serializers

InvitationListSerializer: Serializes invitations for listing.
InvitationSendSerializer: Serializes invitations for sending.
InvitationAcceptSerializer: Serializes invitations for accepting.
Views

InvitationListView: Lists pending invitations for the authenticated user.
InvitationCreateView: Creates and sends a new invitation.
InvitationAcceptView: Accepts or declines an invitation.
URLs

Patterns defined for invitation-related views.
Post App
Models

Post: Represents a post created by a user in a community.
Serializers

PostSerializer: Serializes the post model.
Views

PostList: Lists all posts or creates a new post if authenticated.
PostDetail: Retrieves, updates, or deletes a post if the user owns it.
CommunityPostList: Lists posts belonging to a specific community for community members.
CommunityPostDetail: Manages retrieving, updating, or deleting a post in a community if the user owns it.
URLs

Patterns defined for post-related views.
Profile App
Models

Profile: Represents a user profile associated with a Django User.
Serializers

ProfileSerializer: Serializes the profile model.
Views

ProfileList: Lists all profiles.
ProfileDetail: Retrieves or updates a profile if the authenticated user is the owner.
Permissions

Read-only access for unauthenticated users.
Authenticated users can view and update their own profiles.
Installation and Setup
Clone the repository.
Create and activate a virtual environment.
Install dependencies using pip install -r requirements.txt.
Apply migrations with python manage.py migrate.
Create a superuser with python manage.py createsuperuser for Django admin access.
Run the development server with python manage.py runserver.
Now, the backend of Web 3 Degenz is set up and ready for use. Additionally, the frontend can be initiated by navigating to the "frontend" directory and running npm start.

##Frontend Design Philosophy and Context Utilization
Design Philosophy
In crafting the frontend of Web 3 Degenz, a key consideration was the pursuit of simplistic clarity. This principle guided the choice of using light colors, creating an interface that is visually clean and easy to navigate. The design aimed to prioritize user experience through a minimalist and user-friendly approach.

Context Utilization
The implementation of context in the frontend code serves as a crucial organizational and state management tool. Context provides a way to share values, such as the current user's data, across components without the need to pass props manually through each level of the component tree. The provided code showcases the utilization of React's createContext, useContext, and useEffect to manage the current user's state.

Context Implementation
CurrentUserContext and SetCurrentUserContext
CurrentUserContext is created to hold the current user's data.
SetCurrentUserContext is created to hold a function that updates the current user's data.
Custom Hooks: useCurrentUser and useSetCurrentUser
useCurrentUser: Retrieves the current user's data from the context.
useSetCurrentUser: Retrieves the function to update the current user's data from the context.
CurrentUserProvider
Wraps the application with the CurrentUserContext.Provider and SetCurrentUserContext.Provider.
Fetches the current user's data on component mount and updates the context using setCurrentUser.
Axios Interceptors
Utilizes Axios interceptors to handle token refresh and authentication.
The axiosReq interceptor handles requests, while the axiosRes interceptor handles responses.
Interceptors are essential for managing token expiration and refreshing, ensuring seamless user authentication.
handleMount and useEffect
handleMount: Function to fetch the current user's data from the backend on component mount.
useEffect: Invokes handleMount on component mount, ensuring the current user's data is retrieved and set.
Memoization
useMemo is used to memoize the configuration of Axios interceptors.
Memoization optimizes performance by preventing unnecessary re-creation of interceptor functions.
Navigation and State Management
Leverages history from React Router to navigate users to the sign-in page if token refresh fails.
Manages the current user's state with setCurrentUser, ensuring smooth transitions between authentication states.
Component Interaction - Send Invitation
The context-based state management simplifies the process of handling invitations across components. When sending an invitation:

Invitation Component: Utilizes the useSetCurrentUser hook to update the current user's data upon sending an invitation.

In summary, the use of context in the frontend provides a clean and efficient way to manage the current user's state and facilitates seamless interactions, such as sending invitations, across different components.

Manual Testing: Admin Panel and Test Scenarios
Admin Panel Overview
The admin panel in Django provides a powerful interface for managing and inspecting the application's data. Manual testing in the admin panel allows for a comprehensive check of various functionalities and ensures that the backend is functioning as expected. Let's walk through creating multiple test scenarios for posts, communities, followers, likes, etc.

1. Test Posts
Objective: Verify the creation, update, and deletion of posts.

Steps:

Log in to the Django admin panel.
Navigate to the "Posts" section.
Create a new post with dummy content.
Edit the post, modifying the content or title.
Delete the post.
Expected Outcome: Successful creation, update, and deletion of posts.

Screenshots:

![Screenshot 2023-11-15 at 03 34 15](https://github.com/Stayin-blick/Web-3-degenz/assets/109948932/c6f663da-6a1d-4449-a484-bbb15f2ff511)
![Screenshot 2023-11-15 at 03 35 23](https://github.com/Stayin-blick/Web-3-degenz/assets/109948932/23ef9fff-fe02-42a9-9d13-4c69bdd8258e)
![Screenshot 2023-11-15 at 03 36 11](https://github.com/Stayin-blick/Web-3-degenz/assets/109948932/f790e18e-63fb-4492-9aa5-f6efae8e1a33)


2. Test Likes
Objective: Verify the creation and deletion of likes on posts.

Steps:

Navigate to the "Likes" section.
Create a new like for a post.
Verify that the like is associated with the correct post.
Delete the like.
Expected Outcome: Successful creation and deletion of likes.

Screenshots:

![Screenshot 2023-11-15 at 03 37 30](https://github.com/Stayin-blick/Web-3-degenz/assets/109948932/09a3c45a-28a2-4315-b55a-79a3fc3ddd92)
![Screenshot 2023-11-15 at 03 38 56](https://github.com/Stayin-blick/Web-3-degenz/assets/109948932/ead1877b-4461-421e-ab32-62fdda4ade97)

5. Test User Profiles
Objective: Verify the creation and update of user profiles.

Steps:

Navigate to the "Profiles" section.
Create a new user profile.
Edit the user profile details.
Verify that the changes are reflected in the profile.
Expected Outcome: Successful creation and update of user profiles.

Screenshots:
![Screenshot 2023-11-15 at 03 39 33](https://github.com/Stayin-blick/Web-3-degenz/assets/109948932/254ef5e1-ed7c-46b4-9334-83ccf940f606)

Bugs:

issues due to too many connections to database, this was resolved by api calls moved away from conponents and props passed to the component

issue between local and deployed site, deployed site is behind 

Conclusion
By manually testing these scenarios in the Django admin panel, you can ensure that the backend functionalities are working as expected. Take screenshots at each step to document the testing process and results for future reference.









