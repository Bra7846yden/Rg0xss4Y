# 代码生成时间: 2025-08-10 10:08:45
import aiohttp
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
import socket

"""
网络连接状态检查器
检查给定的URL是否可达。
"""

# 定义异步函数检查网络连接
async def check_connection(session, url):
    try:
        # 尝试发送HTTP请求
        async with session.get(url) as response:
            # 检查HTTP响应状态码
            if response.status == HTTP_200_OK:
                return True
            else:
                return False
    except (aiohttp.ClientError, asyncio.TimeoutError):
        # 处理请求错误或超时
        return False

# 定义异步函数检查单个URL的可访问性
async def check_url(url):
    async with aiohttp.ClientSession() as session:
        return await check_connection(session, url)

# 创建Starlette应用
app = Starlette(routes=[
    Route("/check", endpoint=lambda request: check_url("http://example.com"), methods=["GET"]),
    Route("/check/{url}", endpoint=lambda request: check_url(request.path_params["url\]), methods=["GET"]),
])

# 定义检查URL可达性的异步函数
async def check_url_endpoint(request):
    url = request.path_params["url"]
    try:
        # 检查URL是否可达
        accessible = await check_url(url)
        # 返回结果和状态码
        return JSONResponse(
            {
                "url": url,
                "accessible": accessible,
            },
            status_code=HTTP_200_OK if accessible else HTTP_503_SERVICE_UNAVAILABLE,
        )
    except Exception as e:
        # 处理其他异常
        return JSONResponse(
            {"error": str(e)},
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

# 更新路由以添加异常处理
app.routes[1] = Route("/check/{url}", endpoint=check_url_endpoint, methods=["GET"])
