import time

from function import NeoAdapter


neo = NeoAdapter(host="10.9.3.209", port="7687", password="12345678")

init_time = time.time()
res = neo.run_query(filepath="./cypher_query/create_r_INTERACTED_COMMON_POSTS.cyp")
print(res)
print(f"runtime: {time.time() - init_time}")
