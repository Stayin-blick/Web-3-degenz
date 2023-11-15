// page with coomunity post comment and likes 

// Import other components as needed
import React, { useEffect, useState } from "react";

import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Container from "react-bootstrap/Container";

import appStyles from "../../App.module.css";
import { useParams } from "react-router";
import { axiosReq } from "../../api/axiosDefaults";
import Post from "./Post";
import Comment from "../comments/Comment";
import CommunityPost from "../../pages/communities/CommunitiesPage";
import CommentCreateForm from "../comments/CommentCreateForm";
import { useCurrentUser } from "../../contexts/CurrentUserContext";

import InfiniteScroll from "react-infinite-scroll-component";
import Asset from "../../components/Asset";
import { fetchMoreData } from "../../utils/utils";


function CommunityPostPage() {
    const { id } = useParams();
    const [post, setPost] = useState({ results: [] });
    const [comments, setComments] = useState({ results: [] });
    const [loading, setLoading] = useState(true);
    const currentUser = useCurrentUser();
    const profile_image = currentUser?.profile_image;
  
    useEffect(() => {
      const fetchData = async () => {
        try {
          const [{ data: post }, { data: comments }] = await Promise.all([
            axiosReq.get(`/posts/${id}`),
            axiosReq.get(`/comments/?post=${id}`),
          ]);
          setPost({ results: [post] });
          setComments(comments);
        } catch (error) {
          console.error('Error fetching data:', error);
          // Handle the error (e.g., display an error message to the user)
        } finally {
          setLoading(false);
        }
      };
  
      fetchData();
    }, [id]);
  
    return (
      <Row className="h-100">
        <Col className="py-2 p-0 p-lg-2" lg={8}>
          {loading ? (
            <Container className={appStyles.Content}>
              <Asset spinner />
            </Container>
          ) : (
            <>
              <CommunityPost {...post.results[0]} setPosts={setPost} postPage />
              <Container className={appStyles.Content}>
                {currentUser && (
                  <CommentCreateForm
                    profile_id={currentUser.profile_id}
                    profileImage={profile_image}
                    post={id}
                    setPost={setPost}
                    setComments={setComments}
                  />
                )}
                {comments.results.length > 0 ? (
                  <InfiniteScroll
                    children={comments.results.map((comment) => (
                      <Comment
                        key={comment.id}
                        {...comment}
                        setPost={setPost}
                        setComments={setComments}
                      />
                    ))}
                    dataLength={comments.results.length}
                    loader={<Asset spinner />}
                    hasMore={!!comments.next}
                    next={() => fetchMoreData(comments, setComments)}
                  />
                ) : (
                  <span>
                    {currentUser ? "No comments yet, be the first" : "No comments yet"}
                  </span>
                )}
              </Container>
            </>
          )}
        </Col>
      </Row>
    );
  }
  
  export default CommunityPostPage;
  