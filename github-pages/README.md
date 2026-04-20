# 🤖 Agent 智能对话 - GitHub Pages 部署指南

## 📦 项目简介

这是一个功能完整的 Agent 对话系统，可以在 GitHub Pages 上部署！

- ✅ **Coze Agent 页面**：专门为 Coze API 设计的聊天界面 ⭐
- ✅ **通用 Agent 页面**：支持自定义后端 API 的通用界面
- ✅ **后端服务**：与你的 Agent 完美集成的 FastAPI 服务
- ✅ **GitHub Pages**：一键部署，无需服务器

---

## 🎯 选择适合你的页面

### 🚀 Coze Agent 页面（推荐）
**文件**: `index.html` 或 `coze-agent-chat.html`

专为 Coze API 设计：
- ✅ 支持 Authorization Token 配置
- ✅ 支持 Project ID 配置
- ✅ 支持 Session ID 管理
- ✅ 配置持久化到 localStorage
- ✅ 内置连接测试功能

**快速开始**: 查看 [QUICK_START.md](./QUICK_START.md)

---

### 🌐 通用 Agent 页面
**文件**: `agent-chat.html`

通用 API 兼容：
- ✅ 演示模式（无需后端）
- ✅ API 模式（连接自定义后端）
- ✅ 灵活的 API 格式支持

---

## 🚀 快速开始

### 方式一：GitHub Pages 部署

#### 1️⃣ 准备文件

确保你的仓库中有以下文件：
- `index.html` - Coze Agent 主页面 ⭐
- `.nojekyll` - GitHub Pages 配置
- `README.md` - 说明文档（本文件）
- `QUICK_START.md` - 快速配置指南

#### 2️⃣ 启用 GitHub Pages

1. 进入你的 GitHub 仓库
2. 点击 `Settings` → `Pages`
3. 配置如下：
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` (或 `master`)
   - **Folder**: `/ (root)` 或 `/docs`
4. 点击 `Save`

#### 3️⃣ 访问你的页面

几分钟后，访问：`https://你的用户名.github.io/仓库名/`

---

### 方式二：本地直接使用

#### 1️⃣ 打开页面

直接在浏览器中打开：
```bash
# Coze Agent 页面
open github-pages/index.html

# 或通用页面
open github-pages/agent-chat.html
```

#### 2️⃣ 配置参数

根据页面提示配置 API 地址和 Token。

---

### 方式三：本地完整部署（带后端）

#### 1️⃣ 克隆或下载项目

```bash
cd 你的项目目录
```

#### 2️⃣ 启动后端服务

**方法 A：使用启动脚本**
```bash
bash scripts/start_chat_server.sh
```

**方法 B：直接运行 Python**
```bash
python -m src.chat_server
```

#### 3️⃣ 访问聊天页面

打开浏览器访问：`http://localhost:8000`

---

## 📁 文件说明

### GitHub Pages 文件

| 文件 | 说明 |
|------|------|
| `index.html` | Coze Agent 主页面 ⭐ |
| `coze-agent-chat.html` | Coze Agent 页面（副本） |
| `agent-chat.html` | 通用 Agent 页面 |
| `QUICK_START.md` | Coze Agent 快速配置指南 ⭐ |
| `API_GUIDE.md` | API 接口详细文档 |
| `README.md` | 本说明文件 |
| `.nojekyll` | GitHub Pages 配置 |

### 后端文件

| 文件 | 说明 |
|------|------|
| `src/chat_server.py` | FastAPI 聊天服务器 ⭐ |
| `scripts/start_chat_server.sh` | 启动脚本 |

---

## 🎯 Coze Agent 页面使用指南

### 配置步骤

1. **打开页面**
   - GitHub Pages: `https://你的用户名.github.io/仓库名/`
   - 本地: 直接打开 `index.html`

2. **显示配置**
   - 点击 "⚙️ 显示/隐藏配置"

3. **填写配置**
   - **API地址**: `https://qz23wrnyv4.coze.site/stream_run`
   - **Project ID**: `7630729322323787795`
   - **Authorization Token**: `Bearer eyJhbGciOiJSUzI1NiIs...`（你的Token）
   - **Session ID**: 点击 "🔄 生成Session ID"

4. **保存并测试**
   - 点击 "💾 保存配置"
   - 点击 "🔗 测试连接"

5. **开始对话**
   - 输入消息，按回车发送！

详细指南请查看 [QUICK_START.md](./QUICK_START.md)

---

## 🔧 后端 API 开发

### 快速测试后端

```bash
# 启动后端
python -m src.chat_server

# 测试 API
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "你好"}
    ]
  }'
```

### API 规范

**通用格式：**
```json
POST /chat
{
  "messages": [
    {"role": "user", "content": "用户消息"},
    {"role": "assistant", "content": "助手回复"}
  ]
}
```

**Coze 格式：**
```json
POST /stream_run
{
  "content": {
    "query": {
      "prompt": [{"type": "text", "content": {"text": "用户消息"}}]
    }
  },
  "type": "query",
  "session_id": "会话ID",
  "project_id": 项目ID
}
```

详细文档请查看 [API_GUIDE.md](./API_GUIDE.md)

---

## 🌐 部署架构

```
┌─────────────────┐         ┌─────────────────┐
│  GitHub Pages   │         │   Coze API      │
│  (前端页面)     │◄───────►│  (你的服务)     │
│                 │   API   │                 │
│   index.html    │         │  stream_run     │
└─────────────────┘         └─────────────────┘
```

### 部署选项

1. **GitHub Pages + Coze API**
   - 前端：GitHub Pages
   - 后端：Coze 提供的 API
   - 适用：最简单的方式 ⭐

2. **GitHub Pages + 自定义后端**
   - 前端：GitHub Pages
   - 后端：Vercel/Railway/Render/云服务器
   - 适用：需要自定义逻辑

3. **完全本地部署**
   - 前端 + 后端都在本地
   - 适用：内网使用、隐私保护

---

## ❓ 常见问题

### Q: Coze Agent 页面和通用页面有什么区别？
A:
- **Coze Agent 页面**: 专门为 Coze API 设计，支持 Token、Project ID、Session ID 等配置
- **通用页面**: 支持自定义后端 API，适合通用场景

### Q: GitHub Pages 上可以直接使用 Coze API 吗？
A: 可以！只需要：
1. 部署 `index.html` 到 GitHub Pages
2. 配置你的 Coze API 地址和 Token
3. 开始对话！

### Q: Token 安全吗？
A: Token 只保存在浏览器的 localStorage 中，不会发送到其他服务器。但请注意：
- 不要在公共电脑上使用
- 定期更换 Token
- 不要分享包含 Token 的配置

### Q: 如何让其他人也能使用？
A:
1. 将 `index.html` 部署到 GitHub Pages
2. 分享访问链接
3. 告知对方需要配置自己的 Token

---

## 📚 文档索引

- 🚀 [Coze Agent 快速配置](./QUICK_START.md) ⭐
- 📖 [完整部署指南](./README.md)
- 🔌 [API 接口文档](./API_GUIDE.md)
- 📚 [FastAPI 自动文档](http://localhost:8000/docs) (启动后端后访问)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

**享受你的智能 Agent 对话！** 🎉
