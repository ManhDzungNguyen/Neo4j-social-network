// retrieves the visualization of the database schema
CALL db.schema.visualization()

// get total number of Nodes
MATCH (n)
RETURN count(n) AS numberOfNodes

// get total number of Relationships
MATCH ()-[r]->()
RETURN count(r) AS numberOfRelationships

// show all indexes
SHOW INDEXES

// show all gds.graph
CALL gds.graph.list()
YIELD graphName
RETURN graphName;