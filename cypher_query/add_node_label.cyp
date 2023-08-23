// CONVERT NODE PROPERTY 'louvain_cid' TO LABEL
MATCH (u:User WHERE u.louvain_cid IS NOT NULL)
CALL apoc.create.addLabels( u, [ toString(u.louvain_cid) ] )
YIELD node
RETURN node;


// ADD LABEL FOR TOP 100 NODES HAVING HIGHEST BETWEENNESS CENTRALITY
MATCH (u:User WHERE u.global_betweenness IS NOT NULL) WITH u ORDER BY u.global_betweenness DESC LIMIT 50
CALL apoc.create.addLabels( u, [ 'TOP_BTW' ] )
YIELD node
RETURN node;


// ADD LABEL SEEDER_P (POSTED)
MATCH (p:Post)<-[r:COMMENTED|SHARED]-(:User)
WITH p, COUNT(r) AS no_r
WHERE no_r > 30
WITH COLLECT(DISTINCT p) AS hotPosts 
MATCH (u:User)-[r_p:POSTED]->(p:Post WHERE p in hotPosts)
WITH u, COUNT(r_p) AS no_r_p
WHERE no_r_p > 2
CALL apoc.create.addLabels( u, [ "SEEDER_P" ] )
YIELD node
RETURN node;


// ADD LABEL SEEDER_I (INTERACTED - COMMENTED und SHARED)
MATCH (u:User)-[r_i:COMMENTED|SHARED]->(p:Post)<-[r_p:POSTED]-(p_u:SEEDER_P)
WITH u, COUNT(r_i) AS no_r_i
WHERE no_r_i > 30
CALL apoc.create.addLabels( u, [ "SEEDER_I" ] )
YIELD node
RETURN node;