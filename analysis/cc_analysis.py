def parse_radoncc_output(file_path):
    # 初始化存储结构
    parsed_results = {}

    # 打开并读取文件
    with open(file_path, 'r') as file:
        lines = file.readlines()

    current_file = None

    summary_started = False  # 标记是否开始处理总结信息

    for line in lines:
        line = line.strip()
        if not line:
            summary_started = True  # 遇到空行，下一部分可能是总结信息
            parsed_results['summary'] = []
            continue

        if summary_started:
            parsed_results['summary'].append(line)

        else:
            if line and not line.startswith('    '):
                # 这是一个新文件的开始
                current_file = line
                parsed_results[current_file] = []
            else:
                # 这是当前文件的一个代码块条目
                parts = line.split(' ')
                if len(parts) > 3:  # 确保行是代码块条目格式
                    block_type = parts[0]  # 类型：F、M或C
                    line_no = parts[1]  # 行号
                    name = ' '.join(parts[2:-3])  # 代码块名称
                    complexity_grade = parts[-3]  # 复杂度等级，如A、B、C、D
                    complexity_score = parts[-2] + parts[-1]  # 复杂度得分，如(5)
                    parsed_results[current_file].append({
                        'type': block_type,
                        'line_no': line_no,
                        'name': name,
                        'complexity_grade': complexity_grade,
                        'complexity_score': complexity_score
                    })

    # 返回解析结果
    return parsed_results
def print_parsed_results_with_summary(parsed_results, output_file_path):
    with open(output_file_path, 'w') as file:
        # 遍历解析结果，打印并写入到文件
        for key, value in parsed_results.items():
            if key == 'summary':
                # 打印并写入总结信息
                file.write("Summary:\n")
                print("Summary:")
                for summary_line in value:
                    file.write(f"{summary_line}\n")
                    print(summary_line)
            else:
                # 打印并写入文件的代码块信息
                file.write(f"{key}\n")
                print(f"{key}")
                for block in value:
                    block_info = f"  Type: {block['type']}, Line No: {block['line_no']}, Name: {block['name']}, Complexity Grade: {block['complexity_grade']}, Complexity Score: {block['complexity_score']}"
                    file.write(f"{block_info}\n")
                    print(block_info)
            file.write("\n")
            print()


# 假设这是你的文件路径
input_file_path = '../src/radoncc.log'
output_file_path = 'cc_analysis.txt'
# 解析radoncc输出
parsed_results = parse_radoncc_output(input_file_path)

# 打印解析结果并将其保存到文件
print_parsed_results_with_summary(parsed_results, output_file_path)
