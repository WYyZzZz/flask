import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import subprocess
import pandas as pd

# 使用Git命令获取每次提交的统计信息和日期
cmd = 'git log --pretty=format:"%ad" --date=short --numstat'
result = subprocess.check_output(cmd, shell=True).decode('utf-8')

# 解析输出，创建一个包含新增、删除行数、日期和净增加的数据框
lines = result.strip().split('\n')
data = []
current_date = None
for line in lines:
    if '-' in line and len(line) == 10:  # 这是日期行的一个简单检查
        current_date = line
    else:
        parts = line.split('\t')
        if len(parts) == 3:  # 确保这一行有足够的部分来解包
            additions, deletions, _ = parts
            # 检查是否为'-'，如果是，则替换为0
            additions = 0 if additions == '-' else int(additions)
            deletions = 0 if deletions == '-' else int(deletions)
            net_increase = additions - deletions
            data.append([current_date, net_increase])

df = pd.DataFrame(data, columns=['Date', 'Net Increase'])

# 将字符串日期转换为日期类型，并设置为索引
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

# 确保日期索引是单调的
df = df.sort_index()

# 筛选2016-2018年间的数据
df_filtered = df.loc['2016-01-01':'2018-12-31']

# 累积净增加
df_cumulative = df_filtered.cumsum()

# 绘制累积的行数净增加
df_cumulative.plot()
plt.xlabel('Date')
plt.ylabel('Net Lines of Code Added')
plt.title('Net Git Repository Code Changes (2016-2018)')
plt.xticks(rotation=45)  # 旋转日期标签以便阅读
plt.tight_layout()  # 调整布局以防止标签被截断

plt.savefig('git_code_changes.png')
