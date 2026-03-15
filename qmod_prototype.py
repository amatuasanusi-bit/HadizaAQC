pip install networkx numpy matplotlib
############################################################
# QMOD PROTOTYPE
# Quantum Modular Operational Dynamics
# Minimal research prototype (~300 lines)
############################################################

import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt

############################################################
# SECTION 1: INFRASTRUCTURE GRAPH MODEL
############################################################

class InfrastructureGraph:

    def __init__(self):
        self.G = nx.Graph()

    def add_asset(self, name, asset_type, capacity=0):
        self.G.add_node(name,
                        type=asset_type,
                        capacity=capacity,
                        load=0)

    def connect(self, a, b, distance=1):
        self.G.add_edge(a, b, distance=distance)

    def set_load(self, node, load):
        self.G.nodes[node]['load'] = load

    def draw(self):

        pos = nx.spring_layout(self.G)

        colors = []
        for n in self.G.nodes:
            t = self.G.nodes[n]['type']

            if t == "generator":
                colors.append("green")
            elif t == "substation":
                colors.append("orange")
            elif t == "load":
                colors.append("red")
            else:
                colors.append("blue")

        nx.draw(self.G, pos, with_labels=True, node_color=colors)
        plt.title("QMOD Infrastructure Graph")
        plt.show()


############################################################
# SECTION 2: PREDICTION ENGINE
############################################################

class PredictionEngine:

    def forecast_load(self, historical):

        # simple moving average predictor
        window = min(3, len(historical))
        return np.mean(historical[-window:])

    def predict_network(self, graph):

        predictions = {}

        for node in graph.G.nodes:

            hist = np.random.normal(50,10,5)
            predictions[node] = self.forecast_load(hist)

        return predictions


############################################################
# SECTION 3: QGAD ANOMALY DETECTION
############################################################

class QGAD:

    def detect_load_anomalies(self, graph):

        loads = []

        for n in graph.G.nodes:
            loads.append(graph.G.nodes[n]['load'])

        mean = np.mean(loads)
        std = np.std(loads)

        anomalies = []

        for n in graph.G.nodes:

            load = graph.G.nodes[n]['load']

            if abs(load - mean) > 2*std:
                anomalies.append(n)

        return anomalies


############################################################
# SECTION 4: MULTI-OBJECTIVE ENERGY MODEL
############################################################

class EnergyModel:

    def build_energy(self, graph):

        nodes = list(graph.G.nodes)

        n = len(nodes)

        Q = np.zeros((n,n))

        for i in range(n):

            node = nodes[i]

            load = graph.G.nodes[node]['load']
            capacity = graph.G.nodes[node]['capacity']

            cost = abs(load - capacity)

            Q[i,i] = cost

        # edge coupling

        for i in range(n):
            for j in range(n):

                if graph.G.has_edge(nodes[i],nodes[j]):
                    Q[i,j] += -1

        return Q,nodes


############################################################
# SECTION 5: CLASSICAL ANNEALING SOLVER
############################################################

class ClassicalAnnealer:

    def solve(self, Q):

        n = len(Q)

        x = np.random.randint(0,2,n)

        T = 10
        cooling = 0.95

        def energy(v):

            e = 0
            for i in range(n):
                for j in range(n):
                    e += Q[i,j]*v[i]*v[j]
            return e

        best = x.copy()
        best_e = energy(x)

        while T > 0.01:

            i = random.randint(0,n-1)

            new = x.copy()
            new[i] = 1-new[i]

            dE = energy(new)-energy(x)

            if dE < 0 or random.random() < np.exp(-dE/T):
                x = new

            e = energy(x)

            if e < best_e:
                best = x.copy()
                best_e = e

            T *= cooling

        return best,best_e


############################################################
# SECTION 6: RISK & RESILIENCE ANALYSIS
############################################################

class RiskAnalyzer:

    def node_failure_impact(self, graph):

        impacts = {}

        original = nx.number_connected_components(graph.G)

        for node in graph.G.nodes:

            temp = graph.G.copy()
            temp.remove_node(node)

            comp = nx.number_connected_components(temp)

            impacts[node] = comp - original

        return impacts


############################################################
# SECTION 7: QMOD SYSTEM ORCHESTRATOR
############################################################

class QMOD:

    def __init__(self):

        self.graph = InfrastructureGraph()
        self.predictor = PredictionEngine()
        self.qgad = QGAD()
        self.energy = EnergyModel()
        self.solver = ClassicalAnnealer()
        self.risk = RiskAnalyzer()

    ########################################################

    def build_demo_network(self):

        g = self.graph

        g.add_asset("SolarFarm","generator",capacity=80)
        g.add_asset("WindFarm","generator",capacity=60)
        g.add_asset("SubstationA","substation",capacity=120)
        g.add_asset("CityLoad","load",capacity=100)
        g.add_asset("Industry","load",capacity=70)

        g.connect("SolarFarm","SubstationA")
        g.connect("WindFarm","SubstationA")
        g.connect("SubstationA","CityLoad")
        g.connect("SubstationA","Industry")

        g.set_load("SolarFarm",70)
        g.set_load("WindFarm",55)
        g.set_load("SubstationA",90)
        g.set_load("CityLoad",120)
        g.set_load("Industry",60)

    ########################################################

    def run_prediction(self):

        pred = self.predictor.predict_network(self.graph)

        print("\nPredicted Loads")
        for k,v in pred.items():
            print(k,round(v,2))

    ########################################################

    def run_qgad(self):

        anomalies = self.qgad.detect_load_anomalies(self.graph)

        print("\nQGAD Anomalies")

        if anomalies:
            for a in anomalies:
                print("Anomaly:",a)
        else:
            print("No anomalies")

    ########################################################

    def run_optimizer(self):

        Q,nodes = self.energy.build_energy(self.graph)

        sol,e = self.solver.solve(Q)

        print("\nOptimization Result")

        for i,n in enumerate(nodes):
            print(n,sol[i])

        print("Energy:",e)

    ########################################################

    def run_risk(self):

        r = self.risk.node_failure_impact(self.graph)

        print("\nRisk Impact")

        for k,v in r.items():
            print(k,"impact:",v)

    ########################################################

    def visualize(self):

        self.graph.draw()


############################################################
# SECTION 8: MAIN EXECUTION
############################################################

def main():

    qmod = QMOD()

    qmod.build_demo_network()

    qmod.visualize()

    qmod.run_prediction()

    qmod.run_qgad()

    qmod.run_optimizer()

    qmod.run_risk()


if __name__ == "__main__":
    main()