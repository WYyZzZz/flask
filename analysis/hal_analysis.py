def parse_radonhal_output(file_path):
    # 初始化存储结构
    parsed_results = {}

    # 打开并读取文件
    with open(file_path, 'r') as file:
        for line in file:
            # 分割每一行为文件名和复杂度等级
            parts = line.strip().split(' - ')
            if len(parts) == 2:
                file_name, grade = parts
                parsed_results[file_name] = grade

    # 返回解析结果
    return parsed_results

def print_parsed_results(parsed_results):
    # 打印解析结果
    for file_name, grade in parsed_results.items():
        print(f"File: {file_name}, Complexity Grade: {grade}")

# 假设这是你的文件路径
file_path = '../src/radonhal.log'
parsed_results = parse_radonhal_output(file_path)
print_parsed_results(parsed_results)
