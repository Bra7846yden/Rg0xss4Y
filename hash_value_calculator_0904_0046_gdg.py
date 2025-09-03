# 代码生成时间: 2025-09-04 00:46:38
import hashlib
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


class HashValueCalculator:
    """哈希值计算工具"""
    def __init__(self):
        self.algorithms = ['md5', 'sha1', 'sha256', 'sha512']

    def calculate_hash(self, value: str, algorithm: str) -> str:
        """根据给定的值和哈希算法计算哈希值"""
        if algorithm not in self.algorithms:
            raise ValueError(f"Unsupported algorithm: {algorithm}
Supported algorithms: {[alg for alg in self.algorithms]}
")

        try:
            hash_func = getattr(hashlib, algorithm)()
            hash_func.update(value.encode('utf-8'))
            return hash_func.hexdigest()
        except AttributeError as e:
            raise ValueError(f"Invalid hash function: {algorithm}
{str(e)}")


def hash_value_endpoint(request):
    """计算哈希值的端点"""
    try:
        value = request.query_params['value']
        algorithm = request.query_params['algorithm']

        calculator = HashValueCalculator()
        hash_value = calculator.calculate_hash(value, algorithm)
        return JSONResponse({'hash_value': hash_value})
    except KeyError as e:
        return JSONResponse({'error': f"Missing parameter: {str(e)}"}, status_code=400)
    except ValueError as e:
        return JSONResponse({'error': str(e)}, status_code=400)


def main():
    # 创建Starlette应用
    app = Starlette(debug=True)

    # 定义路由
    routes = [
        Route('/hash-value', hash_value_endpoint),
    ]

    # 将路由添加到应用
    app.routes.extend(routes)

    # 运行应用
    if __name__ == '__main__':
        import uvicorn
        uvicorn.run(app, host='0.0.0.0', port=8000)

"""
哈希值计算工具

用法:
  - 通过GET请求访问/hash-value端点，传入value和algorithm参数
  - 支持的哈希算法: md5, sha1, sha256, sha512
"""
