"""
Kruskal's algorithm for a minimum spanning tree. Using the idea of a forest, we pick minimum weight edges from the graph
and use them to connect components. Each component is a tree itself and once we have connected every component our
forest as grown into a beautiful spanning tree.

Algorithm 5.4.2 on page 85
"""
import networkx as nx
import matplotlib.pyplot as plt
import heapq


def comp_rep(comp_ptr, u):
    """
    Find the component representative for the input vertex

    Parameters
    ----------
    comp_ptr : list
        The list of component pointers
    u : int
        The vertex of interest

    Returns
    -------
    int :
        The component representative of the component u is a part of
    """
    # The pointer for the representative vertex is equal to negative the size of the component
    if isinstance(comp_ptr[u], int) and comp_ptr[u] < 0:
        return u
    else:
        # Recurse to find the component representative, using path compression so that the next access is faster
        rep = comp_rep(comp_ptr, comp_ptr[u])
        comp_ptr[u] = rep
        return rep


def merge(comp_ptr, u_rep, v_rep):
    """
    Merge the smaller component into the larger one

    Parameters
    ----------
    comp_ptr : List of int
        The list of component pointers
    u_rep : int
        The component representative for the first component
    v_rep : int
        The component representative for the first component
    """
    # Find the sizes of the components
    u_size = -comp_ptr[u_rep]
    v_size = -comp_ptr[v_rep]

    if u_size < v_size:
        # Update the component representative for both vertices
        comp_ptr[u_rep] = v_rep
        comp_ptr[v_rep] = -(u_size + v_size)
    else:
        # Update the component representative for both vertices
        comp_ptr[v_rep] = u_rep
        comp_ptr[u_rep] = -(u_size + v_size)


def kruskal(G):
    """
    Perform Kruskal's minimum spanning tree algorithm on the graph

    Parameters
    ----------
    G : nx.Graph

    Returns
    -------
    nx.Graph
        The minimum spanning tree of the graph
    """
    # Create the tree and add every vertex to it
    tree = nx.Graph()
    # We will track the vertices with a modified system similar to the components algorithm, using a dictionary
    components = {}
    for v in G:
        components[v] = -1
    # Create an construct the heap of edges
    heap = []
    for e in G.edges:
        heapq.heappush(heap, [G[e[0]][e[1]]['weight'], (e[0], e[1])])

    # While we don't have enough edges to make a tree
    while tree.number_of_edges() < len(G) - 1:
        # Pull the minimum edge
        weight, e = heapq.heappop(heap)
        e0_rep = comp_rep(components, e[0])
        e1_rep = comp_rep(components, e[1])
        if e0_rep != e1_rep:
            tree.add_edge(e[0], e[1])
            merge(components, e0_rep, e1_rep)
    return tree


if __name__ == '__main__':
    graph = nx.readwrite.read_weighted_edgelist("../graphs/prim.edgelist", nodetype=int)
    mst = kruskal(graph)
    nx.draw_circular(graph, with_labels=True, font_weight='bold', font_color='white')
    plt.show()
    nx.draw_circular(mst, with_labels=True, font_weight='bold', font_color='white')
    plt.show()
