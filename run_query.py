from neo4j_adapter import NeoAdapter
import time

neo = NeoAdapter(host="10.9.3.209", port="7687", password="12345678")
start_time = time.time()


# neo.run_query(filepath="./cypher_query/create_interact_v2.cyp")
# print(f"create relationship time: {time.time() - start_time}")

# start_time = time.time()


# neo.drop_property(property_name="pagerank",
#                   label="User")
print(neo.list_graph())
print(f"runtime: {time.time() - start_time}")