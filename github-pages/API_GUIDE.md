# 🤖 Agent 对话 API 接口指南

## 概述

这是 Agent 对话前端页面的后端 API 接口规范。按照这个规范实现后端，就可以与我们提供的前端页面完美集成。

## 前端页面

前端页面文件：`agent-chat.html`

特性：
- ✅ 支持演示模式（无需后端）
- ✅ 支持 API 模式（连接真实后端）
- ✅ 完整的聊天界面
- ✅ 配置持久化（localStorage）
- ✅ 响应式设计

## API 接口规范

### 1. 对话接口

**端点：** `POST /chat` (或你自定义的路径)

**请求头：**
```
Content-Type: application/json
```

**请求体：**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "你好"
    },
    {
      "role": "assistant", 
      "content": "你好！有什么我可以帮助你的？"
    },
    {
      "role": "user",
      "content": "最新的用户消息"
    }
  ]
}
```

**字段说明：**
- `messages`: 对话历史数组，按时间顺序排列
- `role`: 消息角色，`"user"` 或 `"assistant"`
- `content`: 消息内容

---

### 2. 响应格式

**成功响应 (200 OK):**

**格式 1：简单字符串**
```json
"这是助手的回复内容"
```

**格式 2：对象格式 (推荐)**
```json
{
  "content": "这是助手的回复内容",
  "usage": {
    "prompt_tokens": 100,
    "completion_tokens": 50
  }
}
```

**格式 3：兼容 OpenAI 格式**
```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "这是助手的回复内容"
      }
    }
  ]
}
```

---

## Python 后端实现示例

### 方案 1：FastAPI (推荐)

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境请设置具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    content: str

@app.post("/chat")
async def chat(request: ChatRequest):
    # 获取最后一条用户消息
    user_message = request.messages[-1].content
    
    # TODO: 在这里调用你的 Agent 逻辑
    # 示例回复
    response = f"收到你的消息：{user_message}\n\n这是一条示例回复。"
    
    return ChatResponse(content=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 方案 2：Flask

```python
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # 允许跨域请求

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    messages = data.get('messages', [])
    
    # 获取最后一条用户消息
    if messages:
        user_message = messages[-1].get('content', '')
    else:
        user_message = ''
    
    # TODO: 在这里调用你的 Agent 逻辑
    response = f"收到你的消息：{user_message}"
    
    return jsonify({"content": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
```

### 方案 3：与现有 LangChain Agent 集成

如果你的项目已经有 LangChain Agent，可以这样集成：

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import sys
import os

# 导入你的 Agent
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from src.agents.agent import build_agent

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化 Agent
agent = build_agent()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.post("/chat")
async def chat(request: ChatRequest):
    # 获取对话历史
    messages = request.messages
    
    # 将消息转换为 LangChain 格式
    from langchain_core.messages import HumanMessage, AIMessage
    
    langchain_messages = []
    for msg in messages:
        if msg.role == 'user':
            langchain_messages.append(HumanMessage(content=msg.content))
        else:
            langchain_messages.append(AIMessage(content=msg.content))
    
    # 调用 Agent
    config = {"configurable": {"thread_id": "web-chat"}}
    response = await agent.ainvoke(
        {"messages": langchain_messages},
        config=config
    )
    
    # 获取最后的回复
    assistant_message = response["messages"][-1].content
    
    return {"content": assistant_message}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 快速测试

### 1. 启动后端（以 FastAPI 为例）

```bash
# 安装依赖
pip install fastapi uvicorn flask-cors

# 启动服务
python your_backend_file.py
```

### 2. 测试 API

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

### 3. 使用前端页面

1. 在浏览器中打开 `agent-chat.html`
2. 切换到 "API模式"
3. 配置后端地址（如：`http://localhost:8000/chat`）
4. 点击 "测试连接"
5. 开始对话！

---

## 部署建议

### 后端部署选项

1. **本地开发**
   - 直接运行在 localhost:8000
   - 前端使用 file:// 或本地服务器打开

2. **内网部署**
   - 部署在公司内网服务器
   - 前端配置内网 IP 地址

3. **云服务器部署**
   - 阿里云、腾讯云、AWS 等
   - 配置域名和 HTTPS
   - 前端配置公网域名

4. **Vercel/Railway/Render**
   - 快速部署 Python 后端
   - 自动 HTTPS
   - 免费额度可用

### CORS 配置注意事项

生产环境请严格配置 CORS：

```python
# 不要这样（允许所有来源）
allow_origins=["*"]

# 应该这样
allow_origins=[
    "https://your-username.github.io",
    "https://your-custom-domain.com"
]
```

---

## 常见问题

### Q: 前端显示"连接失败"？
A: 检查以下几点：
1. 后端服务是否正常启动
2. 端口是否正确（默认 8000）
3. CORS 是否正确配置
4. 防火墙是否阻止了请求

### Q: 如何支持流式响应？
A: 当前版本使用简单的请求-响应模式。如需流式响应，可以使用 Server-Sent Events (SSE) 或 WebSocket。

### Q: 如何添加身份验证？
A: 可以在请求头中添加 API Key：
```javascript
// 前端
headers: {
  'Authorization': 'Bearer YOUR_API_KEY'
}
```

---

## 技术支持

如有问题，请查看项目文档或提交 Issue！
