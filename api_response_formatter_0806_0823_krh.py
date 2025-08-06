# 代码生成时间: 2025-08-06 08:23:11
import json
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import FastAPI, HTTPException
from typing import Any, Dict, Optional

# 创建FastAPI应用实例
def create_app() -> FastAPI:
    app = FastAPI()
    return app

# API响应格式化工具类
class ApiResponseFormatter:
    """用于格式化API响应的工具类"""

    def __init__(self, status_code: int = 200, error: Optional[str] = None):
        self.status_code = status_code
        self.error = error
        self.data = {}

    def set_data(self, data: Any) -> None:
        """设置响应数据"""
        self.data = data

    def set_error(self, error: str) -> None:
        """设置错误信息"""
        self.error = error

    def format_response(self) -> JSONResponse:
        """格式化响应数据为JSONResponse对象"""
        if self.error:
            return JSONResponse(
                content={"error": self.error},
                status_code=self.status_code
            )
        else:
            return JSONResponse(
                content={"data": self.data},
                status_code=self.status_code
            )

# 路由处理函数
@app.get("/")
async def root(request: Request):
    # 使用ApiResponseFormatter来格式化响应
    formatter = ApiResponseFormatter()
    formatter.set_data({"message": "Hello, World!"})
    return formatter.format_response()

# 错误处理函数
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    # 使用ApiResponseFormatter来格式化异常响应
    formatter = ApiResponseFormatter(exc.status_code, str(exc))
    return formatter.format_response()

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(create_app(), host='0.0.0.0', port=8000)