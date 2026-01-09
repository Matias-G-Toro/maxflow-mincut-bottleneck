#!/usr/bin/env python3

from collections import deque
from typing import List, Dict

class Edge:
    def __init__(self, u: int, v: int, capacity: int, flow: int = 0, reverse_edge: 'Edge' = None):
        """ Helper class to represent a logistics route (Edge) """
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = flow
        self.reverse_edge = reverse_edge

class FlowNetwork:
    def __init__(self, n: int):
        """ Constructor: n = total number of cities """
        self.n = n
        self.graph: Dict[int, List[Edge]] = {i: [] for i in range(n)}

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        """ Adds a directional route between cities """
        forward = Edge(u, v, capacity)
        backward = Edge(v, u, 0)
        
        # Link them for residual graph updates
        forward.reverse_edge = backward
        backward.reverse_edge = forward
        
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def _bfs(self, s: int, t: int, parent_map: Dict[int, Edge]) -> bool:
        """ Helper: BFS to find an augmenting path """
        visited = set()
        queue = deque([s])
        visited.add(s)

        while queue:
            u = queue.popleft()
            for edge in self.graph[u]:
                remaining_cap = edge.capacity - edge.flow
                if remaining_cap > 0 and edge.v not in visited:
                    visited.add(edge.v)
                    parent_map[edge.v] = edge
                    queue.append(edge.v)
                    if edge.v == t:
                        return True
        return False

    def edmonds_karp(self, s: int, t: int) -> int:
        """ Computes Maximum Flow using Edmonds-Karp """
        max_flow = 0
        parent_map = {}

        while self._bfs(s, t, parent_map):
            path_flow = float('inf')
            
            # Find bottleneck
            v = t
            while v != s:
                edge = parent_map[v]
                path_flow = min(path_flow, edge.capacity - edge.flow)
                v = edge.u
            
            # Update residual graph
            v = t
            while v != s:
                edge = parent_map[v]
                edge.flow += path_flow
                edge.reverse_edge.flow -= path_flow
                v = edge.u

            max_flow += path_flow
            parent_map = {} 

        return max_flow
