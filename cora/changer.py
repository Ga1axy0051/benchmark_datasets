import pickle
import numpy as np
import pandas as pd
import sys
import os

def load_cora_to_csv(dataset_path="/home/guoquanjiang/WXY/benchmark_datasets/cora/"):
    # 明确定义加载函数，处理 scipy 稀疏矩阵
    def load_pickle(name):
        path = os.path.join(dataset_path, f"ind.cora.{name}")
        with open(path, 'rb') as f:
            if sys.version_info > (3, 0):
                return pickle.load(f, encoding='latin1')
            return pickle.load(f)

    def to_array(m):
        return m.toarray() if hasattr(m, "toarray") else m

    print("--- 正在加载原始文件 ---")
    # 1. 只有这些是 pickle 格式
    x = load_pickle('x')
    y = load_pickle('y')
    tx = load_pickle('tx')
    ty = load_pickle('ty')
    allx = load_pickle('allx')
    ally = load_pickle('ally')

    # 2. index 文件是纯文本，直接用 numpy 加载
    index_path = os.path.join(dataset_path, "ind.cora.test.index")
    index = np.loadtxt(index_path, dtype=np.int32)
    print(f"Index 加载成功，长度: {len(index)}")

    # 3. 转换为密集阵
    allx_dense = to_array(allx)
    tx_dense = to_array(tx)
    ally_dense = to_array(ally)
    ty_dense = to_array(ty)

    # 4. 核心逻辑：还原测试集顺序
    # Planetoid 格式中，allx 是训练+无标签数据，tx 是测试数据，其位置由 index 指定
    max_idx = max(index)
    total_nodes = max(max_idx + 1, allx_dense.shape[0] + tx_dense.shape[0])
    
    full_features = np.zeros((total_nodes, allx_dense.shape[1]))
    full_labels = np.zeros((total_nodes, ally_dense.shape[1]))

    # 填充 non-test 部分
    full_features[:allx_dense.shape[0], :] = allx_dense
    full_labels[:ally_dense.shape[0], :] = ally_dense

    # 填充 test 部分 (根据 index 映射)
    full_features[index, :] = tx_dense
    full_labels[index, :] = ty_dense

    # 5. 导出为 Table
    df = pd.DataFrame(full_features)
    # 将 One-hot 转换为单列数字标签 (TODO 4: Node Classification [cite: 49, 50])
    df['target_label'] = np.argmax(full_labels, axis=1)
    
    output_path = os.path.join(dataset_path, "cora_full_table.csv")
    df.to_csv(output_path, index_label="node_id")
    
    print(f"--- 转换完成 ---")
    print(f"节点总数: {total_nodes}")
    print(f"保存路径: {output_path}")

if __name__ == "__main__":
    load_cora_to_csv()