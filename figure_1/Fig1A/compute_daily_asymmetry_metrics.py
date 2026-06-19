
import os
import pandas as pd
import numpy as np
import time
import warnings

# 忽略可能的除以0警告
warnings.filterwarnings('ignore')

# ========== 1. 统计指标计算函数 (保持不变) ==========

def calculate_gini(flows):
    """计算基尼系数 (Gini Coefficient)"""
    flows = np.array(flows).flatten()
    flows = flows[flows > 0]
    if len(flows) < 2: return 0.0
    flows_sorted = np.sort(flows)
    n = len(flows_sorted)
    index = np.arange(1, n + 1)
    gini = (2 * np.sum(index * flows_sorted)) / (n * np.sum(flows_sorted)) - (n + 1) / n
    return max(0.0, gini)

def calculate_cv(flows):
    """计算变异系数 (Coefficient of Variation)"""
    flows = np.array(flows).flatten()
    flows = flows[flows > 0]
    if len(flows) < 2 or np.mean(flows) == 0: return 0.0
    return np.std(flows) / np.mean(flows)

# ========== 2. 设置路径 ==========
# 输入文件夹：下面应该包含16个城市的子文件夹
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
input_root_folder = os.path.join(SCRIPT_DIR, "real_year")
output_folder = SCRIPT_DIR
os.makedirs(output_folder, exist_ok=True)

# 获取所有城市的子文件夹
city_folders = [d for d in os.listdir(input_root_folder) if os.path.isdir(os.path.join(input_root_folder, d))]

# 结果存储列表
city_stats_summary = []

print(f"🚀 准备处理 {len(city_folders)} 个城市的每日数据 (计算均值与标准差)...")

# ========== 3. 主循环 (遍历城市) ==========
for city_name in city_folders:
    city_start_time = time.time()
    city_dir_path = os.path.join(input_root_folder, city_name)
    
    # 获取该城市下的所有每日CSV文件
    daily_files = [f for f in os.listdir(city_dir_path) if f.endswith(".csv")]
    
    print(f"\n🏙️ 正在处理城市: {city_name} (共 {len(daily_files)} 天数据)")
    
    # 存储该城市每一天的指标
    daily_metrics_list = []
    
    # ========== 4. 内层循环 (遍历每一天) ==========
    for i, day_file in enumerate(daily_files):
        # 简单的进度显示
        if i % 50 == 0:
            print(f"   进度: {i}/{len(daily_files)}...")
            
        day_path = os.path.join(city_dir_path, day_file)
        
        try:
            # 读取每日矩阵
            # 注意：每日矩阵可能比较稀疏
            df = pd.read_csv(day_path, index_col=0)
            matrix = df.apply(pd.to_numeric, errors='coerce').fillna(0).values
            
            # 形状检查
            if matrix.shape[0] != matrix.shape[1]:
                # 如果非方阵，尝试截断到最小维度
                min_dim = min(matrix.shape)
                matrix = matrix[:min_dim, :min_dim]
            
            # [关键] 去除对角线 (社区内部流动)
            np.fill_diagonal(matrix, 0)
            
            # --- 计算该日的指标 ---
            
            # A. 整体不对称性
            matrix_t = matrix.T
            diff_matrix = np.abs(matrix - matrix_t)
            sum_matrix = matrix + matrix_t
            
            total_diff = np.sum(diff_matrix)
            total_flow = np.sum(sum_matrix)
            
            if total_flow > 0:
                daily_asymmetry = total_diff / total_flow
            else:
                daily_asymmetry = np.nan # 如果某天没流量，设为NaN不参与统计
            
            # B. 基尼系数与变异系数
            # 展平并只取非零值
            all_flows = matrix.flatten()
            if np.sum(all_flows) > 0:
                daily_gini = calculate_gini(all_flows)
                daily_cv = calculate_cv(all_flows)
            else:
                daily_gini = np.nan
                daily_cv = np.nan
                
            # 记录该日结果
            daily_metrics_list.append({
                "day_asymmetry": daily_asymmetry,
                "day_gini": daily_gini,
                "day_cv": daily_cv,
                "daily_total_flow": total_flow / 2 # 真实流量是 sum_matrix 的一半
            })
            
        except Exception as e:
            # 个别文件损坏不应中断整个程序
            print(f"   ⚠️ 读取文件 {day_file} 失败: {e}")
            continue
            
    # ========== 5. 聚合该城市的统计特征 ==========
    
    if len(daily_metrics_list) > 0:
        # 转换为DataFrame方便计算统计量
        df_metrics = pd.DataFrame(daily_metrics_list)
        
        # 计算均值 (Mean) 和 标准差 (Std)
        # skipna=True 会自动忽略上面设置的 NaN
        stats = {
            "city_name": city_name,
            "days_count": len(df_metrics), # 成功处理的天数
            
            # 不对称性
            "asymmetry_mean": df_metrics["day_asymmetry"].mean(),
            "asymmetry_std": df_metrics["day_asymmetry"].std(),
            
            # 基尼系数
            "gini_mean": df_metrics["day_gini"].mean(),
            "gini_std": df_metrics["day_gini"].std(),
            
            # 变异系数
            "cv_mean": df_metrics["day_cv"].mean(),
            "cv_std": df_metrics["day_cv"].std(),
            
            # 平均日流量
            "daily_flow_mean": df_metrics["daily_total_flow"].mean()
        }
        
        city_stats_summary.append(stats)
        
        elapsed = time.time() - city_start_time
        print(f"✅ {city_name} 完成! Mean Asym: {stats['asymmetry_mean']:.4f} ± {stats['asymmetry_std']:.4f} (耗时 {elapsed:.1f}s)")
    else:
        print(f"❌ {city_name} 没有有效数据。")

# ========== 6. 保存最终汇总 ==========
final_df = pd.DataFrame(city_stats_summary)
final_df = final_df.sort_values(by="asymmetry_mean", ascending=False)

output_path = os.path.join(output_folder, "Fig1A_Daily_Stats_With_ErrorBars.csv")
final_df.to_csv(output_path, index=False, encoding="utf-8-sig")

print("\n" + "="*50)
print(f"🎉 所有处理完成！结果已保存至: {output_path}")
print("此文件包含用于绘制 Figure 1A 误差棒的关键数据：")
print("- asymmetry_mean, asymmetry_std")
print("- gini_mean, gini_std")
print("- cv_mean, cv_std")
print("="*50)