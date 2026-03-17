import pickle
import pandas as pd
import numpy as np
import os

# --- 路径配置 ---
FEAT_FILE = "airport_alldata.p"
LABEL_FILE = "airport.p"
EDGE_FILE = "airport_edgelist.txt"
OUTPUT_CSV = "airport_full_table.csv"
OUTPUT_GRAPH = "ind.airport.graph"

def construct_airport_dataset():
    print("--- 开始严谨转换 Airport 数据集 ---")

    # 1. 提取特征 (Features)
    if not os.path.exists(FEAT_FILE):
        print(f"错误: 找不到特征文件 {FEAT_FILE}")
        return
    
    with open(FEAT_FILE, 'rb') as f:
        df_feat = pickle.load(f, encoding='latin1')
    
    # 将数字列名转换为字符串，并保留 'gdp', 'pop' 等统计特征
    df_feat.columns = [f"feat_{c}" if isinstance(c, int) else c for c in df_feat.columns]
    num_nodes = len(df_feat)
    print(f"1. 特征加载成功: {num_nodes} 节点, {df_feat.shape[1]} 维特征")

    # 2. 提取标签 (Labels)
    labels = None
    if os.path.exists(LABEL_FILE):
        with open(LABEL_FILE, 'rb') as f:
            data_dict = pickle.load(f, encoding='latin1')
            # 标准 HGCN/HGNN 格式中标签存在字典的 'labels' 或 'y' 键下
            if isinstance(data_dict, dict):
                labels = data_dict.get('labels', data_dict.get('y'))
            elif isinstance(data_dict, (np.ndarray, list)):
                labels = data_dict
    
    if labels is not None:
        # 确保标签长度与节点数匹配
        labels = np.array(labels).flatten()[:num_nodes]
        df_feat['target_label'] = labels
        print(f"2. 标签加载成功: 唯一类别数 {len(np.unique(labels))}")
    else:
        print("警告: 未能在 airport.p 中找到标签列，请检查文件内容。")

    # 3. 插入 node_id 并生成 CSV
    if 'node_id' not in df_feat.columns:
        df_feat.insert(0, 'node_id', range(num_nodes))
    
    df_feat.to_csv(OUTPUT_CSV, index=False)
    print(f"3. Table 数据已保存: {OUTPUT_CSV}")

    # 4. 构建并保存图结构 (Graph)
    # 用于对接你之前的 HGCN/HGNN/HGAT 基准脚本
    if os.path.exists(EDGE_FILE):
        adj_dict = {i: [] for i in range(num_nodes)}
        with open(EDGE_FILE, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    u, v = int(parts[0]), int(parts[1])
                    if u < num_nodes and v < num_nodes:
                        adj_dict[u].append(v)
                        adj_dict[v].append(u) # 无向图处理
        
        with open(OUTPUT_GRAPH, 'wb') as f:
            pickle.dump(adj_dict, f)
        print(f"4. 图拓扑结构已保存: {OUTPUT_GRAPH}")

if __name__ == "__main__":
    construct_airport_dataset()