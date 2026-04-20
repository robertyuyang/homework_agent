# 部署指南

## 🎯 GitHub Pages 部署方案

### 方案一：纯静态版本（推荐用于演示）

**文件**：`static/index-standalone.html`

这个版本可以直接部署到 GitHub Pages，展示界面，但评分功能是演示版。

#### 部署步骤：

1. **创建 GitHub 仓库**
   ```bash
   # 在 GitHub 上创建一个新仓库
   # 或者使用现有仓库
   ```

2. **准备文件**
   ```bash
   # 复制静态文件
   cp static/index-standalone.html /path/to/your/repo/index.html
   ```

3. **推送到 GitHub**
   ```bash
   cd /path/to/your/repo
   git add index.html
   git commit -m "Add grading system frontend"
   git push
   ```

4. **启用 GitHub Pages**
   - 进入仓库 Settings
   - 找到 Pages 选项
   - Source 选择 "Deploy from a branch"
   - Branch 选择 main 或 gh-pages
   - 点击 Save

5. **访问你的网站**
   - 等待几分钟
   - 访问：`https://your-username.github.io/repo-name/`

---

### 方案二：分离部署（完整功能）

如果你需要完整的评分功能，需要分离部署：

#### 前端部署（GitHub Pages）
- 使用 `static/index.html`
- 修改 API 地址，指向你的后端

#### 后端部署（选择一个）
1. **Vercel** - 免费，部署简单
2. **Heroku** - 免费额度
3. **阿里云/腾讯云** - 云服务器
4. **Railway** - 免费额度

---

## 📁 文件说明

```
/workspace/projects/
├── static/
│   ├── index.html              # 完整版本（需要后端）
│   └── index-standalone.html   # 纯静态版本（可直接部署）
├── src/
│   ├── main.py                 # 后端服务
│   ├── agents/
│   └── tools/
└── DEPLOY_GUIDE.md            # 本文件
```

---

## 🚀 快速开始（本地测试）

如果你想先在本地测试完整功能：

```bash
cd /workspace/projects

# 安装依赖
uv pip install

# 启动后端
python src/main.py

# 打开浏览器访问
# http://localhost:5000/
```

---

## 💡 推荐方案

**如果你只是想展示界面**：
- 使用 `index-standalone.html`
- 直接部署到 GitHub Pages

**如果你需要完整功能**：
- 前端：GitHub Pages
- 后端：Vercel 或其他云平台
- 修改前端 API 地址

---

## 📞 需要帮助？

有问题随时问我！😊
