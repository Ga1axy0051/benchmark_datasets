import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.ipc as ipc
import pickle
import os

def convert_citeseer():
    arrow_path = "/home/guoquanjiang/WXY/benchmark_datasets/citeseer/default/0.0.0/8b681d9d02adc4733bf1c09cfaea4a06563a2b51/citeseer-train.arrow"
    output_dir = "/home/guoquanjiang/WXY/benchmark_datasets/CiteSeer"
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print(f"--- 正在解析 Arrow 流文件: {os.path.basename(arrow_path)} ---")
    
    # 1. 强制使用 IPC Stream 模式读取
    try:
        with pa.memory_map(arrow_path, 'r') as source:
            # 尝试作为 Stream 打开
            try:
                reader = ipc.open_stream(source)
                table = reader.read_all()
            except:
                # 如果不是 Stream，尝试作为 File 打开
                source.seek(0)
                reader = ipc.open_file(source)
                table = reader.read_all()
    except Exception as e:
        print(f"❌ 读取失败: {e}")
        return

    # 2. 提取数据（取第一行示例）
    data = table.to_pylist()[0]

    # 根据 JSON 结构提取：CiteSeer 特征通常在 'distances' 字段
    features = np.array(data['distances']) 
    labels = np.array(data['classification_labels'])
    adj_matrix = np.array(data['adjacency'])
    
    num_nodes = features.shape[0]
    print(f"✅ 解析成功！节点: {num_nodes}, 特征: {features.shape[1]}, 标签数: {len(np.unique(labels))}")

    # 3. 构造 CSV Table
    df = pd.DataFrame(features, columns=[f"feat_{i}" for i in range(features.shape[1])])
    df.insert(0, 'node_id', range(num_nodes))
    df['target_label'] = labels
    
    csv_path = os.path.join(output_dir, "citeseer_full_table.csv")
    df.to_csv(csv_path, index=False)
    print(f"✅ CSV Table 已保存: {csv_path}")

    # 4. 转换邻接矩阵为邻接字典 (ind.graph)
    adj_dict = {i: [] for i in range(num_nodes)}
    rows, cols = np.where(adj_matrix > 0)
    for r, c in zip(rows, cols):
        adj_dict[int(r)].append(int(c))
    
    graph_path = os.path.join(output_dir, "ind.citeseer.graph")
    with open(graph_path, 'wb') as f:
        pickle.dump(adj_dict, f)
    print(f"✅ Graph 拓扑已保存: {graph_path}")

if __name__ == "__main__":
    convert_citeseer()