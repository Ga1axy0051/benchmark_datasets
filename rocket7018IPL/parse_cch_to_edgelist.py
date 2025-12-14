# parse_cch_to_edgelist.py
import re

edges = set()

with open("7018.r1.cch") as f:
    for line in f:
        # 行首必须是正 uid
        m = re.match(r"^(\d+)", line)
        if not m:
            continue
        u = int(m.group(1))

        # 找所有 <v>
        vs = re.findall(r"<(\d+)>", line)
        for v in vs:
            v = int(v)
            if u != v:
                # 无向图，去重
                edges.add(tuple(sorted((u, v))))

with open("7018_edgelist.txt", "w") as f:
    for u, v in edges:
        f.write(f"{u} {v}\n")

print(f"Edges: {len(edges)}")
