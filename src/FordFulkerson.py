"""

"""
import networkx as nx
from itertools import chain


def augment_flow(N, s, t, prev_pt, res_cap):
    """
    Take the augmenting path to `t` and increase the flow so that it is no longer augmenting

    All operations are done in place to the network `N`

    Parameters
    ----------
    N : nx.DiGraph
        The network with contains the augmenting path
    s : int
        The starting vertex of the augmenting path
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
    while u is not s:
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
    prev_pt = dict()
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
        augment_flow(N, s, t, prev_pt, res_cap)
        flow += res_cap[t]
        prev_pt.clear()


if __name__ == '__main__':
    network = nx.read_edgelist("../graphs/network.edgelist", create_using=nx.DiGraph, nodetype=int)
    print(ford_fulkerson(network, 0, 5))
