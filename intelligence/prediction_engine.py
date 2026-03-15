import numpy as np

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