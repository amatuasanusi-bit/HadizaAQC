import networkx as nx

class RiskAnalyzer:

    def node_failure(self, graph):

        impacts = {}

        base = nx.number_connected_components(graph.G)

        for node in graph.G.nodes:

            temp = graph.G.copy()

            temp.remove_node(node)

            comp = nx.number_connected_components(temp)

            impacts[node] = comp - base

        return impacts