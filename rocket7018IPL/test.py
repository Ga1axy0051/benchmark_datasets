import pandas as pd
import re

cch_path = r"D:\benchmark_datasets\rocket7018IPL\7018.r1.cch"
al_path = r"D:\benchmark_datasets\rocket7018IPL\7018.al"

# 1. 读取 AL 文件
print("读取 AL 特征库...")
al_df = pd.read_csv(al_path, sep=r'\s+', header=None, names=['uid', 'ip', 'hostname'], usecols=[0, 1, 2], engine='python')

# 2. 读取 CCH 文件的第一行并解析
print("分析 CCH 文件行内容...")
with open(cch_path, 'r') as f:
    line = f.readline().strip()
    print(f"CCH 首行原文: {line}")
    
    # 提取 UID (取绝对值) 和 IP
    # 假设格式是: -8849 =192.205.32.170 r1
    parts = line.split()
    cch_uid_raw = parts[0]
    cch_uid_abs = abs(int(cch_uid_raw))
    
    # 提取 IP (去掉前面的 '=')
    cch_ip = parts[1].replace('=', '')
    
    print(f"提取结果: 原始ID={cch_uid_raw}, 绝对值ID={cch_uid_abs}, IP={cch_ip}")

# 3. 进行交叉比对
print("\n--- 比对结果 ---")

# 检查绝对值 ID
id_match = al_df[al_df['uid'] == cch_uid_abs]
if not id_match.empty:
    print(f"[ID 匹配成功] CCH 的绝对值 ID {cch_uid_abs} 对应 AL 中的主机名: {id_match['hostname'].values[0]}")
else:
    print(f"[ID 匹配失败] AL 中找不到 ID {cch_uid_abs}")

# 检查 IP 地址
ip_match = al_df[al_df['ip'] == cch_ip]
if not ip_match.empty:
    print(f"[IP 匹配成功] CCH 的 IP {cch_ip} 在 AL 中对应的 UID 是: {ip_match['uid'].values[0]}")
    print(f"这说明这个节点的 Feature (主机名) 是: {ip_match['hostname'].values[0]}")
else:
    print(f"[IP 匹配失败] AL 特征库中找不到 IP {cch_ip}")