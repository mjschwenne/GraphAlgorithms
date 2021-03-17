"""
Prim's algorithm for minimum spanning trees. Given a starting vertex, create a cloud of vertices VT and then find the
edge of minimum weight such that one end is in VT and the other end is not. Repeat until the tree has n - 1 edges.

Algorithm 5.4.2 on page 82, using a heap to store vertices
"""
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import math


def prim(G):
    """
    Perform Prim's algorithm for a minimum spanning tree.

    This version of Prims will ALWAYS start a vertex 0

    Parameters
    ----------
    G : nx.Graph
        The graph we want to find a minimum spanning tree in

    Returns
    -------
    nx.Graph
        A minimum spanning tree for `G`.
    """
    # Initialize the data structures
    tree = nx.Graph()
    vt = {0}
    heap = []
    heap_map = {}
    # For vertices adjacent to u in G, record them as their weight from u in the heap, else inf
    for e in G.edges:
        # Cast everything into tuples so that I can compare them directly and construct new ones later in the algorithm
        if 0 in e:
            heap_map[(e[0], e[1])] = [G[e[0]][e[1]]['weight'], (e[0], e[1])]
        else:
            heap_map[(e[0], e[1])] = [math.inf, (e[0], e[1])]
        heapq.heappush(heap, heap_map[e])

    # While we don't have enough edges to make a tree
    while tree.number_of_edges() < len(G) - 1:
        weight, e = heapq.heappop(heap)
        if e[0] not in vt and e[1] in vt:
            vt.add(e[0])
            tree.add_edge(e[0], e[1], weight=weight)
            # Update the heap
            for v in G[e[0]]:
                if (v, e[0]) in heap_map.keys():
                    heap_map[(v, e[0])][0] = G[v][e[0]]['weight']
                else:
                    heap_map[(e[0], v)][0] = G[v][e[0]]['weight']
            heapq.heapify(heap)
        if e[1] not in vt and e[0] in vt:
            vt.add(e[1])
            tree.add_edge(e[0], e[1], weight=weight)
            # Update the heap
            for v in G[e[1]]:
                if (v, e[1]) in heap_map.keys():
                    heap_map[(v, e[1])][0] = G[v][e[1]]['weight']
                else:
                    heap_map[(e[1], v)][0] = G[v][e[1]]['weight']
            heapq.heapify(heap)

    return tree


if __name__ == '__main__':
    graph = nx.readwrite.read_weighted_edgelist("../graphs/prim.edgelist", nodetype=int)
    mst = prim(graph)
    nx.draw_circular(graph, with_labels=True, font_weight='bold', font_color='white')
    plt.show()
    nx.draw_circular(mst, with_labels=True, font_weight='bold', font_color='white')
    plt.show()
