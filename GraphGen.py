import networkx as nx
import matplotlib.pyplot as plt

# This algorithm takes a list of degree sequence and determines if it is graphic.
# If it is graphic, we will generate a graph with that degree sequence.

# This is the input degree sequence
deg_seq = [4, 4, 4, 4, 4]

# We assume that the degree sequence is true so that we can use this as a control variable in our loops
graphic = True

# Create the graph object
G = nx.Graph()

# Create the list of lists to track the outstanding degrees.
pts = list()
for x in deg_seq:
    pts.append(list())

# Create a temporary list to store vertices between degree updates
temp = list()
for x in deg_seq:
    temp.append(list())

# Sort the degree sequence
deg_seq.sort(reverse=True)

# Insert the degrees into the Pts list of lists.
# Also add the vertex to the Graph.
for x in range(len(deg_seq)):
    if deg_seq[x] >= len(deg_seq):
        graphic = False
    else:
        pts[deg_seq[x]].append(x)
        # We add one to shift from Python's zero indexing to start at vertex 1
        G.add_node(x + 1)

# Loop over all the possible vertex degrees starting with the largest
for k in reversed(range(len(deg_seq))):
    while len(pts[k]) > 0 and graphic:
        u = pts[k][0]
        pts[k].pop(0)
        # Join u to the next k vertices of largest degree
        i = k
        for j in range(1, k + 1):
            while len(pts[i]) == 0:
                i = i - 1
                if i == 0:
                    graphic = False
            v = pts[i][0]
            pts[i].pop(0)
            # We add one to shift from Python's zero indexing to one indexing
            G.add_edge(u + 1, v + 1)
            temp[i].append(v)
        # Transfer the vertices down in degree
        for j in reversed(range(k + 1)):
            while len(temp[j]) > 0:
                v = temp[j][0]
                temp[j].pop(0)
                pts[j - 1].append(v)

# Print where the input sequence is graphic or not
print(graphic)

# Display the graph
if graphic:
    nx.draw_circular(G, with_labels=True, font_weight='bold', font_color='white')
    plt.show()