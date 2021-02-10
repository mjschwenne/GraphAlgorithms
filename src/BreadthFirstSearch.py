"""
The breadth first search finds the shortest path from a given vertex to every other vertex in an unweighted simple graph

Algorithm 2.4.1 on page 52
"""

import networkx as nx
import math
import queue


def bfs(G, u):
    """
    Perform a breadth first search over G starting at u

    Parameters
    ----------
    G : nx.Graph
        The graph we wish to search
    u : int
        The origin vertex from which the search starts

    Returns
    -------
    A list dist where dist[v] is the distance of the shortest path from u to v.
    Note, dist[u] = 0
    """
    # initialize the distance list to infinity for every vertex except u, which has a distance of 0
    dist = list()
    for v in range(len(G)):
        dist.append(math.inf)
    dist[u] = 0

    # Create a queue and seed vertex u into it.
    # Unlike ScanQ in the textbook, which is just an array we traverse in one direction, this is a proper FIFO queue
    q = queue.Queue()
    q.put(u)
    # So long as there are vertices left to process, get them from the queue
    # and if they do not have a non-infinity distance, update it.
    # Otherwise, we have already found the shortest path to that vertex
    while not q.empty():
        v = q.get()
        for w in G[v]:
            if dist[w] == math.inf:
                q.put(w)
                dist[w] = dist[v] + 1
    return dist


def print_bfs_dist(G, u):
    """
    Perform a breadth first search over G starting with u and print the results

    Parameters
    ----------
    G : nx.Graph
        The graph we wish to search
    u : int
        The origin vertex from which the search starts
    """
    bfs_dist = bfs(G, u)
    for v in range(len(G)):
        print(f"Vertex {v}: Dist({u}, {v}) = {bfs_dist[v]}")


if __name__ == '__main__':
    graph = nx.readwrite.read_adjlist("../graphs/petersen.adjlist", nodetype=int)
    print_bfs_dist(graph, 0)
