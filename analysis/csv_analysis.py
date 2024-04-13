import pandas as pd

# 读取CSV文件
file_path = 'commits history.csv'  # 将这里的路径替换为你的CSV文件路径
df = pd.read_csv(file_path)

df['date'] = pd.to_datetime(df['date'], utc=True)


# 筛选2016到2018年间的数据
df_filtered = df[(df['date'].dt.year >= 2016) & (df['date'].dt.year <= 2018)]

# 找出delta最大和最小的20项
df_sorted = df_filtered.sort_values(by='delta', ascending=False)
filtered_by_delta = df_sorted[df_sorted['delta'] > 100]

# 合并结果
result_df = pd.concat([filtered_by_delta])

# 输出到CSV文件
output_path = '2017.csv'  # 你希望输出的CSV文件路径
result_df.to_csv(output_path, index=False)

print("处理完成，结果已输出到:", output_path)


