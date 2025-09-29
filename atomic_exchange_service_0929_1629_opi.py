# 代码生成时间: 2025-09-29 16:29:27
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
import asyncio
import logging

# 设置日志记录器
logger = logging.getLogger(__name__)

class AtomicExchangeService:
    """Atomic Exchange Service for handling atomic operations."""
    def __init__(self):
        self.data = {}

    async def atomic_exchange(self, key, value):
        """
        Perform an atomic exchange operation.

        Args:
            key (str): The key to exchange.
            value: The new value to set for the key.

        Returns:
            tuple: A tuple containing the old value and the new value.
        """
        try:
            old_value = self.data.get(key)
            self.data[key] = value
            return old_value, value
        except Exception as e:
            logger.error(f"Error during atomic exchange: {e}")
            raise

    async def get_value(self, key):
        """
        Get the value associated with a key.

        Args:
            key (str): The key to retrieve.

        Returns:
            any: The value associated with the key or None if not found.
        """
        try:
            return self.data.get(key)
        except Exception as e:
            logger.error(f"Error during get operation: {e}")
            raise

# 创建AtomicExchangeService的实例
atomic_exchange_service = AtomicExchangeService()

# 定义路由和处理函数
async def atomic_exchange_endpoint(request):
    """Endpoint to perform an atomic exchange operation."""
    try:
        key = request.query_params.get('key')
        value = await request.json()
        if not key or not value:
            return JSONResponse({'detail': 'Key and value are required'}, status_code=HTTP_400_BAD_REQUEST)
        old_value, new_value = await atomic_exchange_service.atomic_exchange(key, value)
        return JSONResponse({'old_value': old_value, 'new_value': new_value})
    except Exception as e:
        logger.error(f"Error in atomic_exchange_endpoint: {e}")
        return JSONResponse({'detail': 'An error occurred'}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

async def get_value_endpoint(request):
    """Endpoint to get the value associated with a key."""
    try:
        key = request.query_params.get('key')
        if not key:
            return JSONResponse({'detail': 'Key is required'}, status_code=HTTP_400_BAD_REQUEST)
        value = await atomic_exchange_service.get_value(key)
        if value is None:
            return JSONResponse({'detail': 'Not found'}, status_code=HTTP_404_NOT_FOUND)
        return JSONResponse({'value': value})
    except Exception as e:
        logger.error(f"Error in get_value_endpoint: {e}")
        return JSONResponse({'detail': 'An error occurred'}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 创建Starlette应用并添加路由
app = Starlette(
    routes=[
        Route('/api/atomic-exchange', endpoint=atomic_exchange_endpoint, methods=['POST']),
        Route('/api/get-value', endpoint=get_value_endpoint, methods=['GET'])
    ]
)

# 运行应用
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)