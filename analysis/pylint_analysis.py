log_file_path = '../src/pylint.log'

if __name__ == '__main__':
    # 用于存储错误类型及其详细信息的字典
    error_details = {}

    with open(log_file_path, 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line and not line.startswith('***') and not line.startswith('----'):
                parts = line.split(':')
                if len(parts) >= 4:
                    error_code = parts[3].strip().split(' ')[0]
                    if error_code == 'R0801':  # 处理代码重复错误
                        file_path = parts[0].strip()
                        line_no = parts[1].strip()
                        # 初始化错误描述，包括错误代码行本身
                        description = [line]
                        i += 1  # 移动到下一行，开始收集相似行信息
                        # 收集相似代码段，直到遇到下一个错误代码或文件末尾
                        while i < len(lines) and (
                            not lines[i].strip() or lines[i].startswith('    ') or
                            lines[i].startswith('==')):
                            description.append(lines[i].rstrip())  # 使用rstrip删除行尾的空白字符
                            i += 1
                        # 不需要回退一行，因为我们想从下一个非空白行开始处理
                        detail = {'file': file_path, 'line': line_no,
                                  'description': '\n'.join(description)}
                        error_type = 'R0801'
                        i-=1
                    else:
                        file_path = parts[0].strip()
                        line_no = parts[1].strip()
                        description = ':'.join(parts[3:]).strip()  # 保留完整的错误描述
                        detail = {'file': file_path, 'line': line_no,
                                  'description': description}
                        error_type = error_code

                    if error_type not in error_details:
                        error_details[error_type] = [detail]
                    else:
                        error_details[error_type].append(detail)
            i += 1

    # 文件名定义
    output_file_path = 'pylint_errors_summary.txt'

    # 使用'with'语句打开文件，确保文件最后被正确关闭
    with open(output_file_path, 'w') as output_file:
        # 遍历归类后的错误信息并写入文件
        for error_code, details in error_details.items():
            print(f"Error Type: {error_type}")
            output_file.write(f"Error Code: {error_code}\n")
            for detail in details:
                print(
                    f"  File: {detail['file']}, Line: {detail['line']}, Description: {detail['description']}")

                output_file.write(
                    f"  File: {detail['file']}, Line: {detail['line']}, Description: {detail['description']}\n")
            output_file.write("----------\n")
            print("----------")

    print(f"Errors have been successfully written to {output_file_path}")
