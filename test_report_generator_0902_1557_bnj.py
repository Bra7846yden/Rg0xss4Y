# 代码生成时间: 2025-09-02 15:57:35
import os
import uuid
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 定义一个类来生成测试报告
class TestReportGenerator():
    def __init__(self, template_path):
        self.template_path = template_path

    def generate_report(self, test_results):
        """
        根据测试结果生成测试报告。
        :param test_results: 测试结果的字典
        :return: 生成的报告的文件路径
        """
        try:
            # 读取模板文件
            with open(self.template_path, 'r') as file:
                template = file.read()

            # 插入测试结果
            report_content = template.format(**test_results)

            # 生成文件名
            report_filename = f"test_report_{uuid.uuid4().hex}.txt"

            # 写入报告文件
            with open(report_filename, 'w') as file:
                file.write(report_content)

            return report_filename
        except Exception as e:
            # 异常处理
            return f"Error generating report: {str(e)}"

# 创建Starlette应用
app = Starlette(debug=True)

# 路由：生成测试报告
@app.route("/report", methods=["POST"])
async def generate_report(request):
    """
    接收测试结果并生成测试报告。
    :param request: Starlette的请求对象
    :return: JSON响应，包含报告的文件路径
    """
    # 获取请求体
    try:
        test_results = await request.json()
    except Exception as e:
        return JSONResponse(
            content={"error": f"Invalid JSON: {str(e)}"}, status_code=400
        )

    # 生成报告
    report_generator = TestReportGenerator("test_report_template.txt")
    report_filename = report_generator.generate_report(test_results)

    # 返回响应
    return JSONResponse(
        content={"filename": report_filename}, status_code=200
    )

# 定义路由
routes = [
    Route("/report", generate_report),
]

# 将路由添加到应用
app.add_routes(routes)