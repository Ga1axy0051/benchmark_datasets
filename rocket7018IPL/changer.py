import pandas as pd
import re
import os

cch_path = r"D:\benchmark_datasets\rocket7018IPL\7018.cch"
al_path = r"D:\benchmark_datasets\rocket7018IPL\7018.al"

def process_data():
    # 1. 加载节点特征 (Node Features)
    print("正在加载并合并节点特征...")
    if not os.path.exists(al_path):
        print(f"错误: 找不到文件 {al_path}")
        return

    # 读取 AL 文件，提取 uid, ip, hostname
    nodes_df = pd.read_csv(al_path, sep=r'\s+', header=None, names=['node_id', 'ip', 'hostname'], usecols=[0, 1, 2], engine='python')
    # 一个 UID 可能对应多个 IP，去掉重复的 UID，保留第一条记录作为特征
    nodes_df = nodes_df.drop_duplicates('node_id').reset_index(drop=True)

    # 2. 提取边关系 (Edges)
    print("正在从 CCH 文件提取边关系...")
    edges = []
    
    # 正则表达式：匹配可选的负号后面跟着数字
    id_pattern = re.compile(r'-?\d+')

    with open(cch_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            parts = line.strip().split()
            if not parts: continue
            
            try:
                # 提取行首的源节点 UID
                u_match = id_pattern.search(parts[0])
                if not u_match: continue
                u = abs(int(u_match.group()))

                # 根据 README.cch，邻居节点在 '->' 符号之后
                if '->' in parts:
                    neighbors_start = parts.index('->') + 1
                    for v_str in parts[neighbors_start:]:
                        # 使用正则提取邻居 ID
                        v_match = id_pattern.search(v_str)
                        if v_match:
                            v = abs(int(v_match.group()))
                            edges.append({'source': u, 'target': v})
            except Exception as e:
                # 如果某行格式实在太怪异，跳过并打印调试信息
                # print(f"跳过第 {line_num} 行，原因: {e}")
                continue

    edges_df = pd.DataFrame(edges)

    # 3. 保存结果
    nodes_df.to_csv('rocket_7018_nodes.csv', index=False)
    # 去重，防止双向边或重复定义导致冗余
    edges_df = edges_df.drop_duplicates().reset_index(drop=True)
    edges_df.to_csv('rocket_7018_edges.csv', index=False)

    print(f"\n[处理完成]！")
    print(f"节点特征表: rocket_7018_nodes.csv (共 {len(nodes_df)} 个唯一节点)")
    print(f"边关系表: rocket_7018_edges.csv (共 {len(edges_df)} 条边)")

if __name__ == "__main__":
    process_data()