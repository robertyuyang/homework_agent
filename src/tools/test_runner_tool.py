import csv
import os
import tempfile
import sys
from io import StringIO
from contextlib import redirect_stdout
from langchain.tools import tool
from coze_coding_utils.log.write_log import request_context
from coze_coding_utils.runtime_ctx.context import new_context


def _read_test_cases():
    """读取测试用例文件"""
    workspace_path = os.getenv("COZE_WORKSPACE_PATH", "/workspace/projects")
    test_file = os.path.join(workspace_path, "assets/testcase_with_result.csv")
    
    test_cases = []
    expected_results = []
    
    with open(test_file, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row or not row[0].strip():
                continue
            # 前6个是输入数据
            test_case = row[:6]
            # 第7个是预期结果
            expected = int(row[6])
            test_cases.append(test_case)
            expected_results.append(expected)
    
    return test_cases, expected_results


def _run_code_with_test_cases(code, test_cases):
    """运行学生的代码并传入测试用例"""
    # 创建临时目录
    with tempfile.TemporaryDirectory() as temp_dir:
        # 创建测试用的CSV文件
        test_csv = os.path.join(temp_dir, "test_rectangles.csv")
        with open(test_csv, 'w') as f:
            for case in test_cases:
                f.write(','.join(case) + '\n')
        
        # 修改代码中的文件名，并添加返回结果的捕获
        modified_code = code.replace("'rectangles.csv'", f"'{test_csv}'")
        modified_code = modified_code.replace('"rectangles.csv"', f'"{test_csv}"')
        
        # 添加捕获结果的代码
        full_code = f"""{modified_code}

# 捕获结果
if 'calcArea' in globals():
    try:
        result = calcArea('{test_csv}')
        print('__RESULT_START__')
        print(result)
        print('__RESULT_END__')
    except Exception as e:
        print('__ERROR_START__')
        print(str(e))
        print('__ERROR_END__')
"""
        
        # 重定向stdout并执行代码
        f = StringIO()
        try:
            with redirect_stdout(f):
                # 在独立的命名空间中执行
                exec_globals = {}
                exec(full_code, exec_globals)
            output = f.getvalue()
        except Exception as e:
            return {"error": f"代码执行错误: {str(e)}"}
        
        # 解析输出
        if '__ERROR_START__' in output:
            error_start = output.find('__ERROR_START__') + len('__ERROR_START__')
            error_end = output.find('__ERROR_END__')
            error_msg = output[error_start:error_end].strip()
            return {"error": f"代码运行时错误: {error_msg}"}
        
        if '__RESULT_START__' in output:
            result_start = output.find('__RESULT_START__') + len('__RESULT_START__')
            result_end = output.find('__RESULT_END__')
            result_str = output[result_start:result_end].strip()
            
            try:
                # 尝试解析结果列表
                result = eval(result_str)
                if isinstance(result, list):
                    return {"results": result}
                else:
                    return {"error": f"返回结果不是列表类型: {type(result)}"}
            except Exception as e:
                return {"error": f"解析结果失败: {str(e)}, 输出: {result_str}"}
        
        return {"error": "未捕获到返回结果，请确保代码中有 print(calcArea('rectangles.csv'))"}


@tool
def run_test_cases(code: str) -> str:
    """
    运行学生的Python代码，使用测试用例进行测试，并返回测试结果。
    
    Args:
        code: 学生提交的完整Python代码字符串
        
    Returns:
        测试结果的详细报告，包括通过率、错误的测试用例等
    """
    ctx = request_context.get() or new_context(method="run_test_cases")
    
    try:
        # 读取测试用例
        test_cases, expected_results = _read_test_cases()
        
        # 运行代码
        run_result = _run_code_with_test_cases(code, test_cases)
        
        if "error" in run_result:
            return f"❌ 测试失败：{run_result['error']}"
        
        actual_results = run_result["results"]
        
        # 对比结果
        passed = 0
        failed = 0
        failed_cases = []
        
        for i, (actual, expected) in enumerate(zip(actual_results, expected_results)):
            if actual == expected:
                passed += 1
            else:
                failed += 1
                failed_cases.append({
                    "case": i + 1,
                    "input": test_cases[i],
                    "expected": expected,
                    "actual": actual
                })
        
        # 生成报告
        total = len(expected_results)
        pass_rate = (passed / total) * 100 if total > 0 else 0
        
        report = []
        report.append("## 🧪 测试用例执行结果\n")
        report.append(f"**总测试用例数**: {total}")
        report.append(f"**通过**: {passed} ✅")
        report.append(f"**失败**: {failed} ❌")
        report.append(f"**通过率**: {pass_rate:.1f}%\n")
        
        if failed > 0:
            report.append("### ❌ 失败的测试用例：\n")
            for fc in failed_cases[:10]:  # 最多显示10个失败的用例
                report.append(f"- **用例 {fc['case']}**:")
                report.append(f"  输入: {fc['input']}")
                report.append(f"  期望: {fc['expected']}")
                report.append(f"  实际: {fc['actual']}\n")
            
            if len(failed_cases) > 10:
                report.append(f"... 还有 {len(failed_cases) - 10} 个失败用例未显示\n")
        
        if pass_rate == 100:
            report.append("🎉 **所有测试用例通过！代码完全正确！**")
        elif pass_rate >= 80:
            report.append("👍 **大部分测试通过，只有少量错误需要修正**")
        elif pass_rate >= 50:
            report.append("⚠️ **部分测试通过，需要检查核心逻辑**")
        else:
            report.append("❌ **较多测试失败，建议重新检查逻辑**")
        
        return "\n".join(report)
        
    except Exception as e:
        return f"❌ 测试执行异常：{str(e)}"
