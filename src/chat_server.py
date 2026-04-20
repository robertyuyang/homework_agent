"""
Agent 对话服务器
提供 HTTP API 接口，供前端页面调用
"""
import os
import sys
import json
from typing import List, Dict, Any
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# 导入项目中的 Agent
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
try:
    from src.agents.agent import build_agent
    AGENT_AVAILABLE = True
except ImportError:
    AGENT_AVAILABLE = False
    print("⚠️  Agent 模块不可用，将使用演示模式")


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


class ChatResponse(BaseModel):
    content: str
    model: str = "agent"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """生命周期管理"""
    print("🚀 启动 Agent 对话服务器...")
    
    # 初始化 Agent
    if AGENT_AVAILABLE:
        try:
            app.state.agent = build_agent()
            print("✅ Agent 初始化成功")
        except Exception as e:
            print(f"⚠️  Agent 初始化失败: {e}")
            app.state.agent = None
    else:
        app.state.agent = None
    
    yield
    
    print("👋 服务器关闭")


app = FastAPI(
    title="Agent Chat API",
    description="智能 Agent 对话接口",
    version="1.0.0",
    lifespan=lifespan
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请设置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 演示模式的回复
DEMO_RESPONSES = [
    "你好！我是你的智能助手。有什么我可以帮助你的吗？",
    "这是一个很好的问题！让我来帮你分析一下...",
    "我理解你的需求。根据我的分析，我建议...",
    "这个想法很有趣！让我们深入探讨一下...",
    "感谢你的提问！这是我的回答。",
    "好的，我来帮你处理这个问题。",
    "明白了！让我为你解释一下这个概念。"
]


def get_demo_response(message: str) -> str:
    """演示模式的回复"""
    if "你好" in message or "hello" in message.lower():
        return "你好！很高兴见到你！我是你的智能助手，有什么我可以帮助你的吗？😊"
    
    if "代码" in message or "code" in message.lower():
        return """当然！我可以帮你处理代码问题。

```python
# 示例代码
def hello():
    print('Hello, World!')
```

这是一个简单的示例函数！"""
    
    import random
    return random.choice(DEMO_RESPONSES)


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    对话接口
    """
    if not request.messages:
        return ChatResponse(content="请输入消息", model="demo")
    
    # 获取最后一条用户消息
    last_message = request.messages[-1]
    user_content = last_message.content
    
    # 如果有可用的 Agent，使用 Agent
    if AGENT_AVAILABLE and hasattr(app.state, 'agent') and app.state.agent:
        try:
            # 将消息转换为 LangChain 格式
            from langchain_core.messages import HumanMessage, AIMessage
            
            langchain_messages = []
            for msg in request.messages:
                if msg.role == 'user':
                    langchain_messages.append(HumanMessage(content=msg.content))
                else:
                    langchain_messages.append(AIMessage(content=msg.content))
            
            # 调用 Agent
            config = {"configurable": {"thread_id": "web-chat"}}
            response = await app.state.agent.ainvoke(
                {"messages": langchain_messages},
                config=config
            )
            
            # 获取最后的回复
            assistant_message = response["messages"][-1].content
            
            return ChatResponse(
                content=assistant_message,
                model="agent"
            )
            
        except Exception as e:
            print(f"Agent 调用失败: {e}")
            # 降级到演示模式
            return ChatResponse(
                content=get_demo_response(user_content),
                model="demo"
            )
    
    # 演示模式
    return ChatResponse(
        content=get_demo_response(user_content),
        model="demo"
    )


@app.get("/")
async def root():
    """根路径 - 重定向到聊天页面"""
    static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    chat_html = os.path.join(static_dir, "agent-chat.html")
    
    if os.path.exists(chat_html):
        return FileResponse(chat_html)
    
    return {
        "message": "Agent Chat Server",
        "version": "1.0.0",
        "endpoints": {
            "chat": "POST /chat",
            "docs": "GET /docs"
        }
    }


@app.get("/health")
async def health():
    """健康检查"""
    return {
        "status": "healthy",
        "agent_available": AGENT_AVAILABLE
    }


# 挂载静态文件（如果存在）
static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")


def start_server(host: str = "0.0.0.0", port: int = 8000):
    """启动服务器"""
    import uvicorn
    print(f"🌟 Agent 对话服务器启动中...")
    print(f"📍 访问地址: http://{host}:{port}")
    print(f"📚 API 文档: http://{host}:{port}/docs")
    print()
    
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent 对话服务器")
    parser.add_argument("--host", default="0.0.0.0", help="监听地址")
    parser.add_argument("--port", type=int, default=8000, help="监听端口")
    
    args = parser.parse_args()
    
    start_server(args.host, args.port)
