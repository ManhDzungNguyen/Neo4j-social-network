// retrieve the number of relationships between users who have commented on common posts
// and total users involved in those relationships.
MATCH (u1:User)-[r:COMMENTED_COMMON_POSTS]->(u2:User)
WITH COUNT(r) AS numberOfRelationships, COLLECT( DISTINCT u1) + COLLECT( DISTINCT u2) AS allUsers
RETURN numberOfRelationships, SIZE(allUsers) AS numberOfUsers
