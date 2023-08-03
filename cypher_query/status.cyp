// retrieves the visualization of the database schema
CALL db.schema.visualization()

// get total number of Nodes
MATCH (n)
RETURN count(n) AS numberOfNodes

// get total number of Relationships
MATCH ()-[r]->()
RETURN count(r) AS numberOfRelationships

