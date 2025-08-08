# 代码生成时间: 2025-08-08 12:18:56
import httpx
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

# 网络连接状态检查器
class NetworkStatusChecker:
    def __init__(self):
        self.base_url = "httpbin.org"

    async def check_status(self):
        """
        检查网络连接状态。
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.head(self.base_url)
                if response.status_code == 200:
                    return {"status": "connected"}
                else:
                    return {"status": "disconnected", "error": response.status_code}
        except httpx.RequestError as e:
            return {"status": "disconnected", "error": str(e)}

# 星型网络状态检查器应用
class NetworkStatusCheckerApp(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route("/check", endpoint=self.check_endpoint, methods=["GET"])
            ]
        )

    async def check_endpoint(self, request):
        """
        提供检查网络连接状态的HTTP端点。
        """
        checker = NetworkStatusChecker()
        status = await checker.check_status()
        if status["status"] == "connected":
            return JSONResponse(status, status_code=HTTP_200_OK)
        else:
            return JSONResponse(status, status_code=HTTP_503_SERVICE_UNAVAILABLE)

# 程序入口点
if __name__ == "__main__":
    app = NetworkStatusCheckerApp()
    app.run(debug=True)