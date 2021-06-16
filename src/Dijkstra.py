"""
This is Dijkstra's algorithm for finding the shortest path in a weighted graph.

It uses a priority queue to track the next closest vertex to add to the vertex cloud.
We assume that every vertex other than the starting one has a distance of infinity and added them to the priority queue.
Next, we pull from the priority queue and compare the distance to each of that vertex's neighbors to see if we have
found a shorter path. Update the distance in the priority queue and ensure it is still in heap order.

Algorithm 2.5.1 on page 35, however we are uses a priority queue rather than a list of vertices.
"""
import networkx as nx
import heapq
import math


def dijkstra(G, u):
    """
    Perform Dijkstra's algorithm on the graph `G` from origin vertex `u`.

    Parameters
    ----------
    G : nx.Graph
        The graph we wish to find the shortest paths though
    u : int
        The origin vertex, or where each path must start

    Returns
    -------
    List
        The list of shortest distances, such that list[v] = Dist(u, v)
    """
    dist = []
    heap = []
    heap_map = {}
    for v in G:
        if v == u:
            dist.append(0)
        else:
            dist.append(math.inf)
        heap_map[v] = [dist[v], v]
        heapq.heappush(heap, heap_map[v])

    while len(heap) != 0:
        dist_u, u = heapq.heappop(heap)
        for v in G[u]:
            dist[v] = min(dist[v], dist_u + G[u][v]["weight"])
            heap_map[v][0] = dist[v]
            heapq.heapify(heap)
    return dist


if __name__ == "__main__":
    graph = nx.readwrite.read_weighted_edgelist(
        "../graphs/weighted_sample.edgelist", nodetype=int
    )
    print(dijkstra(graph, 0))
