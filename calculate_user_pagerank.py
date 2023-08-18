from function import NeoAdapter


neo = NeoAdapter(host="10.9.3.209", port="7687", password="12345678")
check_use_graph = neo.run_query("RETURN gds.graph.exists('user-subgraph') AS r")
check_use_graph = check_use_graph.data()[0]["r"]
if not check_use_graph:
    neo.run_query(filepath="./cypher_query/project_user_graph.cyp")

df_pagerank = neo.calculate_PageRank("user-subgraph", top_k=200)
df_pagerank.to_csv("pagerank_top200.csv", index=False)
