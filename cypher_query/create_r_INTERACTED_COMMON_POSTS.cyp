MATCH (u:User)
WITH COLLECT(u) AS ls_user
UNWIND ls_user AS user1
CALL {
    WITH user1
    MATCH (user1)-[r1:COMMENTED|SHARED|POSTED]->(post:Post)<-[r2:COMMENTED|SHARED|POSTED]-(user2:User WHERE user1.uid < user2.uid)
    WITH user1, user2, COLLECT(DISTINCT post) AS commonPosts
    WITH user1, user2, SIZE(commonPosts) AS numberOfCommonPosts
    WHERE numberOfCommonPosts > 1
    MERGE (user1)-[r:INTERACTED_COMMON_POSTS]-(user2)
    SET r.weight = numberOfCommonPosts
} IN TRANSACTIONS OF 1000 ROWS
