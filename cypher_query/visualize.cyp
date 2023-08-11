//
MATCH (u:User)
WHERE u.degree_centrality IS NOT NULL
WITH u
ORDER BY u.degree_centrality DESC
LIMIT 10
WITH COLLECT(u) AS top_users

MATCH (u1:User WHERE u1 IN top_users)-[r:INTERACTED_COMMON_POSTS]->(u2:User WHERE u2 IN top_users)
RETURN u1, r, u2


//
MATCH (u:User WHERE u.louvainCommunityID IS NOT NULL)
RETURN u.uid, u.louvainCommunityID, u.pagerank
ORDER BY u.pagerank DESC
LIMIT 20
