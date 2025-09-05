# 代码生成时间: 2025-09-05 19:24:19
import hashlib
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
哈希值计算工具
提供接口计算输入数据的哈希值
"""

# 定义哈希值计算函数
def calculate_hash(data: str, algorithm: str = 'sha256') -> str:
    """
    计算指定算法的哈希值
    
    参数:
    data (str): 待计算哈希值的数据
    algorithm (str): 哈希算法，默认为 'sha256'
    
    返回:
    str: 计算得到的哈希值
    """
    try:
        hash_func = getattr(hashlib, algorithm)()
        hash_func.update(data.encode())
        return hash_func.hexdigest()
    except Exception as e:
        raise ValueError(f'计算哈希值失败: {str(e)}')

# 定义API路由和处理函数
def hash_value_endpoint(request: Request) -> JSONResponse:
    """
    处理哈希值计算请求
    
    参数:
    request (Request): Starlette请求对象
    
    返回:
    JSONResponse: 包含哈希值的JSON响应
    """
    try:
        data = request.query_params.get('data')
        if not data:
            return JSONResponse({'error': '缺少数据参数'}, status_code=400)

        algorithm = request.query_params.get('algorithm', 'sha256')
        hash_value = calculate_hash(data, algorithm)
        return JSONResponse({'hash': hash_value})
    except ValueError as e:
        return JSONResponse({'error': str(e)}, status_code=400)

# 创建Starlette应用
app = Starlette(debug=True, routes=[
    Route('/calculate-hash', hash_value_endpoint),
])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)