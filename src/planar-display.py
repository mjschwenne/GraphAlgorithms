import networkx as nx
import matplotlib.pyplot as plt

if __name__ == '__main__':
    graph = nx.readwrite.read_adjlist("../Graphs/edge-cut.adjlist", nodetype=int)
    nx.draw_planar(graph, with_labels=True, font_weight='bold', font_color='white')
    plt.show()
