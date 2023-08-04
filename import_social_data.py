import time
from neo4j_adapter import NeoAdapter
import pandas as pd


neo = NeoAdapter(host="10.9.3.209", port="7687", password="12345678")

# clean database 
neo.clear_database()


init_time = time.time()

# import User nodes
start_time = time.time()
query = """
    CALL apoc.periodic.iterate(
        'CALL apoc.load.json("/home/dungnguyen/work/Neo4j-social-network/data/clean/event_6843/N_User.json") YIELD value UNWIND value.data AS user RETURN user.uid AS uid',
        'CREATE (:User {uid:uid})',
        {batchSize:1000, iterateList:true, parallel:true}
    )
"""
neo.run_query(query)
print(f"Fininised importing User nodes: {time.time() - start_time}")


# import User nodes
start_time = time.time()
query = """
    CALL apoc.periodic.iterate(
        'CALL apoc.load.json("/home/dungnguyen/work/Neo4j-social-network/data/clean/event_6843/N_Post.json") YIELD value UNWIND value.data AS post RETURN post.post_id AS post_id',
        'CREATE (:Post {post_id:post_id})',
        {batchSize:1000, iterateList:true, parallel:true}
    )
"""
neo.run_query(query)
print(f"Fininised importing Post nodes: {time.time() - start_time}")


# create index
start_time = time.time()
neo.run_query("CREATE INDEX user_index FOR (u:User) ON (u.uid)")
neo.run_query("CREATE INDEX post_index FOR (p:Post) ON (p.post_id)")
print(f"Fininised creating index: {time.time() - start_time}")


# import COMMENTED relationship
start_time = time.time()
query = """
    CALL apoc.periodic.iterate(
        'CALL apoc.load.json("/home/dungnguyen/work/Neo4j-social-network/data/clean/event_6843/R_COMMENTED.json") YIELD value UNWIND value.data AS edge RETURN edge',
        'MATCH (user:User {uid:edge.fb_id}),(post:Post {post_id:edge.post_id}) CREATE (user)-[r:COMMENTED {total : edge.total_comment, first_cmt_time : datetime(edge.first_cmt_time), last_cmt_time : datetime(edge.last_cmt_time)}]->(post)',
        {batchSize:1000}
    )
"""
neo.run_query(query)
print(f"Fininised importing COMMENTED relationships: {time.time() - start_time}")


# import SHARED relationship
start_time = time.time()
query = """
    CALL apoc.periodic.iterate(
        'CALL apoc.load.json("/home/dungnguyen/work/Neo4j-social-network/data/clean/event_6843/R_SHARED.json") YIELD value UNWIND value.data AS edge RETURN edge',
        'MATCH (user:User {uid:edge.fb_id}),(post:Post {post_id:edge.post_id}) CREATE (user)-[r:SHARED {total : edge.total_share}]->(post)',
        {batchSize:1000}
    )
"""
neo.run_query(query)
print(f"Fininised importing SHARED relationships: {time.time() - start_time}")


# import POSTED relationship
start_time = time.time()
query = """
    CALL apoc.periodic.iterate(
        'CALL apoc.load.json("/home/dungnguyen/work/Neo4j-social-network/data/clean/event_6843/R_POSTED.json") YIELD value UNWIND value.data AS edge RETURN edge',
        'MATCH (user:User {uid:edge.fb_id}),(post:Post {post_id:edge.post_id}) CREATE (user)-[r:POSTED]->(post)',
        {batchSize:1000}
    )
"""
neo.run_query(query)
print(f"Fininised importing POSTED relationships: {time.time() - start_time}")

print(f"\nTotal runtime: {time.time() - init_time}")