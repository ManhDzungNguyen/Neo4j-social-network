// VISUALIZE TOP 4 COMMUNITIES
MATCH (u:`1197`|`6071`|`17497`)
WITH u ORDER BY u.global_pagerank DESC LIMIT 100
WITH COLLECT(u) AS topUsers
MATCH (u1 WHERE u1 IN topUsers)-[r:INTERACTED_COMMON_POSTS WHERE r.weight > 15]->(u2 WHERE u2 IN topUsers) RETURN u1, r, u2


// VISUALIZE INTERACTION BETWEEN POSTED SEEDERS AND INTERACTED SEEDERS
// If DB has labels SEEDER_P und SEEDER_I
MATCH (i_u:SEEDER_I)-[r:INTERACTED_COMMON_POSTS]-(p_u:SEEDER_P)
RETURN i_u, r, p_u


// If DB doesn't have labels SEEDER_P und SEEDER_I
MATCH (p:Post)<-[r:COMMENTED|SHARED]-(:User)
WITH p, COUNT(r) AS no_r
WHERE no_r > 30
WITH COLLECT(DISTINCT p) AS hotPosts 
MATCH (u:User)-[r_p:POSTED]->(p:Post WHERE p in hotPosts)
WITH u, COUNT(r_p) AS no_r_p
WHERE no_r_p > 2
WITH COLLECT(u) AS p_Seeders
MATCH (u:User)-[r_i:COMMENTED|SHARED]->(p:Post)<-[r_p:POSTED]-(p_u:User WHERE p_u IN p_Seeders)
WITH u, COUNT(r_i) AS no_r_i, p_Seeders
WHERE no_r_i > 30
WITH COLLECT(u) AS cs_Seeders, p_Seeders
MATCH (cs_u:User WHERE cs_u IN cs_Seeders)-[r:INTERACTED_COMMON_POSTS]-(p_u:User WHERE p_u IN p_Seeders)
RETURN cs_u, r, p_u


// GET HIDDEN MUTUAL FIRENDS OF TanThai UND TienThai
MATCH (u1:User WHERE u1.uid='100004483337392')-[r1:INTERACTED_COMMON_POSTS]-(u:User)-[r2:INTERACTED_COMMON_POSTS]-(u2:User WHERE u2.uid='100003397443390')
WHERE r1.weight > 5 AND r2.weight > 5
RETURN u.uid, r1.weight AS w_TanThai, r2.weight AS w_TienThai
ORDER BY w_TanThai DESC