# 代码生成时间: 2025-07-31 23:16:09
import hashlib
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK


# 哈希值计算工具类
class HashCalculatorService:
    def __init__(self):
        pass

    def calculate_hash(self, input_string: str, algorithm: str = "sha256") -> str:
        """
        根据给定的字符串和算法计算哈希值。
        :param input_string: 要计算哈希值的字符串
        :param algorithm: 哈希算法（默认为sha256）
        :return: 计算得到的哈希值
        """
        try:
            hash_func = getattr(hashlib, algorithm)()
            hash_func.update(input_string.encode("utf-8"))
            return hash_func.hexdigest()
        except AttributeError:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        except Exception as e:
            raise Exception(f"Error calculating hash: {str(e)}")


# API端点处理函数
async def calculate_hash_endpoint(request: Request):
    """
    计算并返回请求体中字符串的哈希值。
    :param request: 包含输入字符串和哈希算法的请求对象。
    :return: JSON响应，包含哈希值。
    """
    try:
        data = await request.json()
        input_string = data.get("input_string")
        algorithm = data.get("algorithm", "sha256")
        if not input_string:
            return JSONResponse(
                content={"error": "Input string is missing."}, status_code=HTTP_400_BAD_REQUEST
            )
        hash_calculator = HashCalculatorService()
        hash_result = hash_calculator.calculate_hash(input_string, algorithm)
        return JSONResponse(content={"hash": hash_result}, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


# 创建Starlette应用并定义路由
app = Starlette(
    routes=[
        Route("/hash", calculate_hash_endpoint, methods=["POST"]),
    ]
)

# 如果直接运行文件，启动服务
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)