import React, { useEffect, useState } from "react";
import { Row, Col, Container } from "react-bootstrap";
import InfiniteScroll from "react-infinite-scroll-component";
import { axiosReq } from "../../api/axiosDefaults";
import { fetchMoreData } from "../../utils/utils";
import Asset from "../../components/Asset";
import NoResults from "../../assests/no-results.png";
import CommunityPost from "./CommunitiesPost";
import appStyles from "../../App.module.css";
// import styles from "../../styles/Communities.module.css";

function CommunityPostsPage( { message, filter = "", pk } ) {
    const [posts, setPosts] = useState({ results: [] });
    const [hasLoaded, setHasLoaded] = useState(false);

  useEffect(() => {
    const fetchCommunityPosts = async () => {
      try {
        const response = await axiosReq.get(`/communities/${pk}/posts/`);
        setPosts(response.data);
        console.log('fetching post', response.data)
        setHasLoaded(true);
      } catch (error) {
        console.error('Failed to fetch community posts.', error);
        setHasLoaded(true);
      }
    };

    fetchCommunityPosts();
  }, [pk]);

  
  return (
    <Row className="h-100">
      <Col>
        {hasLoaded ? (
          <>
            {posts.results.length ? (
              <InfiniteScroll
                children={posts.results.map((post) => (
                  <CommunityPost key={post.id} {...post} setPosts={setPosts} />
                ))}
                dataLength={posts.results.length}
                loader={<Asset spinner />}
                hasMore={!!posts.next}
                next={() => fetchMoreData(posts, setPosts)}
              />
            ) : (
              <Container className={appStyles.Content}>
                <Asset src={NoResults} message={message} />
              </Container>
            )}
          </>
        ) : (
          <Container className={appStyles.Content}>
            <Asset spinner />
          </Container>
        )}
      </Col>
    </Row>
  );
}

export default CommunityPostsPage;
