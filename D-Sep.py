import numpy as np
from collections import deque

class BayesianNet:
    def __init__(self, adjacency_matrix):
        self.adj_matrix = adjacency_matrix
        self.num_nodes = adjacency_matrix.shape[0]
        self.graph = {i: [] for i in range(self.num_nodes)}
        self.parents = {i: [] for i in range(self.num_nodes)}

        for i in range(self.num_nodes):
            for j in range(self.num_nodes):
                if adjacency_matrix[i,j] == 1:
                    self.graph[i].append(j)
                    self.parents[j].append(i)

    def get_ancestors(self, nodes):
        ancestors = set()
        queue = deque(nodes)

        while queue:
            node = queue.popleft()
            for parent in self.parents[node]:
                if parent not in ancestors:
                    ancestors.add(parent)
                    queue.append(parent)
        return ancestors

    def is_d_sep(self, X, Y, Z):

        X = set(X) if isinstance(X, (list, tuple)) else {X}
        X = set(Y) if isinstance(Y, (list, tuple)) else {Y}
        X = set(Z) if isinstance(Z, (list, tuple)) else set(Z)

        ancestors = self.get_ancestors(X.union(Y).union(Z))

        graph = {i: set() for i in range(self.num_nodes)}
        for node in range(self.num_nodes):
            for child in self.graph[node]:
                graph[node].add(child)
                graph[child].add(node)

        visited = set()
        queue = deque()
        active_nodes = {node: False for node in range(self.num_nodes)}

        for x in X:
            queue.append((x,True))
            visited.add(x)

        while queue:
            node, active = queue.popleft()
            active_nodes[node] = active

            if node in Y and active:
                return False
            
            for neighbor in graph[node]:
                new_active = False
                if node in Z:
                    if neighbor in self.graph[node]:
                        new_active = False
                    else:
                        new_active = False
                else:
                    if neighbor in self.graph[node]:
                        new_active = active
                    else:
                        new_active = active and (node not in Z)

            if neighbor not in visited or (active_nodes[neighbor] != new_active and new_active):
                visited.add(neighbor)
                queue.append((neighbor, new_active))

        return True


