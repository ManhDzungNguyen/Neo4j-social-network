docker run \
    --name neo4j \
    -p 7475:7474 -p 7688:7687 \
    -d \
    -v $HOME/work/Neo4j-social-network/docker/neo4j/data:/data \
    -v $HOME/work/Neo4j-social-network/docker/neo4j/logs:/logs \
    -v $HOME/work/Neo4j-social-network/docker/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/work/Neo4j-social-network/docker/neo4j/plugins:/plugins \
    --env NEO4JLABS_PLUGINS='["apoc", "graph-data-science"]' \
    --env apoc.import.file.enabled=true \
    --env NEO4J_AUTH=neo4j/12345678 \
    neo4j:latest