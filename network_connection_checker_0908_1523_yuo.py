# 代码生成时间: 2025-09-08 15:23:00
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE
import requests
import socket

# 网络连接状态检查器异常类
class ConnectionCheckError(Exception):
    pass

# 检查单个主机的网络连接状态
async def check_host_connection(host):
    try:
        # 使用socket库尝试建立TCP连接
        socket.create_connection((host, 80), timeout=10)
        return True
    except (socket.timeout, socket.error):
        return False

# 异步路由处理函数
async def check_connection(request):
    host = request.query_params.get('host')
    if not host:
        return JSONResponse({'error': 'Host parameter is required'}, status_code=HTTP_400_BAD_REQUEST)
    try:
        connected = await check_host_connection(host)
        if connected:
            return JSONResponse({'status': 'connected'}, status_code=HTTP_200_OK)
        else:
            return JSONResponse({'status': 'disconnected'}, status_code=HTTP_503_SERVICE_UNAVAILABLE)
    except ConnectionCheckError as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        # 捕获其他未预期异常
        return JSONResponse({'error': 'An unexpected error occurred'}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 创建Starlette应用
app = Starlette(
    debug=True,  # 开启调试模式
    routes=[
        Route('/status', check_connection),  # 定义路由
    ]
)

# 如果直接运行此模块，则启动服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)