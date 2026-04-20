# 📝 GitHub Pages 部署指南

## 快速部署步骤

### 方法一：直接部署（推荐）

1. **Fork 本仓库**
   - 点击右上角的 "Fork" 按钮
   - 等待 Fork 完成

2. **启用 GitHub Pages**
   - 进入 Fork 后的仓库
   - 点击 `Settings`（设置）
   - 在左侧菜单找到 `Pages`
   - 在 `Build and deployment` 部分：
     - Source 选择：`Deploy from a branch`
     - Branch 选择：`main` 或 `master`
     - Folder 选择：`/ (root)`
   - 点击 `Save`

3. **上传 GitHub Pages 文件**
   - 将本文件夹中的 `index.html` 上传到你仓库的根目录
   - 或者创建一个 `docs` 文件夹，把 `index.html` 放进去，然后在 Pages 设置中选择 `docs` 文件夹

4. **等待部署**
   - 部署通常需要 1-2 分钟
   - 在仓库首页可以看到部署状态
   - 部署完成后，访问地址类似：`https://your-username.github.io/repo-name/`

### 方法二：使用 gh-pages 分支

1. **创建 gh-pages 分支**
```bash
# 在本地仓库中
git checkout -b gh-pages

# 复制 index.html 到分支
# 提交并推送
git add index.html
git commit -m "Add GitHub Pages"
git push origin gh-pages
```

2. **在 GitHub 仓库设置中**
   - Settings → Pages
   - Branch 选择：`gh-pages`
   - 点击 `Save`

## 文件结构

```
your-repo/
├── index.html          # GitHub Pages 主页（必需）
└── README.md          # 说明文档（可选）
```

## 自定义设置

### 修改仓库链接

编辑 `index.html`，找到这一行：
```html
<p><strong>源代码</strong>：<a href="https://github.com/your-username/your-repo" target="_blank">查看 GitHub 仓库</a></p>
```
将链接修改为你自己的仓库地址。

### 修改页面标题

编辑 `index.html` 的 `<title>` 标签：
```html
<title>矩形重合面积计算 - 作业评分系统</title>
```

### 修改配色方案

在 `index.html` 的 `<style>` 部分，找到：
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```
修改为你喜欢的颜色。

## 完整功能部署指南

GitHub Pages 版本仅提供界面演示。如需完整功能，请在本地部署后端。

### 本地部署完整版本

1. **下载项目**
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务**
```bash
python src/main.py
```

4. **访问完整版本**
   - 打开浏览器访问：`http://localhost:8000`
   - 使用完整的 AI 评分功能

## 常见问题

### Q: 部署后访问 404？
A: 
- 检查 Pages 设置中的分支是否正确
- 确认 index.html 在正确的位置
- 等待几分钟让 GitHub 完成部署

### Q: 如何自定义域名？
A:
- 在仓库根目录创建 `CNAME` 文件
- 内容填写你的域名，例如：`example.com`
- 在你的域名 DNS 提供商处添加 CNAME 记录

### Q: 能否添加更多页面？
A: 可以！在同一目录下添加更多 HTML 文件，通过链接相互跳转。

## 技术说明

- **纯静态页面**：无需后端，直接在浏览器运行
- **响应式设计**：支持手机、平板、桌面设备
- **现代浏览器支持**：Chrome、Firefox、Safari、Edge

## 许可证

本项目采用 MIT 许可证。

---

**如有问题，欢迎提交 Issue！** 🚀
