# 代码生成时间: 2025-09-01 07:28:00
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException

# 排序算法实现
class SortingService:
    def sort_numbers(self, numbers):
        """
        对数字列表进行排序
        :param numbers: 需要排序的数字列表
        :return: 排序后的数字列表
        """
        try:
            # 对输入参数进行验证
            if not all(isinstance(num, (int, float)) for num in numbers):
                raise ValueError("列表中所有元素必须是数字")
            # 排序数字
            return sorted(numbers)
        except Exception as e:
            # 捕获任何异常并返回错误信息
            return {
                "error": str(e),
                "code": 500
            }

# 创建Starlette应用
app = Starlette(routes=[
    Route("/sort", endpoint=SortingService(), methods=["POST"]),
])

# 定义路由处理函数
@app.route("/sort", methods=["POST"])
async def sort(request):
    # 从请求中获取数据
    try:
        data = await request.json()
        numbers = data.get("numbers")
        if not numbers:
            raise HTTPException(status_code=400, detail="请求体中缺少'numbers'字段")
        # 使用SortingService进行排序
        sorting_service = SortingService()
        sorted_numbers = sorting_service.sort_numbers(numbers)
        # 返回排序结果
        return JSONResponse(sorted_numbers)
    except HTTPException as http_err:
        return JSONResponse(status_code=http_err.status_code, content={"detail": http_err.detail})
    except Exception as err:
        return JSONResponse(status_code=500, content={"error": str(err)})
