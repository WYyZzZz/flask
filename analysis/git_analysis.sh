#!/bin/bash

# 设置输出的CSV文件名
output_csv="gitlog.csv"

# 写入CSV头部
echo "Timestamp,Message,Committer,Added,Removed,File" > "$output_csv"

# 使用git log命令提取所需信息并追加到CSV文件
git log --numstat --pretty=format:'%ad,%s,%cn' --date=format:'%Y-%m-%d %H:%M:%S' |
awk 'BEGIN { commit_info=""; file_info="" }
     /^[0-9]{4}-[0-9]{2}-[0-9]{2}/ { if(commit_info != "") print commit_info file_info; commit_info=$0; file_info=""; next }
     /^[0-9]+/ { gsub("\t",","); file_info=$0; print commit_info","file_info; file_info=""; next }' >> "$output_csv"

echo "CSV文件已生成：$output_csv"
