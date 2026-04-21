# 🚀 Vercel 代理部署指南

## 概述

这个代理服务器可以解决 GitHub Pages 和 Coze API 之间的 CORS 问题。

---

## 📦 一键部署（最简单）

### 方法一：使用 Vercel 一键部署

1. **创建一个新的 GitHub 仓库**，专门用于代理
   - 仓库名：`coze-proxy`（或你喜欢的名字）

2. **创建以下文件结构**：
```
coze-proxy/
├── api/
│   └── proxy.js
└── vercel.json
```

3. **复制文件内容**：
   - `api/proxy.js` - 从本项目的 `vercel-proxy/api/proxy.js` 复制
   - `vercel.json` - 从本项目的 `vercel-proxy/vercel.json` 复制

4. **推送到 GitHub**

5. **部署到 Vercel**：
   - 访问 https://vercel.com
   - 点击 "New Project"
   - 选择你的 `coze-proxy` 仓库
   - 点击 "Deploy"
   - 等待部署完成（约 1 分钟）

6. **获取你的代理 URL**：
   - 部署完成后，Vercel 会给你一个 URL，类似：
   ```
   https://coze-proxy-abc123.vercel.app
   ```

---

## 🎯 配置前端

### 在 GitHub Pages 页面中配置：

1. 打开你的 GitHub Pages 页面
2. 点击 "⚙️ 显示/隐藏配置"
3. 修改 **API地址** 为：
   ```
   https://你的-vercel-proxy地址.vercel.app/api/chat
   ```
   例如：
   ```
   https://coze-proxy-abc123.vercel.app/api/chat
   ```
4. 其他配置保持不变
5. 点击 "💾 保存配置"
6. 点击 "🔗 测试连接"

---

## 📝 完整步骤示例

### 第 1 步：准备代理项目

```bash
# 1. 创建新目录
mkdir coze-proxy
cd coze-proxy

# 2. 创建文件夹
mkdir -p api

# 3. 从你的项目复制文件
cp /path/to/your/project/vercel-proxy/api/proxy.js api/
cp /path/to/your/project/vercel-proxy/vercel.json .

# 4. 初始化 git
git init
git add .
git commit -m "Initial commit"
```

### 第 2 步：创建 GitHub 仓库

1. 访问 https://github.com/new
2. 仓库名：`coze-proxy`
3. 选择 Public
4. 点击 "Create repository"
5. 按提示推送代码

### 第 3 步：部署到 Vercel

1. 访问 https://vercel.com
2. 注册/登录（可以用 GitHub 账号）
3. 点击 "Add New..." → "Project"
4. 选择 `coze-proxy` 仓库
5. 点击 "Deploy"
6. 等待 1-2 分钟

### 第 4 步：配置前端

1. Vercel 部署完成后，复制你的域名，例如：
   ```
   https://coze-proxy-git-main-yourname.vercel.app
   ```

2. 在 GitHub Pages 页面中：
   - API地址: `https://coze-proxy-git-main-yourname.vercel.app/api/chat`
   - Project ID: `7630729322323787795`
   - Authorization Token: `你的 Token`

3. 测试连接！

---

## 🎨 Vercel 代理文件内容

### api/proxy.js
```javascript
const COZE_API_URL = 'https://qz23wrnyv4.coze.site/stream_run';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  try {
    const response = await fetch(COZE_API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': req.headers.authorization || '',
      },
      body: JSON.stringify(req.body),
    });

    const data = await response.json();
    res.status(response.status).json(data);

  } catch (error) {
    res.status(500).json({
      error: 'Proxy error',
      message: error.message
    });
  }
}
```

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/**/*.js",
      "use": "@vercel/node"
    }
  ],
  "routes": [
    {
      "src": "/api/chat",
      "dest": "/api/proxy.js"
    }
  ]
}
```

---

## 💡 架构说明

```
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│  GitHub Pages   │         │   Vercel Proxy  │         │   Coze API      │
│  (前端页面)     │────────►│  (CORS代理)     │────────►│  (你的服务)     │
│                 │         │                 │         │                 │
│ index.html      │         │  api/proxy.js   │         │  stream_run     │
└─────────────────┘         └─────────────────┘         └─────────────────┘
```

---

## ❓ 常见问题

### Q: Vercel 免费吗？
A: 是的！Vercel 有免费额度，完全足够个人使用。

### Q: 代理安全吗？
A: 代理只转发请求，不存储任何数据。Token 直接透传给 Coze API。

### Q: 可以自定义域名吗？
A: 可以！在 Vercel 项目设置中可以配置自定义域名。

### Q: 代理速度怎么样？
A: Vercel 在全球有 CDN 节点，速度很快！

---

## 🚀 替代方案

如果不想用 Vercel，也可以用：

- **Railway**: https://railway.app
- **Render**: https://render.com
- **Cloudflare Workers**: https://workers.cloudflare.com

部署方式都类似！

---

祝你部署成功！🎉
