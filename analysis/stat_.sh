#!/bin/bash

# 函数：使用tree命令生成目录树
generate_tree_with_tree() {
    local directory="${1:-.}" # 默认当前目录
    # 检查tree命令是否存在
    if ! command -v tree &> /dev/null; then
        echo "tree命令未找到，请先安装tree。"
        exit 1
    fi

    # 使用tree生成目录树
    tree "$directory"
}

# 调用函数，传入第一个命令行参数（如果有的话）
generate_tree_with_tree "$1"
