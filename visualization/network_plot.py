import matplotlib.pyplot as plt
import networkx as nx

def draw(graph):

    pos = nx.spring_layout(graph.G)

    nx.draw(graph.G, pos, with_labels=True)

    plt.title("QMOD Infrastructure Network")

    plt.show()