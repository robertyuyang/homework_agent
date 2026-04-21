# ⚡ 最简单的 CORS 解决方案

不需要部署任何东西！直接使用公共 CORS 代理！

---

## 🎯 方案一：使用公共 CORS 代理（最快）⭐

### 步骤 1：修改 API 地址

在 GitHub Pages 页面中，将 **API地址** 修改为：

```
https://api.allorigins.win/raw?url=https://qz23wrnyv4.coze.site/stream_run
```

或者使用这个：

```
https://corsproxy.io/?https://qz23wrnyv4.coze.site/stream_run
```

### 步骤 2：保存并测试

1. 点击 "💾 保存配置"
2. 点击 "🔗 测试连接"
3. 开始对话！

---

## 📝 完整配置示例

| 配置项 | 值 |
|--------|-----|
| **API地址** | `https://api.allorigins.win/raw?url=https://qz23wrnyv4.coze.site/stream_run` |
| **Project ID** | `7630729322323787795` |
| **Authorization Token** | `Bearer eyJhbGciOiJSUzI1NiIs...`（你的Token） |
| **Session ID** | （自动生成） |

---

## 🔄 如果第一个不行，试试这些

### 代理 1
```
https://api.allorigins.win/raw?url=https://qz23wrnyv4.coze.site/stream_run
```

### 代理 2
```
https://corsproxy.io/?https://qz23wrnyv4.coze.site/stream_run
```

### 代理 3
```
https://api.codetabs.com/v1/proxy?quest=https://qz23wrnyv4.coze.site/stream_run
```

### 代理 4
```
https://api.allorigins.win/get?url=https://qz23wrnyv4.coze.site/stream_run
```

---

## ⚠️ 注意事项

### 公共代理的限制

✅ **优点**：
- 无需部署
- 立即使用
- 完全免费

⚠️ **缺点**：
- 可能不稳定
- 不适合生产环境
- 速度可能较慢
- 有请求频率限制

### 安全建议

- 🚨 **不要在公共代理中发送敏感数据**
- 🔐 Token 会经过代理服务器
- 🏭 生产环境请部署自己的代理（见 VERCEL_DEPLOY.md）

---

## 🚀 如果公共代理不行，部署自己的代理

参见 [VERCEL_DEPLOY.md](./VERCEL_DEPLOY.md) 部署自己的 Vercel 代理，只需 5 分钟！

---

## 💡 快速测试

### 测试代理是否工作

在浏览器控制台（F12）中运行：

```javascript
// 测试代理 1
fetch('https://api.allorigins.win/raw?url=https://qz23wrnyv4.coze.site/stream_run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ test: true })
})
.then(r => console.log('代理1工作正常!', r))
.catch(e => console.error('代理1失败:', e))
```

---

## 🎊 总结

| 方案 | 难度 | 稳定性 | 推荐度 |
|------|------|--------|--------|
| 公共 CORS 代理 | ⭐ 最简单 | ⚠️ 一般 | ⭐⭐⭐ 测试用 |
| Vercel 代理 | ⭐⭐ 简单 | ✅ 好 | ⭐⭐⭐⭐⭐ 推荐 |

---

**先试试公共代理，如果不行再部署自己的！🎯**
