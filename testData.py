import random
import sys
from collections import deque

# --- Graph Generation ---
n_nodes = 200
edges_per_node_target = 40
source_node = 0 # S
sink_node = n_nodes - 1 # T
capacity_min = 1 # Capacities should be at least 1 for meaningful flow paths
capacity_max = 20

# Use a set to store edges to ensure uniqueness and apply constraints
edges = set()
target_edges = n_nodes * edges_per_node_target
attempts = 0
max_attempts_factor = 10 # Increase attempts factor for potentially more constrained generation

while len(edges) < target_edges and attempts < target_edges * max_attempts_factor:
    u = random.randint(0, n_nodes - 1)
    v = random.randint(0, n_nodes - 1)

    # Apply constraints: no edges from Sink (T) or to Source (S), and no self-loops
    if u != sink_node and v != source_node and u != v:
        edges.add((u, v))
    attempts += 1

# Convert set to list and add capacities
network_edges = []
for u, v in list(edges):
    capacity = random.randint(capacity_min, capacity_max)
    # We already filtered for positive capacity by setting capacity_min to 1
    network_edges.append((u, v, capacity))

n_edges_actual = len(network_edges)

# --- Max Flow Calculation (Edmonds-Karp Algorithm) ---

# Create adjacency list representation for the residual graph
residual_graph = [{} for _ in range(n_nodes)]

for u, v, capacity in network_edges:
    residual_graph[u][v] = residual_graph[u].get(v, 0) + capacity
    residual_graph[v][u] = residual_graph[v].get(u, 0) + 0 # Initialize backward capacity

# BFS to find augmenting path
def bfs(s, t, parent_info, residual_cap, num_nodes):
    parent_info = [-1] * num_nodes
    queue = deque([s])
    visited = set([s])

    while queue:
        u = queue.popleft()

        for v in residual_cap[u]:
            if v not in visited and residual_cap[u][v] > 0:
                queue.append(v)
                visited.add(v)
                parent_info[v] = u
                if v == t:
                    return parent_info

    return None

# Edmonds-Karp main algorithm
def edmonds_karp(s, t, edges_list, num_nodes):
    residual_cap = [{} for _ in range(num_nodes)]
    for u, v, capacity in edges_list:
        residual_cap[u][v] = residual_cap[u].get(v, 0) + capacity
        residual_cap[v][u] = residual_cap[v].get(u, 0) + 0

    max_flow = 0

    while True:
        parent_info = bfs(s, t, [-1] * num_nodes, residual_cap, num_nodes)

        if parent_info is None:
            break

        path_flow = float('inf')
        v = t
        while v != s:
            u = parent_info[v]
            path_flow = min(path_flow, residual_cap[u][v])
            v = u

        v = t
        while v != s:
            u = parent_info[v]
            residual_cap[u][v] -= path_flow
            residual_cap[v][u] += path_flow
            v = u

        max_flow += path_flow

    return max_flow

calculated_max_flow = edmonds_karp(source_node, sink_node, network_edges, n_nodes)

# --- Provide Output ---

print("Flow Network Data:")
print(f"Number of Nodes: {n_nodes}")
print(f"Actual Number of Edges: {n_edges_actual}")
print(f"Source Node (S): {source_node}")
print(f"Sink Node (T): {sink_node}")
print("Constraints: No edges from T (node 199) or to S (node 0).")

print("\n--- Network File Content (approximate format) ---")
print(f"{n_nodes} {n_edges_actual} {source_node} {sink_node}")
# Print a few example edges
print("...")
for i in range(min(10, n_edges_actual)):
     print(f"{network_edges[i][0]} {network_edges[i][1]} {network_edges[i][2]}")
print("...")
if n_edges_actual > 10:
     for i in range(max(n_edges_actual - 5, 10), n_edges_actual):
          print(f"{network_edges[i][0]} {network_edges[i][1]} {network_edges[i][2]}")
print("--- End of Network File Content ---")

print(f"\nCalculated Maximum Flow: {calculated_max_flow}")

with open("flow_network_constrained.txt", "w") as f:
    f.write(f"{n_nodes} {n_edges_actual} {source_node} {sink_node}\n")
    for u, v, capacity in network_edges:
        f.write(f"{u} {v} {capacity}\n")
print("\nFull network data saved to flow_network_constrained.txt")