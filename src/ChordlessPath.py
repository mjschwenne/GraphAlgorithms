import networkx as nx
from collections import deque


def remove_vertices(G, vertices):
    """
    Remove all vertices in `vertices` from the graph `G`

    Parameters
    ----------
    G : nx.Graph
        The graph from which vertices will be removed
    vertices : list
        The list of vertices in G to be removed

    Returns
    -------
    nx.Graph
        A copy of the graph `G` without the vertices listed in `vertices`
    """
    h = G.copy()
    h.remove_nodes_from(vertices)
    return h


def remove_edge(G, u, v):
    """
    Remove the edge `u``v` from graph `G`

    Parameters
    ----------
    G : nx.Graph
        The graph from which the edge will be removed
    u : Point
        The first endpoint of the edge
    v : Point
        The second endpoint of the edge

    Returns
    -------
    nx.Graph
        A copy of the graph `G` without the `u``v` edge
    """
    h = G.copy()
    h.remove_edge(u, v)
    return h


def bfs_path(G, source, destination):
    """
    Use a breadth first search to find the path from vertex `source` to vertex `destination`.

    Parameters
    ----------
    G : nx.Graph
        The graph to search
    source : Point
        Origin point
    destination : Point
        Destination point

    Returns
    -------
    deque
        A queue with the path from `source` to `destination` already enqueued.
    """
    vertex_dict = dict(nx.bfs_predecessors(G, source))
    queue = deque()
    queue.append(destination)
    while queue[-1] != source:
        queue.append(vertex_dict[queue[-1]])
    queue.reverse()
    return queue


def comp_rep(comp_ptr, u):
    """
    Find the component representative for the input vertex

    Parameters
    ----------
    comp_ptr : Dict
        The dictionary of component pointers
    u : Point
        The vertex of interest

    Returns
    -------
    Point :
        The component representative of the component u is a part of
    """
    # The pointer for the representative vertex is equal to negative the size of the component
    if isinstance(comp_ptr[u], int):
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
    comp_ptr : Dict of Point
        The list of component pointers
    u_rep : Point
        The component representative for the first component
    v_rep : Point
        The component representative for the first component
    """
    # Find the sizes of the components
    if type(comp_ptr[u_rep]) is int:
        u_size = -comp_ptr[u_rep]
    else:
        return
    if type(comp_ptr[v_rep]) is int:
        v_size = -comp_ptr[v_rep]
    else:
        return

    if u_size < v_size:
        # Update the component representative for both vertices
        comp_ptr[u_rep] = v_rep
        comp_ptr[v_rep] = -(u_size + v_size)
    else:
        # Update the component representative for both vertices
        comp_ptr[v_rep] = u_rep
        comp_ptr[u_rep] = -(u_size + v_size)


def components(G):
    """
    Find the components of graph G

    Parameters
    ----------
    G : nx.Graph
        The graph to find the connected components in

    Returns
    -------
    Dict of Point
        A dictionary such that each Point in the dictionary points to it's component representative or the size of
        the component that it represents
    """
    # Create and initialize the lists
    # comp_ptr is seeded with -1 as each vertex is in its own component at the start of the algorithm
    # comp_list is seeded with a list containing n for the same reason as comp_ptr gets -1
    comp_ptr = {}
    for v in G:
        comp_ptr[v] = -1

    # For each vertex, look at all of its adjacent vertices
    for u in G:
        for v in G[u]:
            # if the component representatives are different, merge the components
            u_rep = comp_rep(comp_ptr, u)
            v_rep = comp_rep(comp_ptr, v)
            if u_rep != v_rep:
                merge(comp_ptr, u_rep, v_rep)
    return comp_ptr


def chordless_path(G, t, Q, P, master_Q):
    """
    Find all the chordless paths from `source` to `target`.

    `Q` and `P` are recursive helper variables.

    Parameters
    ----------
    G : nx.Graph
        The Graph to find the chordless paths in
    t : Point
        The target point for the path
    Q : List
        A list of the current path from the original source to `target`
    P : deque
        A SimpleQueue representing the breadth first search path from `source` to `target`
    master_Q : List of List
        A List of List such that each list in the list is a chordless path

    Returns
    -------
    List
        The list of vertices from the original source to the target vertex
    """
    s = P.popleft()
    if t in G[s]:
        Q.append(t)
        master_Q.append(Q)
        return
    for v in G[s]:
        if v is not P[0]:
            # Determine if there is a vt-Path in G \ (N(s) \ v)
            vertices_to_remove = list(G[s].keys())
            vertices_to_remove.remove(v)
            removed_graph = remove_vertices(G, vertices_to_remove)
            comp_ptr = components(removed_graph)
            # Make sure they are in the same component
            if comp_ptr[t] == v or comp_ptr[v] == t:
                bfs_route = bfs_path(removed_graph, v, t)
                new_q = Q.copy()
                new_q.append(v)
                chordless_path(removed_graph, t, new_q, bfs_route, master_Q)
    next_vert = P[0]
    Q.append(next_vert)
    # Find G \ (N(s) \ nxt(s))
    vertices_to_remove = list(G[s].keys())
    vertices_to_remove.remove(next_vert)
    chordless_path(remove_vertices(G, vertices_to_remove), t, Q, P, master_Q)
