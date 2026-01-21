#!/bin/bash

echo "=== 启动开发环境 ==="

# 1. 自动拉取最新的笔记代码
echo "正在拉取最新的笔记源码..."
# 确保在正确的目录
cd "$(dirname "$0")"

# 更新 notebooks_src 到远程最新 (强制覆盖本地任何偶然的修改)
git submodule update --init --recursive --remote --force

# 确保它在 main 分支的最新 commit 上
if [ -d "notebooks_src" ]; then
    cd notebooks_src
    git fetch origin
    git reset --hard origin/main 2>/dev/null || git reset --hard origin/master 2>/dev/null
    cd ..
    echo "✅ 源码已更新至最新"
else
    echo "⚠️ 警告: notebooks_src 目录未找到"
fi

# 2. 构建内容 (从源码生成 content/notebooks)
echo "正在构建 Hugo 内容..."
python3 scripts/build_content.py

# 3. 启动 Hugo
echo "启动 Hugo 服务器..."
hugo server -D --bind 127.0.0.1
