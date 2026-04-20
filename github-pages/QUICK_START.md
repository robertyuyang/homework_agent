# 🚀 Coze Agent 快速配置指南

## 5 分钟快速开始

### 1️⃣ 打开页面

在浏览器中打开：`index.html`（或你部署后的地址）

### 2️⃣ 配置参数

点击页面顶部的 **"⚙️ 显示/隐藏配置"**，填入以下信息：

| 配置项 | 说明 | 示例值 |
|--------|------|--------|
| **API地址** | 你的 Coze API 端点 | `https://qz23wrnyv4.coze.site/stream_run` |
| **Project ID** | 项目 ID | `7630729322323787795` |
| **Authorization Token** | 认证 Token（必填） | `Bearer eyJhbGciOiJSUzI1NiIs...` |
| **Session ID** | 会话 ID（自动生成） | 点击 "🔄 生成Session ID" |

### 3️⃣ 保存配置

点击 **"💾 保存配置"** 按钮，配置会自动保存到浏览器本地存储。

### 4️⃣ 测试连接

点击 **"🔗 测试连接"** 按钮，确认连接成功。

### 5️⃣ 开始对话

在输入框输入消息，按回车或点击发送！

---

## 📝 详细配置说明

### Authorization Token

这是最重要的配置项，格式如下：
```
Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6IjliOWYxZTRjLWE4ZWYtNDA4Yy1iYjU2LTMwNmI5NjJhMzllMCJ9...
```

**注意**：
- Token 必须包含 `Bearer ` 前缀（页面会自动添加）
- Token 有有效期，请定期更新
- 不要将 Token 分享给他人

### Session ID

会话 ID 用于标识不同的对话会话：
- 可以点击 "🔄 生成Session ID" 自动生成
- 也可以手动输入自定义的 ID
- 更换 Session ID 会开始新的对话

### Project ID

项目 ID 是你的 Coze 项目的唯一标识。

---

## 🎯 使用示例

### 示例 1：简单对话

1. 配置好所有参数
2. 输入：`你好`
3. 点击发送
4. 等待 Agent 回复

### 示例 2：多轮对话

1. 保持同一个 Session ID
2. 连续发送多条消息
3. Agent 会记住上下文

### 示例 3：开始新对话

1. 点击 "🔄 生成Session ID"
2. 或手动输入新的 Session ID
3. 开始全新的对话

---

## 🔧 常见问题

### Q: 点击测试连接没反应？
A: 检查以下几点：
1. Authorization Token 是否已填写
2. API 地址是否正确
3. 网络连接是否正常
4. 浏览器控制台是否有错误（按 F12 查看）

### Q: 提示"连接失败"？
A: 可能的原因：
1. Token 已过期
2. API 地址不正确
3. 跨域问题（CORS）
4. 服务端暂时不可用

### Q: 配置刷新后丢失了？
A: 
1. 确保点击了 "💾 保存配置"
2. 检查浏览器是否禁用了 localStorage
3. 尝试使用相同的浏览器和配置文件

### Q: 如何分享给其他人？
A: 
1. 将 HTML 文件部署到 GitHub Pages 或其他静态托管
2. 分享访问链接
3. 告知对方需要配置自己的 Token

---

## 💡 高级功能

### 配置持久化

配置会自动保存到浏览器的 localStorage 中，下次打开页面时会自动加载。

### 快速生成 Session ID

点击 "🔄 生成Session ID" 按钮可以快速生成一个随机的会话 ID。

### 响应格式

页面会自动解析以下响应格式：
- 纯字符串
- `{content: "..."}`
- `{message: "..."}`
- `{output: "..."}`
- OpenAI 格式 `{choices: [{message: {...}}]}`

---

## 📚 相关文档

- [完整部署指南](./README.md)
- [API 接口文档](./API_GUIDE.md)

---

## 🆘 获取帮助

如果遇到问题：
1. 查看浏览器控制台错误信息（F12）
2. 检查 Token 和 API 地址是否正确
3. 确认服务端是否正常运行

祝你使用愉快！🎉
