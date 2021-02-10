"""
This algorithm takes the graph created in the body of the script and it will print the vertices in each of the
connected components of the graph.

Each vertex starts in its own component. We then iterate adjacency list of every vertex u and merge u's component with
the component of each vertex v on the adjacency list.

The `comp_ptr` list tracks the component representative for each component to allow quick determinations on whether
two vertices are in the same component while the `comp_list` list of lists facilitates displaying the results of the
algorithm in a concise and efficient manner.

Algorithm 2.1.1 on page 25
"""

import networkx as nx


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
    The component representative of the component u is a part of
    """
    # The pointer for the representative vertex is equal to negative the size of the component
    if comp_ptr[u] < 0:
        return u
    else:
        # Recurse to find the component representative, using path compression so that the next access is faster
        rep = comp_rep(comp_ptr, comp_ptr[u])
        comp_ptr[u] = rep
        return rep


def merge(comp_ptr, comp_list, u_rep, v_rep):
    """
    Merge the smaller component into the larger one

    Parameters
    ----------
    comp_ptr : List of int
        The list of component pointers
    comp_list : List of List
        The list of lists which tracks vertices in a format conducive to printing them
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
        # Extend the list of vertices, appending that of u_rep to the end of v_rep's list. Free the slot in component
        comp_list[v_rep].extend(comp_list[u_rep])
        comp_list[u_rep] = None
    else:
        # Update the component representative for both vertices
        comp_ptr[v_rep] = u_rep
        comp_ptr[u_rep] = -(u_size + v_size)
        # Extend the list of vertices, appending that of v_rep to the end of u_rep's list. Free the slot in component
        comp_list[u_rep].extend(comp_list[v_rep])
        comp_list[v_rep] = None


def components(G):
    """
    Find the components of graph G

    Parameters
    ----------
    G : nx.Graph
        The graph to find the connected components in

    Returns
    -------
    A list of lists such that each non-None list contains the vertices of that component
    """
    # Create and initialize the lists
    # comp_ptr is seeded with -1 as each vertex is in its own component at the start of the algorithm
    # comp_list is seeded with a list containing n for the same reason as comp_ptr gets -1
    comp_ptr = list()
    comp_list = list()
    for n in range(len(G)):
        comp_ptr.append(-1)
        comp_list.append(list())
        comp_list[n].append(n)

    # For each vertex, look at all of its adjacent vertices
    for u in range(len(G)):
        for v in G[u]:
            # if the component representatives are different, merge the components
            u_rep = comp_rep(comp_ptr, u)
            v_rep = comp_rep(comp_ptr, v)
            if u_rep != v_rep:
                merge(comp_ptr, comp_list, u_rep, v_rep)
    return comp_list


def print_components(G):
    """
    Find the connected components of G and print them

    Parameters
    ----------
    G : nx.Graph
        The graph to find the connected components in
    """
    comp_list = components(G)

    for c in comp_list:
        if c is not None:
            print(f"Component Representative: {c[0]}, Component Members:", *c)


if __name__ == '__main__':
    graph = nx.readwrite.read_adjlist("../graphs/disconnected.adjlist", nodetype=int)
    print_components(graph)
