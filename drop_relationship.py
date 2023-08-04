from neo4j_adapter import NeoAdapter
import time

neo = NeoAdapter(host="10.9.3.209", port="7687", password="12345678")

init_time = time.time()
res = neo.drop_relationship("rel_01")
print(res)
print(f"runtime: {time.time() - init_time}")
