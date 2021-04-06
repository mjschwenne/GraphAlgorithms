"""
The Ford-Fulkerson Algorithm find the maximum flow in a network, a directed graph from a source vertex `s` to a target
vertex `t`. Each edge in the graph has a capacity which may not be exceeded by the flow running through the graph.
Additionally, the amount of flow into a vertex must equal the flow out of that vertex.

The Ford-Fulkerson algorithm finding the maximum flow using the concept of augmenting paths. An augmenting path in a
network is a path form `s` to `t` using only edges with have residual capacity. If there are no such paths, then the
flow is maximum. Forward edges follow the direction of the arc in the network while backwards edges move against the
arc in the network. Backwards edges can have there flow reduced to increase the overall flow of the network

Algorithm 10.2.2 on page 201
"""
import networkx as nx
from itertools import chain


def augment_flow(N, t, prev_pt, res_cap):
    """
    Take the augmenting path to `t` and increase the flow so that it is no longer augmenting

    All operations are done in place to the network `N`. The `prev_pt` of the start of the path is assumed to be `None`.

    Parameters
    ----------
    N : nx.DiGraph
        The network with contains the augmenting path
    t : int
        The terminal vertex of the augmenting path
    prev_pt : Dict
        A mapping of the vertices to the predecessor vertex in the path
    res_cap : Dict
        A mapping from vertex `v` to the residual capacity of the `s`-`v` path
    """
    v = t
    u = prev_pt[v]
    delta = res_cap[t]
    # While we are not at the start of the augmenting path
    while u is not None:
        if v in N[u]:
            N[u][v]['flow'] += delta
        else:
            N[v][u]['flow'] -= delta
        v = u
        u = prev_pt[v]


def ford_fulkerson(N, s, t):
    """
    Performs the Ford-Fulkerson Algorithm on the given network to find the maximum flow of the network.

    Results of the algorithm are stored in place in `N` and the value of the flow is returned.
    Edge attribute capacity is assumed to set for each edge

    Parameters
    ----------
    N : nx.DiGraph
    s : int
        The source vertex of the network
    t : int
        The target vertex of the network

    Returns
    -------
    int
        The value of the maximum flow
    """
    # Ensure that the current flow of the network is the zero flow and initialize the residual capacity dict
    flow = 0
    for u, v in N.edges:
        N[u][v]['flow'] = 0
    res_cap = {s: 0}
    for v in N[s]:
        res_cap[s] += N[s][v]['capacity']
        res_cap[v] = N[s][v]['capacity']
    # Create and initialize the prev_pt list used to track the breadth first search of the algorithm
    prev_pt = {s: None}
    # While there could be an augmenting path in the graph
    while True:
        # Similar to the Hungarian algorithm, the textbook describes q as a queue, but it is not one as we need to be
        # able to see if we have previously visited a vertex which is incompatible with removing elements from the
        # queue in a pop operation. Instead we will use a list which is processed from the front to the back
        q = [s]
        k = 0
        aug_path = False
        while k < len(q) and not aug_path:
            u = q[k]
            # Perform the breadth first search, disregarding edge direction
            adj = chain(N.successors(u), N.predecessors(u))
            for v in adj:
                # If we have not visited v before
                if v not in q:
                    # If uv is a forward edge
                    if v in N[u]:
                        if N[u][v]['capacity'] > N[u][v]['flow']:
                            q.append(v)
                            prev_pt[v] = u
                            if res_cap[u] < N[u][v]['capacity'] - N[u][v]['flow']:
                                res_cap[v] = res_cap[u]
                            else:
                                res_cap[v] = N[u][v]['capacity'] - N[u][v]['flow']
                            if v == t:
                                # Augmenting path has been found
                                aug_path = True
                                break
                    # If uv is a backwards edge
                    else:
                        if N[v][u]['flow'] > 0:
                            q.append(v)
                            prev_pt[v] = u
                            if res_cap[u] < N[v][u]['flow']:
                                res_cap[v] = res_cap[u]
                            else:
                                res_cap[v] = N[v][u]['flow']
                            if v == t:
                                # Augmenting path has been found
                                aug_path = True
                                break
            # Advance the 'queue'
            k += 1
        # if k >= len(q) then there is no augmenting path left in the graph
        if k >= len(q):
            return flow
        augment_flow(N, t, prev_pt, res_cap)
        flow += res_cap[t]
        prev_pt = {s: None}


if __name__ == '__main__':
    network = nx.read_edgelist("../graphs/hw8.edgelist", create_using=nx.DiGraph, nodetype=int)
    print(f"The total value of the flow is {ford_fulkerson(network, 0, 7)}")
    for x, y in network.edges:
        print(f"For edge {x} -> {y} the flow is {network[x][y]['flow']}")
