#!/usr/bin/env python3

import sys
import time
import csv
import random

import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from flow_network import FlowNetwork
from data_generator import generate_dataset

def load_graph(filename: str) -> FlowNetwork:
    """ Loads data from CSV using standard library """
    max_id = 0
    rows = []
    
    try:
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                u, v, cap = int(row['source']), int(row['target']), int(row['capacity'])
                rows.append((u, v, cap))
                max_id = max(max_id, u, v)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
            
    fn = FlowNetwork(max_id + 1)
    for u, v, cap in rows:
        fn.add_edge(u, v, cap)
    
    return fn

def get_node_positions(n: int) -> dict:
    """ 
    Creates a manual layout for the nodes.
    Source (0) is Left. Sink (n-1) is Right.
    """
    pos = {}
    pos[0] = (0.1, 0.5)      # Source
    pos[n-1] = (0.9, 0.5)    # Sink
    
    random.seed(42) # Fixed seed so nodes don't jump around between runs
    for i in range(1, n-1):
        pos[i] = (random.uniform(0.2, 0.8), random.uniform(0.1, 0.9))
    return pos

def visualize(fn: FlowNetwork, max_flow_val: int, output_file: str):
    """ Visualizes using PURE Matplotlib and SAVES to file """
    plt.figure(figsize=(10, 6))
    pos = get_node_positions(fn.n)
    
    # Draw Edges
    for u in range(fn.n):
        for edge in fn.graph[u]:
            if edge.capacity > 0: 
                x1, y1 = pos[u]
                x2, y2 = pos[edge.v]
                
                # Color logic
                color, width, alpha = 'lightgrey', 1, 0.3
                if edge.flow > 0:
                    color, width, alpha = 'blue', 2, 0.8
                if edge.flow == edge.capacity:
                    color, width, alpha = 'red', 3, 1.0 # Bottleneck

                plt.arrow(x1, y1, (x2-x1)*0.95, (y2-y1)*0.95, 
                          head_width=0.02, head_length=0.03, fc=color, ec=color, 
                          width=0.005 * width, alpha=alpha, length_includes_head=True)

    # Draw Nodes
    for i in range(fn.n):
        x, y = pos[i]
        color = 'gold' if i == 0 or i == fn.n-1 else 'white'
        plt.scatter(x, y, s=500, c=color, edgecolors='black', zorder=10)
        plt.text(x, y, str(i), ha='center', va='center', fontweight='bold', zorder=11)

    plt.title(f"Max Throughput: {max_flow_val} Units\n(Red=Bottleneck, Blue=Flow)")
    plt.axis('off')
    plt.tight_layout()
    
    # --- FIX: Save instead of show ---
    plt.savefig(output_file)
    print(f"Visualization saved to: {output_file}")
    plt.close() # Close memory
    # ---------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  ./main.py demo              (Runs random demo)")
        print("  ./main.py file <filename>   (Runs specific file)")
        print("  ./main.py benchmark         (Runs timing analysis)")
        sys.exit(1)
        
    mode = sys.argv[1]

    if mode == "file":
        if len(sys.argv) != 3:
            print("Usage: ./main.py file <filename>")
            sys.exit(1)
        filename = sys.argv[2]
        print(f"--- Processing {filename} ---")
        net = load_graph(filename)
        start_time = time.time()
        max_flow = net.edmonds_karp(0, net.n - 1)
        print(f"Algorithm time: {time.time() - start_time:.6f}s")
        print(f"Max Flow: {max_flow}")
        visualize(net, max_flow, "output_graph.png")

    elif mode == "demo":
        print("--- Running Demo Mode ---")
        generate_dataset("demo_data.csv", 12, density=0.25)
        net = load_graph("demo_data.csv")
        max_flow = net.edmonds_karp(0, net.n - 1)
        print(f"Max Flow: {max_flow}")
        visualize(net, max_flow, "demo_result.png")

    elif mode == "benchmark":
        print("--- Running Timing Analysis ---")
        sizes = [10, 50, 100, 200, 300]
        times = []
        for n in sizes:
            filename = f"bench_{n}.csv"
            generate_dataset(filename, n, density=0.2)
            net = load_graph(filename)
            t0 = time.time()
            net.edmonds_karp(0, n - 1)
            t1 = time.time()
            times.append(t1 - t0)
            print(f"Nodes: {n:3d} | Time: {t1 - t0:.5f}s")
            
        plt.plot(sizes, times, marker='o', linestyle='-', color='b')
        plt.title("Execution Time vs Graph Size")
        plt.xlabel("Number of Nodes")
        plt.ylabel("Time (seconds)")
        plt.grid(True)
        
        # --- FIX: Save instead of show ---
        plt.savefig("benchmark_plot.png")
        print("Timing plot saved to: benchmark_plot.png")
        plt.close()
        # ---------------------------------

if __name__ == "__main__":
    main()
