// use the Louvain algorithm to perform community detection
CALL gds.louvain.stream('user-subgraph')
YIELD nodeId, communityId
WITH communityId, COUNT(nodeId) AS nodeCount
RETURN communityId, nodeCount
ORDER BY nodeCount DESC
LIMIT 10;