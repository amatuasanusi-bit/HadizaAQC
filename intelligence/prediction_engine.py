import numpy as np

import networkx as nx

# 1. Create a sample graph (e.g., using NetworkX)
class InfrastructureGraph:
    def __init__(self):
        # Creating a simple graph with 3 nodes
        self.G = nx.Graph()
        self.G.add_nodes_from(["Server_A", "Database_1", "Gateway_01"])

# 2. Initialize your engine and the graph
graph_instance = InfrastructureGraph()
engine = PredictionEngine()

# 3. Generate the results
results = engine.forecast_network(graph_instance)

# 4. View the output
print(f"Node Predictions: {results}")


class PredictionEngine:

    def moving_average(self, data, window=3):

        if len(data) < window:
            return np.mean(data)

        return np.mean(data[-window:])


    def forecast_node(self):

        hist = np.random.normal(50, 10, 5)

        return self.moving_average(hist)


    def forecast_network(self, graph):

        predictions = {}

        for node in graph.G.nodes:

            predictions[node] = self.forecast_node()

        return predictions