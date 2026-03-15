from qmod_system import QMOD
from visualization.network_plot import draw

def build_demo(q):

    g = q.graph

    g.add_node("SolarFarm","generator",80)
    g.add_node("WindFarm","generator",60)
    g.add_node("Substation","substation",120)
    g.add_node("City","load",100)

    g.connect("SolarFarm","Substation")
    g.connect("WindFarm","Substation")
    g.connect("Substation","City")

    g.set_load("SolarFarm",70)
    g.set_load("WindFarm",50)
    g.set_load("Substation",80)
    g.set_load("City",110)


def main():

    q = QMOD()

    build_demo(q)

    draw(q.graph)

    pred = q.predictor.forecast_network(q.graph)
    print("Predictions:",pred)

    anomalies = q.qgad.detect(q.graph)
    print("Anomalies:",anomalies)

    solution = q.optimize()

    print("Optimization:",solution)

    risk = q.risk.node_failure(q.graph)

    print("Risk:",risk)


if __name__ == "__main__":
    main()