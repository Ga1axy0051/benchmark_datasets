import networkx as nx
import pickle

# 1. 加载 .gpickle 文件
file_path = '/home/guoquanjiang/WXY/benchmark_datasets/telecom/TeleGraph.gpickle'
with open(file_path, 'rb') as f:
    G = pickle.load(f)

# 2. 查看图的基本统计信息
print(f"图类型: {type(G)}")
print(f"节点数: {G.number_of_nodes()}")
print(f"边数: {G.number_of_edges()}")

# 3. 检查节点是否存在特征 (feature)
# 获取第一个节点的 ID
sample_node = list(G.nodes())[0]
# 打印该节点的所有属性
print(f"\n节点 [{sample_node}] 的属性字典: {G.nodes[sample_node]}")

# 4. 逻辑判断
if len(G.nodes[sample_node]) > 0:
    print("\n结论：该文件包含节点特征！")
    print(f"特征键名（Keys）: {list(G.nodes[sample_node].keys())}")
else:
    print("\n结论：该文件不包含节点特征，仅有图结构。")