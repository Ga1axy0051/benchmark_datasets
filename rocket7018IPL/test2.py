import pandas as pd
import os

# 定义文件路径
cch_path = r"D:\benchmark_datasets\rocket7018IPL\7018.cch"
al_path = r"D:\benchmark_datasets\rocket7018IPL\7018.al"

def check_full_correspondence(cch_file, al_file):
    print(f"--- 正在验证全量数据对应关系 ---")
    
    # 1. 加载 AL 特征库
    # 列名依次为 uid, ip, hostname
    print("正在加载 AL 特征库...")
    al_df = pd.read_csv(al_file, sep=r'\s+', header=None, names=['uid', 'ip', 'hostname'], usecols=[0, 1, 2], engine='python')
    al_uids = set(al_df['uid'].unique())
    print(f"AL 文件中共包含 {len(al_uids)} 个唯一路由器 UID。")

    # 2. 提取 CCH 文件中的所有节点 UID
    print("正在提取 CCH 文件中的节点...")
    cch_uids = set()
    try:
        with open(cch_file, 'r') as f:
            for line in f:
                line = line.strip()
                if not line: continue
                # 提取第一列的 UID，并取绝对值（处理负号逻辑）
                raw_id = line.split()[0]
                try:
                    cch_uids.add(abs(int(raw_id)))
                except ValueError:
                    continue # 跳过非数字行
        print(f"CCH 文件中共找到 {len(cch_uids)} 个唯一节点。")
    except Exception as e:
        print(f"读取 CCH 文件失败: {e}")
        return

    # 3. 计算交集和匹配率
    matched_uids = cch_uids.intersection(al_uids)
    match_count = len(matched_uids)
    match_rate = (match_count / len(cch_uids)) * 100 if cch_uids else 0

    print(f"\n--- 匹配统计结果 ---")
    print(f"成功匹配的节点数: {match_count}")
    print(f"匹配率: {match_rate:.2f}%")

    if match_rate > 90:
        print("\n[结论] 验证通过！7018.cch 与 7018.al 几乎完全对应。")
        print("你可以放心地使用 .al 文件作为节点的 Feature 来源。")
    elif match_count > 0:
        print(f"\n[结论] 部分对应。CCH 中有 {match_count} 个节点可以找到特征。")
    else:
        print("\n[警告] 无法匹配任何节点。请检查 ID 转换逻辑或文件完整性。")

    # 4. 展示前 5 个匹配到的节点及其特征预览
    if match_count > 0:
        print("\n--- 匹配节点特征预览 (前5个) ---")
        sample_ids = list(matched_uids)[:5]
        preview = al_df[al_df['uid'].isin(sample_ids)].drop_duplicates('uid')
        print(preview[['uid', 'ip', 'hostname']])

if __name__ == "__main__":
    check_full_correspondence(cch_path, al_path)