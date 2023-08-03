from py2neo import Graph
import pandas as pd
import time

class NeoAdapter(object):
    def __init__(self, host="localhost", port="7688", password="123!@#"):
        self.graph = Graph(host=host, port=port, password=password)

    def get_all_nodes(self, label=()):
        return self.graph.nodes.match(*label)

    def clear_all_data(self):
        query = """
            MATCH (n)
            CALL {
                WITH n
                DETACH DELETE n
            } IN TRANSACTIONS
        """
        self.graph.run(query)
        index_info = self.graph.run("SHOW INDEXES").data()
        ls_index = [index["name"] for index in index_info]
        for index in ls_index:
            self.graph.run(f"DROP INDEX {index}")


    def run_query_from_file(self, filepath):
        with open(filepath, "r") as file:
            query = file.read()

        res = self.graph.run(query)
        return res

    def graph_list(self):
        """
        show graphs in catalog
        """
        query = """
            CALL gds.graph.list()
            YIELD graphName
            RETURN graphName;
        """
        res = self.graph.run(query)
        return res

    def remove_graph(self, graph_name):
        """
        delete a graph
        """
        query = f"""
            CALL gds.graph.drop('{graph_name}')
            YIELD graphName;
        """
        res = self.graph.run(query)
        return res

    def calculate_PageRank(self, graph_name, top_k=20, to_pandas=True):
        start_time = time.time()
        query = (
            """
            CALL gds.pageRank.stream('"""
            + graph_name
            + """', {
                maxIterations: 20,
                dampingFactor: 0.85,
                relationshipWeightProperty: 'weight'
            })
            YIELD nodeId, score
            RETURN nodeId, score
            ORDER BY score DESC
            LIMIT """
            + str(top_k)
            + """;
        """
        )
        res = self.graph.run(query)
        print(f"time_calculate_PageRank: {time.time() - start_time}")

        if to_pandas:
            res = pd.DataFrame(res.data())

        return res
