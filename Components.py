import networkx as nx


# This algorithm takes the graph created in the body of the script and it will print the vertices in each of the
# connected components of the graph.
#
# Algorithm 2.1.1 from Graphs, Algorithms and Optimization (2nd edition) by William L Kocay and Donald L Kreher

# The comp_rep function takes in a vertex and finds the representative for the component it is a part of.
def comp_rep(comp_ptr, u):
    if comp_ptr[u] < 0:
        return u
    else:
        rep = comp_rep(comp_ptr, comp_ptr[u])
        comp_ptr[u] = rep
        return rep


# The merge function takes the component representative of two different components and merges then into a single one.
def merge(comp_ptr, component, u_rep, v_rep):
    u_size = -comp_ptr[u_rep]
    v_size = -comp_ptr[v_rep]

    if u_size < v_size:
        comp_ptr[u_rep] = v_rep
        comp_ptr[v_rep] = -(u_size + v_size)
        component[v_rep].extend(component[u_rep])
        component[u_rep] = None
    else:
        comp_ptr[v_rep] = u_rep
        comp_ptr[u_rep] = -(u_size + v_size)
        component[u_rep].extend(component[v_rep])
        component[v_rep] = None


# The components function executes the algorithm on the given graph
def components(g):
    comp_ptr = list()
    component = list()
    for n in range(len(g)):
        comp_ptr.append(-1)
        component.append(list())
        component[n].append(n)

    for u in range(len(g)):
        for v in G[u]:
            u_rep = comp_rep(comp_ptr, u)
            v_rep = comp_rep(comp_ptr, v)
            if u_rep != v_rep:
                merge(comp_ptr, component, u_rep, v_rep)
    return component


# Create the graph and call the algorithm, then print the component list of lists
G = nx.Graph()
# Add the edges to the graph as a list of tuples.
# In order to work with Python's indexing, the lowest numbered vertex MUST be zero, not one
G.add_edges_from([(0, 1), (2, 3), (2, 4), (3, 4)])
component_list = components(G)

# Print the non empty lists from the component lists
for i in component_list:
    if i is not None:
        print(i)
