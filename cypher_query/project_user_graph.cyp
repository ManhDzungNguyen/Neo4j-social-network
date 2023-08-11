CALL gds.graph.project(
'user-subgraph',
['User'],
{
  COMMENTED_COMMON_POSTS: {
    type: 'COMMENTED_COMMON_POSTS',
    orientation: 'UNDIRECTED',
    properties: {
      weight:{
        property: 'weight'
      }
    }
  }
}
)


CALL gds.graph.project(
  'user_icp',
  ['User'],
  {INTERACTED_COMMON_POSTS: { properties: 'weight'}},
  {
    nodeProperties: ['louvainCommunityID']
  }
)

CALL gds.beta.graph.project.subgraph(
  'user_c69236',
  'user_icp',
  'n.louvainCommunityID = 69236',
  '*'
)
YIELD graphName, fromGraphName, nodeCount, relationshipCount