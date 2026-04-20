# 🔧 CORS 问题解决方案

## 问题说明

"Failed to fetch" 错误是因为浏览器的 **CORS（跨域资源共享）** 安全策略：
- 你的页面在：`https://robertyuyang.github.io/`
- 你的 API 在：`https://qz23wrnyv4.coze.site/`
- 浏览器阻止了这种跨域请求

---

## 🎯 解决方案（按推荐顺序）

### 方案一：本地使用（最简单）⭐

不要在 GitHub Pages 上使用，直接在本地打开 HTML 文件：

```bash
# 方法 1：直接双击打开
# 在文件管理器中双击 index.html

# 方法 2：用浏览器命令打开
open /workspace/projects/index.html
```

**优点**：
- ✅ 无需任何配置
- ✅ 直接使用，立即生效
- ✅ 没有 CORS 问题

---

### 方案二：使用本地代理服务器

创建一个简单的本地代理服务器来转发请求：

#### 1️⃣ 创建代理服务器

创建文件 `src/proxy_server.py`：

```python
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import httpx
from pathlib import Path

app = FastAPI()

# 允许所有来源的 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 你的 Coze API 配置
COZE_API_URL = "https://qz23wrnyv4.coze.site/stream_run"

@app.post("/api/chat")
async def proxy_chat(request: Request):
    """代理请求到 Coze API"""
    body = await request.json()
    
    # 转发请求到 Coze API
    async with httpx.AsyncClient() as client:
        response = await client.post(
            COZE_API_URL,
            json=body,
            headers=dict(request.headers)
        )
        return response.json()

# 挂载静态文件
static_path = Path(__file__).parent.parent
if (static_path / "index.html").exists():
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    print("🚀 代理服务器启动中...")
    print("📍 访问: http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

#### 2️⃣ 启动代理服务器

```bash
# 安装依赖
pip install fastapi uvicorn httpx

# 启动代理
python -m src.proxy_server
```

#### 3️⃣ 修改前端配置

在页面中修改 API 地址为：
```
http://localhost:8000/api/chat
```

---

### 方案三：使用 CORS 代理服务

使用公共的 CORS 代理服务（仅用于测试，不推荐生产环境）：

#### 修改 API 地址为：
```
https://api.allorigins.win/raw?url=https://qz23wrnyv4.coze.site/stream_run
```

或者：
```
https://corsproxy.io/?https://qz23wrnyv4.coze.site/stream_run
```

**注意**：这些公共代理可能不稳定，且不要发送敏感数据！

---

### 方案四：使用浏览器扩展（开发测试用）

安装 CORS 浏览器扩展来临时禁用 CORS 策略：

1. Chrome/Edge: 安装 "Allow CORS: Access-Control-Allow-Origin"
2. Firefox: 安装 "CORS Everywhere"
3. 启用扩展
4. 刷新页面重试

**注意**：仅用于开发测试，不要在日常浏览中启用！

---

## 📝 推荐使用方案

### 🌱 开发测试
**方案一（本地打开）** 或 **方案四（CORS 扩展）**

### 🚀 日常使用
**方案一（本地打开 HTML 文件）**

### 🏭 生产环境
**方案二（自建代理服务器）** 部署到云服务器

---

## 🔍 调试步骤

如果问题仍然存在，按以下步骤调试：

### 1️⃣ 打开浏览器开发者工具
- 按 `F12` 或 `Ctrl+Shift+I`
- 切换到 `Console`（控制台）标签

### 2️⃣ 查看错误信息
- 红色的错误信息会显示具体问题
- 截图或复制错误信息

### 3️⃣ 查看 Network（网络）标签
- 切换到 `Network` 标签
- 尝试发送请求
- 查看失败的请求详情

---

## 💡 快速测试

### 测试 CORS 是否是问题

在浏览器控制台（F12）中运行：

```javascript
fetch('https://qz23wrnyv4.coze.site/stream_run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ test: true })
})
.then(r => console.log('成功:', r))
.catch(e => console.error('失败:', e))
```

如果这个也失败，就是 CORS 问题。

---

## 🆘 需要帮助？

如果以上方案都不行，请提供：
1. 浏览器控制台的错误截图
2. 你使用的是哪个方案
3. 具体的错误信息

祝你早日解决问题！🎯
