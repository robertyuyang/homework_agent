"""
简单的代理服务器，用于解决 CORS 问题
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import httpx
from pathlib import Path

app = FastAPI(title="Coze Agent Proxy", version="1.0.0")

# 允许所有来源的 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 默认的 Coze API 配置
DEFAULT_COZE_API_URL = "https://qz23wrnyv4.coze.site/stream_run"


@app.post("/api/chat")
async def proxy_chat(request: Request):
    """
    代理请求到 Coze API
    """
    try:
        body = await request.json()
        
        # 从请求头获取 Authorization
        headers = {}
        auth_header = request.headers.get("Authorization")
        if auth_header:
            headers["Authorization"] = auth_header
        
        headers["Content-Type"] = "application/json"
        
        # 转发请求到 Coze API
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                DEFAULT_COZE_API_URL,
                json=body,
                headers=headers
            )
            
            # 返回响应
            response.raise_for_status()
            return response.json()
            
    except Exception as e:
        print(f"代理请求错误: {e}")
        return {
            "error": str(e),
            "content": f"代理请求失败: {str(e)}"
        }


@app.get("/")
async def root():
    """根路径 - 返回聊天页面"""
    index_path = Path(__file__).parent.parent / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return {
        "message": "Coze Agent Proxy Server",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /api/chat",
            "docs": "GET /docs"
        }
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {"status": "healthy", "proxy": "active"}


# 挂载静态文件
project_root = Path(__file__).parent.parent
if project_root.exists():
    app.mount("/static", StaticFiles(directory=project_root), name="static")


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """启动服务器"""
    import uvicorn
    print("=" * 60)
    print("🚀 Coze Agent 代理服务器")
    print("=" * 60)
    print(f"📍 本地访问: http://{host}:{port}")
    print(f"📚 API 文档: http://{host}:{port}/docs")
    print(f"🔗 代理端点: http://{host}:{port}/api/chat")
    print("=" * 60)
    print()
    print("💡 使用说明:")
    print("1. 在浏览器中打开上面的地址")
    print("2. 将 API 地址配置为: http://localhost:8000/api/chat")
    print("3. 填入你的 Authorization Token")
    print("4. 开始对话！")
    print()
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Coze Agent 代理服务器")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=8000, help="监听端口")
    
    args = parser.parse_args()
    
    start_server(args.host, args.port)
