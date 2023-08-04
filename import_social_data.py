import time
from py2neo import Graph
import pandas as pd

graph = Graph(
    password="12345678", host="10.9.3.209", port="7687"
)

# clean database 
start_time = time.time()
graph.run("""
    MATCH (n)
    CALL {
        WITH n
        DETACH DELETE n
    } IN TRANSACTIONS
""")

index_info = graph.run("SHOW INDEXES").data()
ls_index = [index["name"] for index in index_info]
for index in ls_index:
    graph.run(f"DROP INDEX {index}")
print(f"Fininised cleaning database: {time.time() - start_time}")


init_time = time.time()
df = pd.read_csv('/home/dungnguyen/work/Neo4j-social-network/data/data_user_post_full.csv',
                 dtype = {'fb_id': str, 'post_id': str, 'total_actor_post': int,
                          'total_share': int, 'total_comment': int, 
                          'first_cmt_time': str, 'last_cmt_time': str})


# import User nodes
start_time = time.time()
unique_uids = df.fb_id.unique()
uid_list_of_dicts = [{"uid": uid} for uid in unique_uids]
user_node_data = {
    "profiles": uid_list_of_dicts
}

query_import_node = """
UNWIND $profiles AS profile
CREATE (:User {uid:profile.uid})
"""
graph.run(query_import_node, parameters=user_node_data)
print(f"Fininised importing User nodes: {time.time() - start_time}")


# import Post nodes
start_time = time.time()
unique_post_ids = df.post_id.unique()
post_id_list_of_dicts = [{"post_id": post_id} for post_id in unique_post_ids]
post_node_data = {
    "posts_info": post_id_list_of_dicts
}

query_import_node = """
UNWIND $posts_info AS post_info
CREATE (:Post {post_id:post_info.post_id})
"""
graph.run(query_import_node, parameters=post_node_data)
print(f"Fininised importing Post nodes: {time.time() - start_time}")


# create index
start_time = time.time()
graph.run("CREATE INDEX user_index FOR (u:User) ON (u.uid)")
graph.run("CREATE INDEX post_index FOR (p:Post) ON (p.post_id)")
print(f"Fininised creating index: {time.time() - start_time}")

# import COMMENTED relationship
start_time = time.time()
selected_columns = ['fb_id', 'post_id', 'total_comment', 'first_cmt_time', 'last_cmt_time']
filtered_df = df[df['total_comment'] > 0]
comment_list_of_dicts = filtered_df[selected_columns].to_dict(orient='records')

commented_relationship_data = {
    "edges": comment_list_of_dicts
}

RELATIONSHIP = "COMMENTED"
query_import_relationship = f"""
UNWIND $edges AS edge
MATCH (user:User {{uid:edge.fb_id}}),(post:Post {{post_id:edge.post_id}})
CREATE (user)-[r:{RELATIONSHIP}  {{
total : edge.total_comment,
first_cmt_time : datetime(edge.first_cmt_time),
last_cmt_time : datetime(edge.last_cmt_time)
                        }}]->(post)
"""
graph.run(query_import_relationship, parameters=commented_relationship_data)
graph.run("CREATE INDEX comment_time FOR ()-[r:COMMENTED]-() ON (r.first_cmt_time)")
print(f"Fininised importing COMMENTED relationships: {time.time() - start_time}")


# import SHARED relationship
start_time = time.time()
selected_columns = ['fb_id', 'post_id', 'total_share']
filtered_df = df[df['total_share'] > 0]
shared_list_of_dicts = filtered_df[selected_columns].to_dict(orient='records')

shared_relationship_data = {
    "edges": shared_list_of_dicts
}

RELATIONSHIP = "SHARED"
query_import_relationship = f"""
UNWIND $edges AS edge
MATCH (user:User {{uid:edge.fb_id}}),(post:Post {{post_id:edge.post_id}})
CREATE (user)-[r:{RELATIONSHIP} {{total : edge.total_share}}]->(post)
"""
graph.run(query_import_relationship, parameters=shared_relationship_data)
print(f"Fininised importing SHARED relationships: {time.time() - start_time}")


# import POSTED relationship
selected_columns = ['fb_id', 'post_id']
filtered_df = df[df['total_actor_post'] > 0]
posted_list_of_dicts = filtered_df[selected_columns].to_dict(orient='records')

posted_relationship_data = {
    "edges": posted_list_of_dicts
}

NODE_LABEL_1 = "User"
NODE_LABEL_2 = "Post"
RELATIONSHIP = "POSTED"

query_import_relationship = f"""
UNWIND $edges AS edge
MATCH (user:User {{uid:edge.fb_id}}),(post:Post {{post_id:edge.post_id}})
CREATE (user)-[r:{RELATIONSHIP}]->(post)
"""
graph.run(query_import_relationship, parameters=posted_relationship_data)
print(f"Fininised importing POSTED relationships: {time.time() - start_time}")

print(f"\nTotal runtime: {time.time() - init_time}")