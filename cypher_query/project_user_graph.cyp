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