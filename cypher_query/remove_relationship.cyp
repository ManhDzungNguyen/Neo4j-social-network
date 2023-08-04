call apoc.periodic.iterate('MATCH p = (:person)-[r:{relationship}]->(:person) return r', 'DETACH DELETE r', {{batchSize:1000}})
yield batches, total return batches, total