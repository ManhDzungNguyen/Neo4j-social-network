// show all node labels
CALL db.labels();

// get a list of node properties
MATCH (n:User)
RETURN DISTINCT keys(n), size(keys(n))
ORDER BY size(keys(n)) DESC 

// retrieve the visualization of the database schema
CALL db.schema.visualization()

// retrieve all possible properties of nodes
MATCH (u:User)
RETURN DISTINCT keys(u) AS all_properties

// get total number of nodes
MATCH (n)
RETURN count(n) AS no_N

// get total number of Relationships
MATCH ()-[r]->()
RETURN count(r) AS no_R

// show all indexes
SHOW INDEXES

// show all gds.graph
CALL gds.graph.list()
YIELD graphName
RETURN graphName;

//show many data
MATCH (n) WITH count(n) AS no_N
MATCH ()-[r]->() WITH no_N, count(r) AS no_R
MATCH (u1:User)-[r:COMMENTED_COMMON_POSTS]->(u2:User)
WITH no_N, no_R, COUNT(r) AS no_CCP, COLLECT( DISTINCT u1) + COLLECT( DISTINCT u2) AS allUsers
WITH no_N, no_R, no_CCP, SIZE(allUsers) AS no_Users_w_CCP
MATCH (u1:User)-[r:INTERACTED_COMMON_POSTS]->(u2:User)
WITH no_N, no_R, no_CCP, no_Users_w_CCP, COUNT(r) AS no_ICP, COLLECT( DISTINCT u1) + COLLECT( DISTINCT u2) AS allUsers
WITH no_N, no_R, no_CCP, no_Users_w_CCP, no_ICP, SIZE(allUsers) AS no_Users_w_ICP    
RETURN no_N, no_R, no_CCP, no_Users_w_CCP, no_ICP, no_Users_w_ICP
