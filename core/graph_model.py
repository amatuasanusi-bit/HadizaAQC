import networkx as nx

class InfrastructureGraph:

    def __init__(self):

        self.G = nx.Graph()

    def add_node(self, name, asset_type, capacity=0):

        self.G.add_node(
            name,
            type=asset_type,
            capacity=capacity,
            load=0
        )

    def connect(self, a, b, distance=1):

        self.G.add_edge(a, b, distance=distance)

    def set_load(self, node, load):

        self.G.nodes[node]['load'] = load

    def nodes(self):

        return list(self.G.nodes)

    def edges(self):

        return list(self.G.edges)