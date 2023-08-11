CALL apoc.periodic.iterate(
    'MATCH (u:User WHERE u.pagerank IS NOT NULL) RETURN u',
    'REMOVE u.pagerank',
    {batchSize:1000}
)
YIELD batches, total
RETURN batches, total