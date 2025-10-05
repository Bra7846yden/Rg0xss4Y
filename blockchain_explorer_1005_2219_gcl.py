# 代码生成时间: 2025-10-05 22:19:43
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
# NOTE: 重要实现细节
import httpx
# NOTE: 重要实现细节
import json
from typing import Dict


# Constants for the blockchain API
API_URL = "https://blockchain.info/unspent?active="
# 增强安全性
ADDRESS_PARAM = "address="
LIMIT_PARAM = "&limit="

# Custom Middleware to handle errors
class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code >= 400:
# TODO: 优化性能
            return JSONResponse(
                content={"message": "An error occurred"},
# 改进用户体验
                status_code=response.status_code
            )
        return response

# BlockchainExplorer class to encapsulate the logic
class BlockchainExplorer:
    def __init__(self, address: str, limit: int = 10):
# 扩展功能模块
        self.address = address
        self.limit = limit

    def fetch_unspent_transactions(self) -> Dict:
        """
        Fetch unspent transactions for the given address.
# FIXME: 处理边界情况

        Returns a list of unspent transactions.
# TODO: 优化性能
        """
# TODO: 优化性能
        try:
            response = httpx.get(
                f"{API_URL}{ADDRESS_PARAM}{self.address}{LIMIT_PARAM}{self.limit}"
            )
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            return {"error": str(e)}

# Routes for the Starlette application
routes = [
    Route("/", lambda req: PlainTextResponse("Welcome to the Blockchain Explorer!")),
    Route("/unspent/{address}", lambda req: unspent_transactions(req.path_params["address"])),
    Route("/unspent/{address}/{limit}", lambda req: unspent_transactions(req.path_params["address"], req.path_params["limit"])),
]

# Async function to handle unspent transactions endpoint
async def unspent_transactions(address: str, limit: str = "10"):
    explorer = BlockchainExplorer(address, int(limit))
    unspent = explorer.fetch_unspent_transactions()
# NOTE: 重要实现细节
    if "error" in unspent:
        return JSONResponse(content={"message": unspent["error"]}, status_code=500)
    return JSONResponse(content=unspent)
# 扩展功能模块

# Create a Starlette application with middleware and routes
app = Starlette(
    middleware=[Middleware(ErrorHandlingMiddleware)],
    routes=routes,
)
# 增强安全性

# Run the application
# 优化算法效率
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)