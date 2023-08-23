// PROJECT GRAPH WITH NODES PROPERTIES
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
{ nodeProperties: ['global_pagerank'] } // Optional
);


// PROJECT SUBGRAPH
CALL gds.beta.graph.project.subgraph(
  'user-icp-pagerank-01501',
  'user-icp',
  'n.global_pagerank > 0.1501',
  '*'
)
YIELD graphName, fromGraphName, nodeCount, relationshipCount