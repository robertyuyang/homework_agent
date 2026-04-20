import os
import zipfile
import tempfile
import re
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_dev_sdk.fetch import FetchClient


def _extract_code_from_text(text):
    """从文本中提取Python代码，查找作业1相关的代码"""
    # 尝试查找代码块
    code_block_pattern = r'```python\s*(.*?)\s*```'
    code_blocks = re.findall(code_block_pattern, text, re.DOTALL)
    
    if code_blocks:
        # 返回找到的第一个代码块
        return code_blocks[0].strip()
    
    # 如果没有找到代码块，尝试查找def calcArea相关的代码
    calc_area_pattern = r'(def calcArea.*?)(?=\n\s*def |\n\s*if __name__|$)'
    matches = re.findall(calc_area_pattern, text, re.DOTALL)
    
    if matches:
        # 找到calcArea函数，还需要找main部分
        full_code = matches[0]
        main_pattern = r'(if __name__.*?)$'
        main_match = re.search(main_pattern, text, re.DOTALL)
        if main_match:
            full_code += '\n' + main_match.group(1)
        return full_code.strip()
    
    # 如果都没找到，返回原始文本（可能是纯代码）
    return text.strip()


def _process_word_document(file_path_or_url):
    """处理单个Word文档，提取代码"""
    try:
        # 先尝试本地文件读取
        if not file_path_or_url.startswith('http'):
            workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
            full_path = os.path.join(workspace_path, file_path_or_url)
            
            if os.path.exists(full_path):
                # 尝试用docx2python读取（支持.docx）
                try:
                    from docx2python import docx2python
                    result = docx2python(full_path)
                    text = result.text
                    code = _extract_code_from_text(text)
                    if code and len(code.strip()) > 0:
                        return {"success": True, "code": code, "filename": os.path.basename(file_path_or_url)}
                except Exception as e:
                    pass
                
                # 如果docx2python失败，尝试用textract（支持更多格式）
                try:
                    import textract
                    text = textract.process(full_path).decode('utf-8')
                    code = _extract_code_from_text(text)
                    if code and len(code.strip()) > 0:
                        return {"success": True, "code": code, "filename": os.path.basename(file_path_or_url)}
                except Exception as e:
                    pass
                
                # 如果都失败，尝试直接读取文件内容
                try:
                    with open(full_path, 'rb') as f:
                        # 尝试作为文本读取
                        content = f.read()
                        # 尝试不同的编码
                        for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                            try:
                                text = content.decode(encoding)
                                code = _extract_code_from_text(text)
                                if code and len(code.strip()) > 0:
                                    return {"success": True, "code": code, "filename": os.path.basename(file_path_or_url)}
                            except:
                                continue
                except Exception as e:
                    pass
                
                # 如果所有方法都失败，返回错误
                return {"success": False, "error": "无法从文档中提取代码，请直接粘贴代码内容", "filename": os.path.basename(file_path_or_url)}
        
        # 如果是URL，使用fetch-url
        client = FetchClient()
        response = client.fetch(url=file_path_or_url)
        
        if response.status_code != 0:
            return {"success": False, "error": f"获取文档失败: {response.status_message}", "filename": file_path_or_url}
        
        # 提取文本内容
        text_content = []
        for item in response.content:
            if item.type == "text":
                text_content.append(item.text)
        
        full_text = "\n".join(text_content)
        code = _extract_code_from_text(full_text)
        
        return {"success": True, "code": code, "filename": response.title or os.path.basename(file_path_or_url)}
        
    except Exception as e:
        return {"success": False, "error": f"处理文档时出错: {str(e)}，请直接粘贴代码内容", "filename": file_path_or_url}


@tool
def extract_code_from_document(file_path_or_url: str) -> str:
    """
    从单个Word文档中提取作业1的Python代码。
    
    Args:
        file_path_or_url: Word文档的文件路径或URL
        
    Returns:
        提取到的代码或错误信息
    """
    ctx = request_context.get() or new_context(method="extract_code_from_document")
    
    result = _process_word_document(file_path_or_url)
    
    if result["success"]:
        return f"""## 📄 文档处理成功

**文件名**: {result['filename']}

**提取到的代码**:
```python
{result['code']}
```

现在你可以使用上面的代码进行评分了！
"""
    else:
        return f"""## ❌ 文档处理失败

**文件名**: {result['filename']}

**错误信息**: {result['error']}
"""


@tool
def extract_codes_from_zip(zip_file_path: str) -> str:
    """
    从zip包中提取所有Word文档，每个文档提取作业1的Python代码。
    
    Args:
        zip_file_path: zip文件的路径
        
    Returns:
        所有提取到的代码的汇总信息
    """
    ctx = request_context.get() or new_context(method="extract_codes_from_zip")
    
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    full_zip_path = os.path.join(workspace_path, zip_file_path)
    
    if not os.path.exists(full_zip_path):
        return f"## ❌ Zip文件不存在\n\n文件路径: {zip_file_path}\n请确认文件路径是否正确。"
    
    results = []
    
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # 解压zip文件
            with zipfile.ZipFile(full_zip_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # 遍历解压后的文件
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.endswith('.docx') or file.endswith('.doc'):
                        file_path = os.path.join(root, file)
                        # 处理每个Word文档
                        result = _process_word_document(file_path)
                        result['original_filename'] = file
                        results.append(result)
        
        # 生成报告
        report = []
        report.append(f"## 📦 Zip包处理完成\n")
        report.append(f"**共找到 {len(results)} 个Word文档**\n")
        
        success_count = sum(1 for r in results if r['success'])
        report.append(f"✅ 成功提取: {success_count} 个\n")
        report.append(f"❌ 提取失败: {len(results) - success_count} 个\n")
        
        if success_count > 0:
            report.append("\n---\n")
            report.append("### 📋 成功提取的代码：\n")
            
            for i, result in enumerate([r for r in results if r['success']], 1):
                report.append(f"\n#### {i}. {result.get('original_filename', result.get('filename', 'unknown'))}\n")
                report.append("```python\n")
                report.append(result['code'])
                report.append("\n```\n")
        
        if len(results) - success_count > 0:
            report.append("\n---\n")
            report.append("### ❌ 提取失败的文档：\n")
            
            for result in [r for r in results if not r['success']]:
                report.append(f"- {result.get('original_filename', result.get('filename', 'unknown'))}: {result.get('error', '未知错误')}\n")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"## ❌ 处理Zip包时出错\n\n错误信息: {str(e)}"
