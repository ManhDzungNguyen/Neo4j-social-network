// CONVERT PROPERTY louvain_cid TO LABEL
MATCH (u:User WHERE u.louvain_cid IS NOT NULL)
CALL apoc.create.addLabels( u, [ toString(u.louvain_cid) ] )
YIELD node
RETURN node;

// ADD LABEL FOR TOP 100 NODES HAVING HIGHEST BETWEENNESS CENTRALITY
MATCH (u:User WHERE u.global_betweenness IS NOT NULL) WITH u ORDER BY u.global_betweenness DESC LIMIT 100
CALL apoc.create.addLabels( u, [ 'TOP_BTW' ] )
YIELD node
RETURN node;

// VISUALIZE
MATCH (u WHERE u.louvain_cid = 30728 OR u.louvain_cid = 77862) 
WITH u ORDER BY u.global_pagerank DESC LIMIT 200
WITH COLLECT(u) AS topUsers
MATCH (u1 WHERE u1 IN topUsers)-[r:INTERACTED_COMMON_POSTS WHERE r.weight > 3]->(u2 WHERE u2 IN topUsers) RETURN u1, r, u2

// VISUALIZE TOP 4 COMMUNITIES
MATCH (u WHERE u.louvain_cid = 30728 OR u.louvain_cid = 77862 OR u.louvain_cid = 61487 OR u.louvain_cid = 11918) 
WITH u ORDER BY u.global_pagerank DESC LIMIT 300
WITH COLLECT(u) AS topUsers
MATCH (u1 WHERE u1 IN topUsers)-[r:INTERACTED_COMMON_POSTS WHERE r.weight > 8]->(u2 WHERE u2 IN topUsers) RETURN u1, r, u2