#!/usr/bin/env python3

import unittest
from flow_network import FlowNetwork

class FlowNetworkTest(unittest.TestCase):
    
    def test_simple_path(self):
        # 0 -> 1 -> 2 (Capacity 10)
        net = FlowNetwork(3)
        net.add_edge(0, 1, 10)
        net.add_edge(1, 2, 10)
        max_flow = net.edmonds_karp(0, 2)
        self.assertEqual(max_flow, 10)

    def test_bottleneck(self):
        # 0 -> 1 (100) -> 2 (5) -> 3 (100)
        net = FlowNetwork(4)
        net.add_edge(0, 1, 100)
        net.add_edge(1, 2, 5)
        net.add_edge(2, 3, 100)
        max_flow = net.edmonds_karp(0, 3)
        self.assertEqual(max_flow, 5)

    def test_disconnected(self):
        # 0 -> 1   2 -> 3
        net = FlowNetwork(4)
        net.add_edge(0, 1, 10)
        net.add_edge(2, 3, 10)
        max_flow = net.edmonds_karp(0, 3)
        self.assertEqual(max_flow, 0)

if __name__ == '__main__':
    unittest.main()
