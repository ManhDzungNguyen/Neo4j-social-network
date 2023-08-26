MATCH (u:User)
WITH COLLECT(u) AS ls_user
UNWIND ls_user AS user1
CALL {
    WITH user1
    MATCH (user1)-[r1:SHARED]->(post:Post)<-[r2:SHARED]-(user2:User WHERE user1.uid < user2.uid)
    WITH user1, user2, COLLECT(DISTINCT post) AS commonPosts
    WITH user1, user2, SIZE(commonPosts) AS numberOfCommonPosts
    WHERE numberOfCommonPosts > 1
    MERGE (user1)-[r:SHARED_COMMON_POSTS_V2]-(user2)
    SET r.weight = numberOfCommonPosts
} IN TRANSACTIONS OF 1000 ROWS