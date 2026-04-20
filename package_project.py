#!/usr/bin/env python3
"""
项目打包脚本
将项目文件打包，方便下载到本地
"""

import os
import zipfile
from datetime import datetime


def package_project():
    """打包项目文件"""
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    os.chdir(workspace_path)
    
    # 生成时间戳
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"rectangle-grading-system_{timestamp}.zip"
    
    # 需要包含的文件和目录
    include_patterns = [
        "src/",
        "static/",
        "config/",
        "assets/",
        "pyproject.toml",
        "DEPLOY_GUIDE.md",
        "README.md",
        "AGENT.md",
    ]
    
    # 需要排除的文件
    exclude_patterns = [
        ".venv/",
        ".git/",
        ".coze/",
        "__pycache__/",
        "*.pyc",
        ".DS_Store",
        "server.log",
    ]
    
    print(f"📦 开始打包项目...")
    print(f"📁 工作目录: {workspace_path}")
    print(f"📦 输出文件: {zip_filename}")
    print()
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历所有文件
        for root, dirs, files in os.walk('.'):
            # 跳过排除的目录
            dirs[:] = [d for d in dirs if not any(excl in os.path.join(root, d) for excl in exclude_patterns)]
            
            for file in files:
                file_path = os.path.join(root, file)
                
                # 检查是否需要包含
                rel_path = os.path.relpath(file_path, '.')
                
                # 检查是否在排除列表中
                should_exclude = any(excl in rel_path for excl in exclude_patterns)
                if should_exclude:
                    continue
                
                # 检查是否在包含列表中，或者是根目录文件
                should_include = any(pattern in rel_path or rel_path == pattern.rstrip('/') 
                                   for pattern in include_patterns)
                
                # 根目录的文件（非目录）默认包含
                if '/' not in rel_path:
                    should_include = True
                
                if should_include:
                    zipf.write(file_path, rel_path)
                    print(f"✅ 已添加: {rel_path}")
    
    # 获取文件大小
    file_size = os.path.getsize(zip_filename) / (1024 * 1024)  # MB
    
    print()
    print("=" * 60)
    print(f"✅ 打包完成！")
    print(f"📦 文件: {zip_filename}")
    print(f"📊 大小: {file_size:.2f} MB")
    print()
    print("📋 包含内容:")
    print("  - src/      - 后端源代码")
    print("  - static/   - 前端页面")
    print("  - config/   - 配置文件")
    print("  - assets/   - 资源文件")
    print("  - pyproject.toml - 依赖配置")
    print("  - DEPLOY_GUIDE.md - 部署指南")
    print()
    print(f"📍 文件位置: {os.path.join(workspace_path, zip_filename)}")
    print("=" * 60)
    
    return zip_filename


if __name__ == "__main__":
    try:
        zip_file = package_project()
        print(f"\n🎉 项目已打包完成！")
        print(f"📦 下载文件: {zip_file}")
    except Exception as e:
        print(f"❌ 打包失败: {e}")
        import traceback
        traceback.print_exc()
