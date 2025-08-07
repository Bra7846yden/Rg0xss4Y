# 代码生成时间: 2025-08-08 04:06:31
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import pandas as pd
import numpy as np

# 数据分析器API类
class DataAnalysisAPI:
    def __init__(self):
        # 初始化时，可以加载数据集或设置参数
        pass

    def calculate_mean(self, data):
        """计算给定数据集的平均值"""
        try:
            return np.mean(data)
        except Exception as e:
            return {
                "error": f"Error calculating mean: {str(e)}"
            }

    def calculate_median(self, data):
        """计算给定数据集的中位数"""
        try:
            return np.median(data)
        except Exception as e:
            return {
                "error": f"Error calculating median: {str(e)}"
            }

    def calculate_standard_deviation(self, data):
        """计算给定数据集的标准差"""
        try:
            return np.std(data)
        except Exception as e:
            return {
                "error": f"Error calculating standard deviation: {str(e)}"
            }

# 创建Starlette应用
app = Starlette(debug=True)

# 定义路由
routes = [
    Route("/mean", endpoint=DataAnalysisAPI().calculate_mean, methods=["POST"]),
    Route("/median", endpoint=DataAnalysisAPI().calculate_median, methods=["POST"]),
    Route("/std_dev", endpoint=DataAnalysisAPI().calculate_standard_deviation, methods=["POST"]),
]

# 将路由添加到Starlette应用中
app.add_routes(routes)

# 启动应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
