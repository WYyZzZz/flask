import re
from collections import defaultdict

# Cyclomatic Complexity Grade Thresholds
GRADE_THRESHOLDS = {
    'A': (1, 5),
    'B': (6, 10),
    'C': (11, 20),
    'D': (21, 40),
    'E': (41, 100)
}


def parse_log(log_lines):
    # 解析每一行的正则表达式
    pattern = r"^\s*(\w)\s+(\d+):\d+\s+([\w\.]+)\s+-\s+(\w)\s+\((\d+)\)"
    file_pattern = r"^src/flask/(\w+)\.py"
    # 存储解析结果
    parsed_data = defaultdict(list)
    module = None
    for line in log_lines:
        file = re.search(file_pattern, line)
        if file:
            module = file.groups()[0]+'.py'
        match = re.search(pattern, line)
        if match:
            item_type, line_number, name, grade, cc = match.groups()
            parsed_data[grade].append({
                "type": item_type,
                "line_number": int(line_number),
                "name": name,
                "cc": int(cc),
                "module": module
            })
    return parsed_data

# 根据给定的分数等级对日志进行进一步排序
def sort_by_grade(classified_data):
    # 将等级转换为可排序的数值（A最高，随后是B，C，等等）
    grade_order = {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6}
    sorted_data = sorted(classified_data.items(), key=lambda x: grade_order[x[0]])
    return sorted_data

# 对已分类和排序的日志数据按等级再排序



# 数据分类和排序
def classify_and_sort(parsed_data):
    for grade in parsed_data.keys():
        # 按照 CC 值降序排序
        parsed_data[grade].sort(key=lambda x: x['cc'], reverse=True)
    return parsed_data


# Main function to read from log file and process
def process_log_file(log_file_path):
    with open(log_file_path, 'r') as log_file:
        log_lines = log_file.readlines()

    log = parse_log(log_lines)

    classified_data = classify_and_sort(log)

    classified_data = sort_by_grade(classified_data)

    # Print classified data
    for grade, items in classified_data:
        print(f"Grade {grade}:")
        for item in items:
            print(
                f"  {item['type']} {item['line_number']}:0 {item['name']} - {grade} ({item['cc']})")
        print("\n")

if __name__ == '__main__':
    # Replace 'your_log_file.log' with the path to your actual log file
    log_file_path = 'srccc.log'
    process_log_file(log_file_path)

