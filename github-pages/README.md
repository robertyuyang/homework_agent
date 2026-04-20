# 🤖 Agent 智能对话 - GitHub Pages 部署指南

## 📦 项目简介

这是一个功能完整的 Agent 对话系统，可以在 GitHub Pages 上部署！

- ✅ **前端页面**：美观的聊天界面，支持演示模式和 API 模式
- ✅ **后端服务**：与你的 Agent 完美集成的 FastAPI 服务
- ✅ **GitHub Pages**：一键部署，无需服务器

---

## 🚀 快速开始

### 方式一：GitHub Pages 部署（纯前端）

#### 1️⃣ 准备文件

确保你的仓库中有以下文件：
- `agent-chat.html` - 主页面
- `.nojekyll` - GitHub Pages 配置
- `README.md` - 说明文档（本文件）

#### 2️⃣ 启用 GitHub Pages

1. 进入你的 GitHub 仓库
2. 点击 `Settings` → `Pages`
3. 配置如下：
   - **Source**: `Deploy from a branch`
   - **Branch**: `main` (或 `master`)
   - **Folder**: `/ (root)` 或 `/docs`
4. 点击 `Save`

#### 3️⃣ 访问你的页面

几分钟后，访问：`https://你的用户名.github.io/仓库名/agent-chat.html`

---

### 方式二：本地完整部署（推荐）

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
| `agent-chat.html` | 聊天主页面 ⭐ |
| `index.html` | 旧版作业评分页面 |
| `API_GUIDE.md` | API 接口详细文档 |
| `README.md` | 本说明文件 |
| `.nojekyll` | GitHub Pages 配置 |

### 后端文件

| 文件 | 说明 |
|------|------|
| `src/chat_server.py` | FastAPI 聊天服务器 ⭐ |
| `scripts/start_chat_server.sh` | 启动脚本 |

---

## 🎯 使用指南

### 前端页面功能

#### 🎮 演示模式
- 无需后端，直接体验完整界面
- 智能的演示回复
- 测试所有交互功能

#### 🔌 API 模式
- 配置你的后端地址
- 连接真实的 Agent 服务
- 享受完整的 AI 对话体验

### 配置步骤

1. **打开页面**
   - GitHub Pages: `https://你的用户名.github.io/仓库名/agent-chat.html`
   - 本地: `http://localhost:8000`

2. **切换模式**
   - 点击右上角 "演示模式" / "API模式"

3. **配置后端（API模式）**
   - 在 "后端地址" 输入框填写你的 API 地址
   - 例如：`http://localhost:8000/chat`
   - 点击 "测试连接"

4. **开始对话**
   - 在输入框输入消息
   - 按 Enter 或点击发送
   - 享受智能对话！

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

**请求：**
```json
POST /chat
{
  "messages": [
    {"role": "user", "content": "用户消息"},
    {"role": "assistant", "content": "助手回复"}
  ]
}
```

**响应：**
```json
{
  "content": "助手的回复内容",
  "model": "agent"
}
```

详细文档请查看 [API_GUIDE.md](./API_GUIDE.md)

---

## 🌐 部署架构

```
┌─────────────────┐         ┌─────────────────┐
│  GitHub Pages   │         │   后端服务      │
│  (前端页面)     │◄───────►│  (你的Agent)    │
│                 │   API   │                 │
│ agent-chat.html │         │  chat_server.py │
└─────────────────┘         └─────────────────┘
```

### 部署选项

1. **GitHub Pages + 本地后端**
   - 前端：GitHub Pages
   - 后端：本地运行（localhost）
   - 适用：个人开发、测试

2. **GitHub Pages + 云后端**
   - 前端：GitHub Pages
   - 后端：Vercel/Railway/Render/云服务器
   - 适用：公开访问、分享给他人

3. **完全本地部署**
   - 前端 + 后端都在本地
   - 适用：内网使用、隐私保护

---

## 📚 详细文档

- [API 接口文档](./API_GUIDE.md) - 完整的 API 规范和示例代码
- [FastAPI 文档](http://localhost:8000/docs) - 启动后端后访问自动生成的文档

---

## 🎨 自定义配置

### 修改配色

编辑 `agent-chat.html` 中的 CSS：

```css
/* 渐变色背景 */
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### 修改页面标题

```html
<title>🤖 我的智能助手</title>
```

### 添加自定义功能

前端使用纯 HTML/CSS/JavaScript，可以随意扩展！

---

## ❓ 常见问题

### Q: GitHub Pages 上可以使用完整功能吗？
A: GitHub Pages 只能托管静态页面。你需要：
- 在 GitHub Pages 上使用前端页面
- 后端服务部署在其他地方（本地、云服务器等）

### Q: 如何让其他人也能使用？
A: 
1. 将后端部署到公网服务器
2. 配置公网 API 地址
3. 分享 GitHub Pages 链接给他人

### Q: 支持流式响应吗？
A: 当前版本使用简单的请求-响应模式。如需流式响应，请参考 API 文档扩展。

### Q: 如何添加身份验证？
A: 可以在 API 请求头中添加 API Key，详细请参考 API_GUIDE.md。

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

**享受你的智能 Agent 对话！** 🎉
