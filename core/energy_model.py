import numpy as np

class EnergyModel:

    def build_energy_matrix(self, graph):

        nodes = list(graph.G.nodes)
        n = len(nodes)

        Q = np.zeros((n, n))

        for i in range(n):

            node = nodes[i]

            load = graph.G.nodes[node]['load']
            capacity = graph.G.nodes[node]['capacity']

            cost = abs(load - capacity)

            Q[i, i] = cost

        for i in range(n):

            for j in range(n):

                if graph.G.has_edge(nodes[i], nodes[j]):

                    Q[i, j] -= 1

        return Q, nodes