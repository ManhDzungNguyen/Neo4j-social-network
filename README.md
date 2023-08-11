# Neo4j-social-network

1. import social data
2. create relationship between users
3. project graph
4. calculate User nodes PageRank


# Neo4j basics

## Installation and configuration

### Install Neo4j on Ubuntu 20.04

[How To Install and Configure Neo4j on Ubuntu 20.04  | DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-neo4j-on-ubuntu-20-04)

### Configure Neo4j for Remote Access

```bash
sudo nano /etc/neo4j/neo4j.conf
```

**Uncomment and edit these lines:**

- Memory Settings:
    - `server.memory.heap.initial_size=1g`
    - `server.memory.heap.max_size=6g`
    - `server.memory.pagecache.size=3g`
    - `dbms.memory.transaction.total.max=4g`
- Network connector configuration:
    - `server.default_listen_address=10.9.3.209` (accept non-local connections)
- Miscellaneous configuration
    - `dbms.security.allow_csv_import_from_file_urls=true`
    - `dbms.security.procedures.unrestricted=gds.*,apoc.*`
    - `dbms.security.procedures.allowlist=apoc.coll.*,apoc.load.*,gds.*,apoc.*`
- Other Neo4j system properties
    - `apoc.import.file.enabled=true`

## Extened library for Neo4j

### Install Neo4j Graph Data Science (GDS)

[Neo4j Server - Neo4j Graph Data Science](https://neo4j.com/docs/graph-data-science/current/installation/neo4j-server/)

- plugins directory: `/var/lib/neo4j/plugins`
- neo4j.conf file: `/etc/neo4j/neo4j.conf`

### Install and configure Neo4j *APOC*

[Installation - APOC Extended Documentation](https://neo4j.com/labs/apoc/5/installation/)

- create APOC configuration file:
    
    `cd /etc/neo4j`
    `sudo touch apoc.conf`
    
- add config:
    - `apoc.import.file.enabled=true`

## Basic commands

- Control the service: `sudo systemctl {enable|start|stop|restart} neo4j`
- Examine Neo4j’s status: `sudo systemctl status neo4j.service`
- Connect to the server: `cypher-shell -a 'neo4j://your_hostname:7687'`
