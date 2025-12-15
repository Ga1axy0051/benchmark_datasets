import sys
from collections import deque, defaultdict

EDGE_PATH = "/home/guoquanjiang/WXY/benchmark_datasets/roadNetCA/roadNet-CA.txt"      # ← 改成你的路径
OUT_20K = "roadNet-CA_bfs20k.edgelist"
OUT_100K = "roadNet-CA_bfs100k.edgelist"

N1 = 20_000
N2 = 100_000

print("📘 Reading edges and building adjacency list (streaming) ...")

adj = defaultdict(list)
nodes_seen = set()

with open(EDGE_PATH, "r") as f:
    for line in f:
        if line.startswith("#") or not line.strip():
            continue
        u, v = map(int, line.split())
        adj[u].append(v)
        adj[v].append(u)   # roadNet 是无向语义
        nodes_seen.add(u)
        nodes_seen.add(v)

print(f"✔ Loaded graph: nodes≈{len(nodes_seen)}, edges≈{sum(len(v) for v in adj.values())//2}")

# -------------------------------------------------------
# 1️⃣ 选择一个 seed（这里用第一个出现的节点）
# -------------------------------------------------------
seed = next(iter(nodes_seen))
print(f"🌱 BFS seed node: {seed}")

# -------------------------------------------------------
# 2️⃣ BFS 扩展，直到 ≥100k
# -------------------------------------------------------
visited = set([seed])
queue = deque([seed])

order = [seed]

print("🚶 Running BFS ...")

while queue and len(order) < N2:
    u = queue.popleft()
    for v in adj[u]:
        if v not in visited:
            visited.add(v)
            queue.append(v)
            order.append(v)
            if len(order) >= N2:
                break

print(f"✔ BFS done: collected {len(order)} nodes")

nodes_20k = set(order[:N1])
nodes_100k = set(order[:N2])

# -------------------------------------------------------
# 3️⃣ 写 edgelist（诱导子图）
# -------------------------------------------------------
def write_subgraph(nodes_set, out_path):
    with open(out_path, "w") as f:
        cnt = 0
        for u in nodes_set:
            for v in adj[u]:
                if v in nodes_set and u < v:
                    f.write(f"{u} {v}\n")
                    cnt += 1
    print(f"✔ Wrote {out_path}: nodes={len(nodes_set)}, edges≈{cnt}")

write_subgraph(nodes_20k, OUT_20K)
write_subgraph(nodes_100k, OUT_100K)

print("🎉 Done.")
