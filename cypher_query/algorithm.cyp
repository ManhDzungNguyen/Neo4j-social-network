// use the Louvain algorithm to perform community detection
CALL gds.louvain.stream('user-subgraph')
YIELD nodeId, communityId
WITH communityId, COUNT(nodeId) AS nodeCount
RETURN communityId, nodeCount
ORDER BY nodeCount DESC
LIMIT 10;


// PageRank with Weight
CALL gds.pageRank.stream('user-subgraph', {
  maxIterations: 20,
  dampingFactor: 0.85,
  relationshipWeightProperty: 'weight'
})
YIELD nodeId, score
RETURN nodeId, score
  ORDER BY score DESC;


CALL gds.pageRank.write('user-subgraph', {
  maxIterations: 20,
  dampingFactor: 0.85,
  writeProperty: 'pagerank'
})
YIELD nodePropertiesWritten, ranIterations