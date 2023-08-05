CALL apoc.periodic.iterate(
    'MATCH (user1:User)-[r1:COMMENTED]->(post:Post)<-[r2:COMMENTED WHERE duration.between(date(r1.first_cmt_time), date(r2.first_cmt_time)).days < 3]-(user2:User WHERE user1.uid < user2.uid) RETURN user1, user2, post',
    'WITH user1, user2, COLLECT(DISTINCT post) AS commonPosts WITH user1, user2, SIZE(commonPosts) AS numberOfCommonPosts WHERE numberOfCommonPosts > 1 MERGE (user1)-[r:COMMENTED_COMMON_POSTS]-(user2) SET r.weight = numberOfCommonPosts',
    {batchSize:1000, iterateList:true, parallel:true}
)
YIELD batches, total
RETURN batches, total