// PROJECT GRAPH
CALL gds.graph.project(
'user-icp',
['User'],
{
  INTERACTED_COMMON_POSTS: {
    type: 'INTERACTED_COMMON_POSTS',
    orientation: 'UNDIRECTED',
    properties: {
      weight: {
        property: 'weight'
      }
    }
  }
}
);


// CALCULATE USER GLOBAL PAGERANK
CALL gds.pageRank.write('user-icp', {
  maxIterations: 20,
  dampingFactor: 0.85,
  writeProperty: 'global_pagerank'
})
YIELD nodePropertiesWritten, ranIterations;


// CALCULATE USER WEIGHTED GLOBAL PAGERANK
CALL gds.pageRank.write('user-icp', {
  maxIterations: 20,
  dampingFactor: 0.85,
  relationshipWeightProperty: 'weight',
  writeProperty: 'global_weighted_pagerank'
})
YIELD nodePropertiesWritten, ranIterations;


// CALCULATE USER GLOBAL BETWEENNESS (RUN IN PYTHON !!!)
CALL gds.betweenness.write('user-icp', {
  writeProperty: 'global_betweenness'
})
YIELD nodePropertiesWritten, computeMillis

  
// APPLY COMMUNITY DETECTION LOUVAIN ALGORITHM
CALL gds.louvain.write('user-icp', {
  writeProperty: 'louvain_cid',
  minCommunitySize: 5,
  relationshipWeightProperty: 'weight',
  maxLevels: 10
})
YIELD communityCount, modularity, modularities;

// // (Optional) CONVERT NODE PROPERTY 'louvain_cid' TO LABEL
// MATCH (u:User WHERE u.louvain_cid IS NOT NULL)
// CALL apoc.create.addLabels( u, [ toString(u.louvain_cid) ] )
// YIELD node
// RETURN node;


// // (Optional) APPLY COMMUNITY DETECTION LPA ALGORITHM
// CALL gds.labelPropagation.write('user-icp', {
//   writeProperty: 'lpa_cid',
//   minCommunitySize: 5,
//   relationshipWeightProperty: 'weight',
//   maxIterations: 10
//   })
//   YIELD communityCount, ranIterations, didConverge;


// GET TOP K COMMUNITIES HAVING THE HIGHEST NUMBER OF NODES
MATCH (u:User WHERE u.louvain_cid IS NOT NULL)
WITH u.louvain_cid AS community, COUNT(u) AS userCount
RETURN community, userCount
ORDER BY userCount DESC
LIMIT 20


// REVIEW A COMMUNITY
MATCH (u:User WHERE u.louvain_cid = 4453) // MATCH (u:`4453`)
WITH u ORDER BY u.global_pagerank DESC LIMIT 200
WITH COLLECT(u) AS topUsers
MATCH (u1 WHERE u1 IN topUsers)-[r:INTERACTED_COMMON_POSTS WHERE r.weight > 4]->(u2 WHERE u2 IN topUsers) RETURN u1, r, u2


// VISUALIZE INTERACTION BETWEEN POSTED SEEDERS AND INTERACTED SEEDERS
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

// // (Optional) ADD LABELS FOR POSTED SEEDERS AND INTERACTED SEEDERS
// // Add label SEEDER_P (POSTED)
// MATCH (p:Post)<-[r:COMMENTED|SHARED]-(:User)
// WITH p, COUNT(r) AS no_r
// WHERE no_r > 30
// WITH COLLECT(DISTINCT p) AS hotPosts 
// MATCH (u:User)-[r_p:POSTED]->(p:Post WHERE p in hotPosts)
// WITH u, COUNT(r_p) AS no_r_p
// WHERE no_r_p > 2
// CALL apoc.create.addLabels( u, [ "SEEDER_P" ] )
// YIELD node
// RETURN node;

// // Add label SEEDER_I (INTERACTED - COMMENTED und SHARED)
// MATCH (u:User)-[r_i:COMMENTED|SHARED]->(p:Post)<-[r_p:POSTED]-(p_u:SEEDER_P)
// WITH u, COUNT(r_i) AS no_r_i
// WHERE no_r_i > 30
// CALL apoc.create.addLabels( u, [ "SEEDER_I" ] )
// YIELD node
// RETURN node;