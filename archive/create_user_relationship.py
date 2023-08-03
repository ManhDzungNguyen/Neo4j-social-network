from py2neo import Graph
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from tqdm import tqdm
import time

init_time = time.time()
graph = Graph(password='12345678', host="10.9.3.209", port="7688") #7687: super big data

start_time = time.time()
res = graph.run("""
    MATCH (user1:User)-[r1:COMMENTED]->(post:Post)<-[r2:COMMENTED]-(user2:User)
    WHERE user1.fb_id < user2.fb_id // To avoid duplicate combinations
    WITH user1, user2, r1, r2,COLLECT(DISTINCT post) AS commonPosts
    RETURN user1, user2, r1, r2, commonPosts
""")
print(f"time_query_data: {time.time() - start_time}")         

raw_data = res.data()

df_res = pd.DataFrame(raw_data)
df_res.to_csv("full_users_connections.csv", index=False)
print(f"no_users_connection_records: {len(raw_data)}")


def exponential_decay(time, initial_value=1., decay_constant=0.1):
    decayed_value = initial_value * math.exp(- decay_constant * time)
    return decayed_value


def get_record_score(record):
    end_1, start_2 = None, None

    if record["r1"]["first_cmt_time"] < record["r2"]["first_cmt_time"]:
        end_1 = record["r1"]["last_cmt_time"]
        start_2 = record["r2"]["first_cmt_time"]
    else:
        end_1 = record["r2"]["last_cmt_time"]
        start_2 = record["r1"]["first_cmt_time"]

    if start_2 < end_1:
        return 1.

    time_interval = start_2 -  end_1
    if time_interval.months > 0:
        return 0.05
    
    time_interval_to_hours = time_interval.days * 24 + time_interval.seconds / 3600
    return max(exponential_decay(time_interval_to_hours), 0.05)


start_time = time.time()
relationship_scores = {}
for record in raw_data:
    user1 = record["user1"]["fb_id"]
    user2 = record["user2"]["fb_id"]

    if relationship_scores.get(user1) is None:
        relationship_scores[user1] = {}
    if relationship_scores[user1].get(user2) is None:
        relationship_scores[user1][user2] = {}

    relationship_scores[user1][user2]['weight'] = relationship_scores[user1][user2].get("weight", 0) + get_record_score(record)
    relationship_scores[user1][user2]['count'] = relationship_scores[user1][user2].get("count", 0) + 1
print(f"time_calculate_relationship_weight: {time.time() - start_time}")


start_time = time.time()
max_count, total_user_connection = 0, 0
k1_max, k2_max, weight_max = None, None, None

for k1 in tqdm(relationship_scores.keys()):
    for k2 in relationship_scores[k1].keys():
        if relationship_scores[k1][k2]["count"] > 1:
            total_weight = relationship_scores[k1][k2]["weight"]
            total_count = relationship_scores[k1][k2]["count"]
            res = graph.run(f"""
                MATCH graph = (user1:User WHERE user1.fb_id='{k1}'), (user2:User WHERE user2.fb_id='{k2}')
                MERGE (user1)-[r:COMMENTED_COMMON_POSTS]-(user2)
                SET r.weight = toFloat({total_weight})
                SET r.count = toInteger({total_count})
                """)
            
            total_user_connection += 1
            if total_count > max_count:
                max_count = total_count
                k1_max, k2_max, weight_max = k1, k2, total_weight

print(f"no_relationships_created: {total_user_connection}")
print(f"time_create_relationship_on_db: {time.time() - start_time}")
print(f"(max_count, uid_1, uid_2, weight); {(max_count, k1_max, k2_max, weight_max)}")
print(f"total_runtime: {time.time() - init_time}")