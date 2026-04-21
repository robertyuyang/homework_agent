# ⚡ Cloudflare Workers 部署指南（推荐！）

Cloudflare Workers 是**最简单、最快、完全免费**的方案！

---

## 🚀 3 步快速部署

### 第 1 步：创建 Cloudflare Worker

1. 访问 https://workers.cloudflare.com
2. 注册/登录 Cloudflare 账号（免费）
3. 点击 "Create application"
4. 选择 "Create Worker"
5. 给你的 Worker 起个名字，比如：`coze-proxy`
6. 点击 "Deploy"

### 第 2 步：替换代码

1. 部署成功后，点击 "Edit code"
2. **删除** 编辑器中的所有默认代码
3. **复制** `cloudflare-worker.js` 的全部内容
4. **粘贴** 到编辑器中
5. 点击 "Save and Deploy"

### 第 3 步：获取你的代理 URL

部署成功后，你会得到一个类似这样的 URL：
```
https://coze-proxy.yourname.workers.dev
```

---

## 🎯 配置前端

### 在 GitHub Pages 页面中：

1. 点击 "⚙️ 显示/隐藏配置"
2. 修改 **API地址** 为：
   ```
   https://coze-proxy.yourname.workers.dev
   ```
   （注意：**不需要** 加 `/api/chat`）
3. 其他配置保持不变
4. 点击 "💾 保存配置"
5. 点击 "🔗 测试连接"

---

## 📝 完整代码

`cloudflare-worker.js` 文件内容：

```javascript
const COZE_API_URL = 'https://qz23wrnyv4.coze.site/stream_run';

export default {
  async fetch(request, env, ctx) {
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        },
      });
    }

    try {
      const requestBody = await request.json();
      const authHeader = request.headers.get('Authorization') || '';

      const cozeResponse = await fetch(COZE_API_URL, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': authHeader,
        },
        body: JSON.stringify(requestBody),
      });

      const responseData = await cozeResponse.json();

      return new Response(JSON.stringify(responseData), {
        status: cozeResponse.status,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });

    } catch (error) {
      return new Response(JSON.stringify({
        error: 'Proxy error',
        message: error.message
      }), {
        status: 500,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
        },
      });
    }
  },
};
```

---

## 💡 为什么推荐 Cloudflare Workers？

| 特性 | 说明 |
|------|------|
| 🆓 **完全免费** | 每天 10 万次请求，完全够用 |
| ⚡ **超快** | 全球 CDN 节点，速度极快 |
| 🛠️ **超简单** | 3 步部署，无需 Git |
| 🔒 **安全** | Cloudflare 安全基础设施 |
| 🌍 **全球** | 世界各地都能快速访问 |

---

## 🔍 调试步骤

如果遇到问题：

### 1️⃣ 测试 Worker 是否工作

在浏览器地址栏直接访问你的 Worker URL：
```
https://coze-proxy.yourname.workers.dev
```

应该看到：`{"error":"Method not allowed"}`（这是正常的！）

### 2️⃣ 检查 Cloudflare Worker 日志

1. 在 Cloudflare Worker 页面
2. 点击 "Logs" 标签
3. 尝试发送请求
4. 查看是否有错误

### 3️⃣ 检查浏览器控制台

1. 按 `F12` 打开开发者工具
2. 切换到 `Console` 标签
3. 尝试发送请求
4. 查看错误信息

---

## 📊 架构说明

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  GitHub Pages   │         │ Cloudflare      │         │   Coze API      │
│  (前端页面)     │────────►│ Worker (代理)   │────────►│  (你的服务)     │
│                 │         │                 │         │                 │
│ index.html      │         │  免费、超快     │         │  stream_run     │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

---

## 🎊 总结

Cloudflare Workers 是目前最好的方案：
- ✅ 完全免费
- ✅ 部署超简单（3 步）
- ✅ 速度超快
- ✅ 支持 POST 请求
- ✅ 完美解决 CORS 问题

**现在就去部署吧！5 分钟搞定！🚀**
