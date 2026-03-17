import pandas as pd
import pickle
import numpy as np
import os

def check_data_integrity():
    csv_path = "citeseer_full_table.csv"
    graph_path = "ind.citeseer.graph"
    
    if not os.path.exists(csv_path) or not os.path.exists(graph_path):
        print("❌ 错误：找不到文件，请确保在 CiteSeer 数据集目录下运行。")
        return

    # 1. 检查加载
    df = pd.read_csv(csv_path)
    with open(graph_path, 'rb') as f:
        adj = pickle.load(f)
        
    print(f"\n" + "="*40)
    print(f"📊 CiteSeer 数据集严谨性报告")
    print(f"="*40)
    print(f"节点总数 (CSV): {len(df)}")
    print(f"图邻接表大小: {len(adj)}")
    
    # 2. 检查特征
    feat_cols = [c for c in df.columns if 'feat' in c]
    print(f"特征列数: {len(feat_cols)}")
    
    # 核心诊断：检查特征矩阵是否全是 0
    feat_matrix = df[feat_cols].values
    total_non_zero = np.count_nonzero(feat_matrix)
    sparsity = 100 * (1 - total_non_zero / feat_matrix.size)
    print(f"特征稀疏度: {sparsity:.2f}%")
    
    avg_val = feat_matrix.mean()
    print(f"特征平均值: {avg_val:.6f}")
    
    # 3. 检查标签分布
    label_counts = df['target_label'].value_counts().to_dict()
    print(f"标签类别分布: {label_counts}")
    
    # 4. 检查边结构
    edge_count = sum(len(v) for v in adj.values())
    print(f"总边数: {edge_count}")
    
    if edge_count == 0:
        print("❌ 致命警告：图中没有边！卷积层将无法学习。")
    if avg_val < 1e-7:
        print("❌ 致命警告：特征几乎全为 0！模型输入全是噪声。")

if __name__ == "__main__":
    check_data_integrity()