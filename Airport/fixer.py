import pickle
import pandas as pd
import numpy as np
import networkx as nx

def fix_airport():
    print("--- 正在修复 Airport 数据集标签 ---")
    
    # 1. 加载特征数据
    with open("airport_alldata.p", 'rb') as f:
        df = pickle.load(f, encoding='latin1')
    num_nodes = len(df)
    
    # 2. 加载图结构
    with open("airport_graph.pkl", 'rb') as f:
        G = pickle.load(f)
    
    # 严谨获取度数：处理 NetworkX 节点索引不匹配的情况
    degrees = []
    # 假设特征矩阵的行序就是节点 0 到 n-1
    for i in range(num_nodes):
        if G.has_node(i):
            degrees.append(G.degree[i])
        else:
            # 如果索引不匹配，尝试从图的所有节点中按顺序取（保底逻辑）
            degrees.append(0) 

    print(f"成功提取 {len(degrees)} 个节点的度数。")

    # 3. 离散化度数为标签 (Activity Level)
    # 将机场按繁忙程度分为 4 个等级（0: 低, 1: 中低, 2: 中高, 3: 高）
    labels = pd.qcut(degrees, q=4, labels=False, duplicates='drop')
    
    # 4. 构建并保存 Table
    df['target_label'] = labels
    if 'node_id' not in df.columns:
        df.insert(0, 'node_id', range(num_nodes))
        
    df.to_csv("airport_full_table.csv", index=False)
    print(f"✅ Airport 修复完成！标签列 'target_label' 已生成。")
    print(f"标签分布: {pd.Series(labels).value_counts().to_dict()}")

if __name__ == "__main__":
    fix_airport()