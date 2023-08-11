// CREATE projected graph
CALL gds.graph.project(
'user-icp',
['User'],
{ INTERACTED_COMMON_POSTS: { properties: 'weight' }}
);

// CALCULATE USER GLOBAL PAGERANK
CALL gds.pageRank.write('user-icp', {
  maxIterations: 20,
  dampingFactor: 0.85,
  writeProperty: 'global_pagerank'
  })
  YIELD nodePropertiesWritten, ranIterations;
  
// APPLY COMMUNITY DETECTION ALGORITHM
CALL gds.louvain.write('user-icp', {
  writeProperty: 'louvain_cid',
  minCommunitySize: 5,
  relationshipWeightProperty: 'weight',
  maxLevels: 10
  })
  YIELD communityCount, modularity, modularities;
    
// (Optional)
CALL gds.labelPropagation.write('user-icp', {
  writeProperty: 'lpa_cid',
  minCommunitySize: 5,
  relationshipWeightProperty: 'weight',
  maxIterations: 10
  })
  YIELD communityCount, ranIterations, didConverge;
      
// GET TOP K COMMUNITIES HAVING THE HIGHEST NUMBER OF NODES:
MATCH (u:User WHERE u.louvain_cid IS NOT NULL)
WITH u.louvain_cid AS community, COUNT(u) AS userCount
RETURN community, userCount
ORDER BY userCount DESC
LIMIT 20