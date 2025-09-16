# 代码生成时间: 2025-09-17 04:14:59
import logging
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import traceback

# 配置日志
logging.basicConfig(level=logging.ERROR, filename='error.log')
logger = logging.getLogger(__name__)


class ErrorLoggerMiddleware(BaseHTTPMiddleware):
    """
    错误日志收集器中间件
    """
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # 记录错误日志
            logger.error(f'Error: {str(exc)}')
            logger.error(traceback.format_exc())
            # 返回错误响应
            return JSONResponse(
                content={"detail": f'Internal Server Error: {str(exc)}'},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )


async def start_error_logger_service():
    """
    启动错误日志收集器服务
    """
    app = Starlette()
    # 添加中间件
    app.add_middleware(ErrorLoggerMiddleware)
    # 启动服务
    await app.serve(port=8000)

# 检查是否直接执行脚本，如果是，则启动服务
if __name__ == '__main__':
    from uvicorn import run
    run(start_error_logger_service, host='0.0.0.0', port=8000)