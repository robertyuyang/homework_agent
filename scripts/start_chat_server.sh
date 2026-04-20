#!/bin/bash
#
# 启动 Agent 对话服务器
#

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# 进入项目根目录
cd "$PROJECT_ROOT"

# 检查是否在虚拟环境中
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "🔧 激活虚拟环境..."
    if [[ -d ".venv" ]]; then
        source .venv/bin/activate
    else
        echo "⚠️  未找到虚拟环境，尝试使用系统 Python"
    fi
fi

# 检查依赖
echo "📦 检查依赖..."
pip install -q fastapi uvicorn flask-cors 2>/dev/null

# 启动服务器
echo ""
echo "🚀 启动 Agent 对话服务器..."
echo "📍 本地访问: http://localhost:8000"
echo "📚 API 文档: http://localhost:8000/docs"
echo ""
echo "按 Ctrl+C 停止服务器"
echo ""

python -m src.chat_server
