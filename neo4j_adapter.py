from py2neo import Graph
import pandas as pd
import time

class NeoAdapter(object):
    def __init__(self, host="localhost", port="7688", password="123!@#"):
        self.graph = Graph(host=host, port=port, password=password)


    def run_query(self, query=None, filepath=None):
        if filepath:
            with open(filepath, "r") as file:
                query = file.read()

        res = self.graph.run(query)
        return res
    

    def clear_database(self):
        ls_graph = self.list_graph()
        for graph in ls_graph:
            self.drop_graph(graph)
        
        query = """
            CALL apoc.periodic.iterate(
                'MATCH (n) RETURN n', 
                'DETACH DELETE n', 
                { batchSize:1000 }
            )
        """
        self.graph.run(query)

        index_info = self.graph.run("SHOW INDEXES").data()
        ls_index = [index["name"] for index in index_info]
        for index in ls_index:
            self.graph.run(f"DROP INDEX {index}")


    def drop_relationship(self, relationship: str):
        query = f"""
            CALL apoc.periodic.iterate(
                'MATCH p = ()-[r:{relationship}]->() RETURN r',
                'DETACH DELETE r',
                {{batchSize:1000}}
            )
            YIELD batches, total
            RETURN batches, total
        """
        res = self.graph.run(query)
        return res


    def list_graph(self):
        """
        show graphs in catalog
        """
        query = """
            CALL gds.graph.list()
            YIELD graphName
            RETURN graphName;
        """
        res = self.graph.run(query).data()
        res = [gds_graph['graphName'] for gds_graph in res]
        return res


    def drop_graph(self, graph_name):
        """
        drop a graph
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
            RETURN gds.util.asNode(nodeId).uid AS uid, score
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
