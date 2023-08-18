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

// CALCULATE USER GLOBAL BETWEENNESS (RUN IN PYTHON !!!)
CALL gds.betweenness.write('user-icp', {
  writeProperty: 'global_betweenness'
})
YIELD nodePropertiesWritten, computeMillis

// CALL gds.betweenness.write('user-icp', {
//   writeProperty: 'global_betweenness_samplingsize100',
//   samplingSize: 100, 
//   samplingSeed: 0
// })
// YIELD nodePropertiesWritten, computeMillis


// // PROJECT GRAPH WITH NODES' PROPERTIES
// CALL gds.graph.project(
// 'user-icp-pagerank',
// ['User'],
// { INTERACTED_COMMON_POSTS: { properties: 'weight' }},
// { nodeProperties: ['global_pagerank'] }
// );

// // PROJECT SUBGRAPH
// CALL gds.beta.graph.project.subgraph(
//   'user-icp-pagerank-01501',
//   'user-icp-pagerank',
//   'n.global_pagerank > 0.1501',
//   '*'
// )
// YIELD graphName, fromGraphName, nodeCount, relationshipCount

  
// APPLY COMMUNITY DETECTION ALGORITHM
CALL gds.louvain.write('user-icp', {
  writeProperty: 'louvain_cid',
  minCommunitySize: 5,
  relationshipWeightProperty: 'weight',
  maxLevels: 10
})
YIELD communityCount, modularity, modularities;
    
// // (Optional)
// CALL gds.labelPropagation.write('user-icp', {
//   writeProperty: 'lpa_cid',
//   minCommunitySize: 5,
//   relationshipWeightProperty: 'weight',
//   maxIterations: 10
//   })
//   YIELD communityCount, ranIterations, didConverge;
      
// GET TOP K COMMUNITIES HAVING THE HIGHEST NUMBER OF NODES:
MATCH (u:User WHERE u.louvain_cid IS NOT NULL)
WITH u.louvain_cid AS community, COUNT(u) AS userCount
RETURN community, userCount
ORDER BY userCount DESC
LIMIT 20


MATCH (u:User WHERE u.louvain_cid = 4453) 
WITH u ORDER BY u.global_pagerank DESC LIMIT 200
WITH COLLECT(u) AS topUsers
MATCH (u1 WHERE u1 IN topUsers)-[r:INTERACTED_COMMON_POSTS WHERE r.weight > 4]->(u2 WHERE u2 IN topUsers) RETURN u1, r, u2