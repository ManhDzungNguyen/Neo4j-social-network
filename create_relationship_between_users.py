from tqdm import tqdm
import time
import argparse
from neo4j_adapter import NeoAdapter


neo = NeoAdapter(host="10.9.3.209", port="7687", password="12345678")

init_time = time.time()
res = neo.run_query(filepath="./cypher_query/create_relationship_between_users_v2.cyp")
print(res)
print(f"runtime: {time.time() - init_time}")

