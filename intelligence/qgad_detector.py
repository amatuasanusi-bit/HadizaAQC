import numpy as np

class QGAD:

    def detect(self, graph):

        loads = []

        for n in graph.G.nodes:

            loads.append(graph.G.nodes[n]['load'])

        mean = np.mean(loads)
        std = np.std(loads)

        anomalies = []

        for n in graph.G.nodes:

            load = graph.G.nodes[n]['load']

            if abs(load - mean) > 2 * std:

                anomalies.append(n)

        return anomalies