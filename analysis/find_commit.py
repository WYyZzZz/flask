import subprocess
import pandas as pd
import csv
from datetime import datetime

def get_date(date_str):
    parts = date_str.split(' ')

    # 根据分割的部分构造所需的日期格式
    # parts[1] 是月份, parts[2] 是日期, parts[4] 是年份
    return f"{parts[1]} {parts[2]} {parts[4]}"

# 读取CSV文件
output_csv_path = 'commit2017.csv'
csv_file_path = '2017.csv'  # CSV文件路径
df = pd.read_csv(csv_file_path)


# 将日期列转换为日期时间对象，确保没有时间偏移
df['date'] = pd.to_datetime(df['date']).dt.tz_localize(None)

# 准备输出文件
with open(output_csv_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # 写入表头
    writer.writerow(['Hash', 'Author', 'Date', 'Message'])

    for date in df['date']:
        date_str = date.strftime('%Y-%m-%d')
        git_command = [
            'git', 'log', '--numstat',
            '--since="{} 00:00:00"'.format(date_str),
            '--until="{} 23:59:59"'.format(date_str),
            '--pretty=format:CommitHash:%H,Author:%an,Date:%ad,Message:%s',
            '--date=local'
        ]

        try:
            result = subprocess.run(git_command, cwd="..", stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, text=True, check=True)
            commit_lines = result.stdout.split('\n')
            commit_info = {}
            for line in commit_lines:
                if line.startswith('CommitHash:'):
                    # 当遇到新的提交时，如果之前已经解析了一个提交，先保存它
                    if commit_info:
                        # 写入到CSV
                        writer.writerow([commit_info['hash'], commit_info['author'],
                                         commit_info['date'], commit_info['message'],])
                        commit_info = {}  # 重置提交信息

                    # 解析基础信息
                    parts = line.split(',')
                    commit_info = {
                        'hash': parts[0].split(':')[1],
                        'author': parts[1].split(':')[1],
                        'date': get_date(parts[2]),
                        'message': ','.join(parts[3:]).split('Message:')[
                            1] if 'Message:' in line else '',
                    }

        except subprocess.CalledProcessError as e:
            print(f"Error running git log for date {date_str}:\n{e.stderr}")
