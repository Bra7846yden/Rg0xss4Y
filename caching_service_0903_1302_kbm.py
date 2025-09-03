# 代码生成时间: 2025-09-03 13:02:07
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Scope, Send
import hashlib
import time

# 缓存存储结构
cache_store = {}

# 缓存键生成函数
def generate_cache_key(request: Request) -> str:
    """根据请求信息生成唯一的缓存键"""
    key_parts = [
        request.scope.get("type", ""),
        request.url.path,
        request.url.query,
        request.method,
        ', '.join(sorted(request.headers.keys())),
    ]
    return hashlib.sha256(", ".join(key_parts).encode()).hexdigest()


# 缓存中间件
class SimpleCacheMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        请求分发中间件，用于缓存处理。
        如果请求已缓存，则直接返回缓存内容；
        否则，处理请求并将结果缓存。
        """
        cache_key = generate_cache_key(request)
        if cache_key in cache_store:
            return cache_store[cache_key]
        
        response = await call_next(request)
        
        # 缓存响应内容
        cache_store[cache_key] = response
        return response


# 示例路由
async def example_route(request: Request) -> Response:
    """
    一个示例路由，返回请求的时间戳。
    """
    return JSONResponse(content={"timestamp": int(time.time())})

# 创建Starlette应用
app = Starlette(debug=True, middleware=[Middleware(SimpleCacheMiddleware)])

# 添加路由
app.add_route("/example", example_route, methods=["GET"])

# 运行Starlette应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)