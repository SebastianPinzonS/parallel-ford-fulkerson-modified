import collections,math,threading

class Edge:
    def __init__(self,from_node, to_node, capacity, held=0):
       
        if capacity < 0:
            raise ValueError("Capacity cannot be negative.")
        if held < 0:
             raise ValueError("Held value cannot be negative.") 
        
        self.from_node = from_node
        self.to_node = to_node
        self.capacity = capacity
        self.held = held
    
    def update_held(self,value):
        self.held += value

    def __repr__(self):
        return f"({self.from_node},{self.to_node}, capacity={self.capacity})"

class FlowNetwork:
    def __init__(self):
        self.graph = collections.defaultdict(list)
        self._lock = threading.Lock()


    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []
            print(f"Node '{node}' added.")
        else:
            print(f"Node '{node}' already exists.")

    def add_edge(self, from_node, to_node, capacity, held=0):

        if from_node not in self.graph:
             self.add_node(from_node)
        if to_node not in self.graph:
             self.add_node(to_node)

        new_edge = Edge(from_node,to_node, capacity, held)

        self.graph[from_node].append(new_edge)
        print(f"Edge added from '{from_node}' to '{to_node}' with capacity={capacity} and held={held}.")


    def get_edges(self, node):
        return self.graph.get(node, [])

    def get_nodes(self):
        return list(self.graph.keys())

    def display_network(self):
        print("\nFlow Network Structure:")
        if not self.graph:
            print("The network is empty.")
            return

        for node, edges in self.graph.items():
            print(f"Node '{node}':")
            if not edges:
                print("  No outgoing edges.")
            else:
                for edge in edges:
                    print(f"  -> {edge}")
    
    def get_edge(self, from_node, to_node):
        from_edges = self.graph.get(from_node)

        if not from_edges:
            return None

        for edge in from_edges:
            if edge.to_node == to_node:
                return edge
             
        return None

    def dfs(self,node,path,visited):
        if node == 'T': return path
        visited.append(node)
        reachable = sorted(self.get_edges(node), key=lambda edge: edge.held)
        for edge in reachable:
            if edge.capacity > 0 and edge.to_node not in visited:
                path.append((edge.from_node,edge.to_node))
                edge.update_held(1)
                result = self.dfs(edge.to_node,path,visited)
                if result: return result
                edge.update_held(-1)
                path.pop()
        return []
    
    def update_capacities(self,edge,value):
        edge.capacity += -value
        if reverse_edge:=self.get_edge(edge.to_node, edge.from_node):
            reverse_edge.capacity += value
        else: self.add_edge(edge.to_node, edge.from_node, value)


    def update_flow(self,edge_path):
        with self._lock:
            edge_list = []
            for edge in edge_path:
               edge_list.append(self.get_edge(edge[0],edge[1]))
            min_capacity = math.inf
            for edge in edge_list:
                if edge.capacity < min_capacity:
                    min_capacity = edge.capacity
            if min_capacity > 0:
                for edge in edge_list:
                    self.update_capacities(edge,min_capacity)
                    edge.update_held(-1)

    def get_max_flow(self):
        total_capacity = 0.0
        outgoing_edges = self.graph.get('T', [])
        for edge in outgoing_edges:
            total_capacity += edge.capacity
        return total_capacity

            
    @staticmethod
    def create_from_file(filename):
        network = FlowNetwork()
        try:
            with open(filename, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue

                    try:
                        # Split the line by space
                        parts = line.split()
                        if len(parts) != 3:
                            print(f"Skipping malformed line: {line} (Expected 3 parts, got {len(parts)})")
                            continue

                        from_name_str, to_name_str, capacity_str = parts

                        capacity = float(capacity_str)
                        held = 0.0 
                        from_node_id = from_name_str
                        to_node_id = to_name_str

                        # Ensure nodes exist in the graph structure
                        network.add_node(from_node_id)
                        network.add_node(to_node_id)

                        network.add_edge(from_node_id, to_node_id, capacity, held)

                    except ValueError as e:
                        print(f"Skipping line due to data conversion error: {line} - {e}")
                    except Exception as e:
                        print(f"Skipping line due to unexpected error during parsing: {line} - {e}")

            print(f"\nSuccessfully created network from file: {filename}")
            return network
        
        except FileNotFoundError:
            print(f"Error: File not found at {filename}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred while reading the file: {e}")
            return None
    
    def find_min_cut_nodes(self, source_node_id):

        reachable_nodes = set()
        stack = [source_node_id]

        if source_node_id not in self.graph:
            print(f"Warning: Source node '{source_node_id}' not found in the network.")
            return reachable_nodes

        reachable_nodes.add(source_node_id) 

        while stack:
            current_node_id = stack.pop()

            outgoing_edges = self.graph.get(current_node_id, [])

            for edge in outgoing_edges:
                neighbor_node_id = edge.to_node
                if edge.capacity > 0 and neighbor_node_id not in reachable_nodes:
                    reachable_nodes.add(neighbor_node_id)
                    stack.append(neighbor_node_id) 

        return reachable_nodes
    
    def find_min_cut_edges(self, source_node_id):
        source_side_nodes = self.find_min_cut_nodes(source_node_id)
        min_cut_edges = []
        for u in self.graph.keys():
            if u in source_side_nodes:
                for edge in self.graph.get(u, []):
                    v = edge.to_node
                    if v not in source_side_nodes:
                        min_cut_edges.append(edge)

        return min_cut_edges
