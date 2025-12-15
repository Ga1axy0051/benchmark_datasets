#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Build airport network graph from OpenFlights routes.dat

Input:
    routes.dat

Output:
    airport_edgelist.txt     # 无向、去重、最大连通子图
    airport_graph.pkl        # networkx Graph（可直接 load）
    airport_stats.txt        # 基本统计信息

Author: you
"""

import os
import networkx as nx
import pickle


ROUTES_PATH = "/home/guoquanjiang/WXY/benchmark_datasets/Airport/routes.dat"          # 原始航线文件
OUT_EDGE_PATH = "/home/guoquanjiang/WXY/benchmark_datasets/Airport/airport_edgelist.txt"
OUT_GRAPH_PATH = "/home/guoquanjiang/WXY/benchmark_datasets/Airport/airport_graph.pkl"
OUT_STATS_PATH = "/home/guoquanjiang/WXY/benchmark_datasets/Airport/airport_stats.txt"


def load_airport_graph(routes_path, undirected=True):
    """
    Load airport graph from OpenFlights routes.dat

    Nodes: AirportID (int)
    Edges: flight routes
    """
    G = nx.DiGraph()

    with open(routes_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) < 6:
                continue

            src = parts[3]
            dst = parts[5]

            if src == "\\N" or dst == "\\N":
                continue

            try:
                src = int(src)
                dst = int(dst)
            except ValueError:
                continue

            if src != dst:
                G.add_edge(src, dst)

    if undirected:
        G = G.to_undirected()

    return G


def main():
    if not os.path.exists(ROUTES_PATH):
        raise FileNotFoundError(f"Cannot find {ROUTES_PATH}")

    print("📘 Loading airport routes...")
    G = load_airport_graph(ROUTES_PATH)

    print(f"Original graph: nodes={G.number_of_nodes()}, edges={G.number_of_edges()}")

    # 取最大连通子图
    print("📘 Extracting largest connected component...")
    largest_cc = max(nx.connected_components(G), key=len)
    G = G.subgraph(largest_cc).copy()

    print(f"LCC graph: nodes={G.number_of_nodes()}, edges={G.number_of_edges()}")

    # 保存 edge list
    print("💾 Saving edge list...")
    with open(OUT_EDGE_PATH, "w") as f:
        for u, v in G.edges():
            f.write(f"{u} {v}\n")

    # 保存 graph 对象
    print("💾 Saving graph pickle...")
    with open(OUT_GRAPH_PATH, "wb") as f:
        pickle.dump(G, f)

    # 写统计信息
    print("💾 Writing stats...")
    with open(OUT_STATS_PATH, "w") as f:
        f.write("Airport Network Statistics\n")
        f.write("===========================\n")
        f.write(f"Nodes: {G.number_of_nodes()}\n")
        f.write(f"Edges: {G.number_of_edges()}\n")
        f.write(f"Average degree: {sum(dict(G.degree()).values()) / G.number_of_nodes():.4f}\n")
        f.write(f"Is connected: {nx.is_connected(G)}\n")
        f.write(f"Diameter (approx): {nx.approximation.diameter(G)}\n")

    print("✅ Done.")
    print(f"  - {OUT_EDGE_PATH}")
    print(f"  - {OUT_GRAPH_PATH}")
    print(f"  - {OUT_STATS_PATH}")


if __name__ == "__main__":
    main()
