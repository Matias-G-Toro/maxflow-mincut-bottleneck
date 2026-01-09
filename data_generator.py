#!/usr/bin/env python3

import csv
import random

def generate_dataset(filename: str, num_nodes: int, density: float = 0.3) -> None:
    """ Generates a synthetic logistics dataset using standard CSV module """
    edges = []
    
    # Generate random connections
    for i in range(num_nodes):
        for j in range(num_nodes):
            if i != j and random.random() < density:
                # Random capacity between 10 and 100
                cap = random.randint(10, 100)
                edges.append([i, j, cap])
    
    # Ensure at least one guaranteed path from 0 to N-1
    current = 0
    while current < num_nodes - 1:
        next_node = min(current + random.randint(1, 3), num_nodes - 1)
        edges.append([current, next_node, 50])
        current = next_node

    # Write to CSV
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['source', 'target', 'capacity']) # Header
        writer.writerows(edges)
        
    print(f"Generated {filename} with {len(edges)} edges.")

if __name__ == "__main__":
    generate_dataset("small_logistics.csv", 10)
    generate_dataset("large_logistics.csv", 500, density=0.05)
