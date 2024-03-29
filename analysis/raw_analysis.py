import re

def parse_radonraw_output(input_file_path, output_file_path):
    # 使用正则表达式匹配文件名和各种统计信息
    file_pattern = re.compile(r'^(\S+)')
    stats_pattern = re.compile(r'^\s+(\S+):\s+(\d+)')
    comment_stats_pattern = re.compile(r'\s+\((C % L|C % S|C \+ M % L)\):\s+(\d+)%')

    results = {}

    with open(input_file_path, 'r') as input_file:
        current_file = ''
        for line in input_file:
            # 检查是否是新文件的开始
            file_match = file_pattern.match(line)
            if file_match:
                current_file = file_match.group(1)
                results[current_file] = {'Comment Stats': {}}
            else:
                # 匹配统计信息
                stats_match = stats_pattern.match(line)
                if stats_match:
                    results[current_file][stats_match.group(1)] = stats_match.group(2)
                else:
                    # 匹配注释统计信息
                    comment_stats_match = comment_stats_pattern.match(line)
                    if comment_stats_match:
                        results[current_file]['Comment Stats'][comment_stats_match.group(1)] = comment_stats_match.group(2) + '%'

    # 写入到输出文件并打印结果
    with open(output_file_path, 'w') as output_file:
        for file, stats in results.items():
            output_file.write(f"{file}\n")
            print(f"{file}")
            for stat, value in stats.items():
                if stat != 'Comment Stats':
                    output_file.write(f"    {stat}: {value}\n")
                    print(f"    {stat}: {value}")
                else:
                    output_file.write(f"    - Comment Stats\n")
                    print(f"    - Comment Stats")
                    for comment_stat, comment_value in value.items():
                        output_file.write(f"        {comment_stat}: {comment_value}\n")
                        print(f"        {comment_stat}: {comment_value}")
            output_file.write("\n")
            print()

# 定义输入和输出文件路径
input_file_path = '../src/radonraw.log'
output_file_path = 'raw_analysis.txt'

# 调用函数
parse_radonraw_output(input_file_path, output_file_path)
