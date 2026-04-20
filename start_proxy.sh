#!/bin/bash
#
# 启动 Coze Agent 代理服务器
#

# 获取脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 检查虚拟环境
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "🔧 检查虚拟环境..."
    if [[ -d ".venv" ]]; then
        echo "✅ 激活虚拟环境"
        source .venv/bin/activate
    fi
fi

# 检查依赖
echo "📦 检查依赖..."
pip install -q fastapi uvicorn httpx 2>/dev/null

# 启动服务器
echo ""
echo "🚀 启动 Coze Agent 代理服务器..."
echo ""
python -m src.proxy_server
