# 代码生成时间: 2025-08-19 14:21:06
Usage:
    - Run this script to start the web server.
    - Access /memory-usage endpoint to get current memory usage statistics.

Features:
    - Provides a simple API endpoint to check memory usage.
    - Includes error handling for server-side operations.
*/

import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

import psutil

def get_memory_usage():
    """
    Retrieves the current memory usage statistics.
    """
    try:
        memory = psutil.virtual_memory()
        return {
            'total': memory.total,
            'available': memory.available,
            'used': memory.used,
            'percentage': memory.percent,
        }
    except Exception as e:
        raise StarletteHTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

class MemoryUsageAnalyzer(Starlette):
    def __init__(self):
        routes = [
            Route('/memory-usage', endpoint=get_memory_usage, methods=['GET']),
        ]
        super().__init__(routes=routes)

    @staticmethod
    async def error_handler(request, exc):
        """
        Custom error handler for Starlette application.
        """
        if isinstance(exc, StarletteHTTPException):
            return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)
        return JSONResponse({'detail': 'An unexpected error occurred.'}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

if __name__ == '__main__':
    # Run the application
    app = MemoryUsageAnalyzer()
    app.run(host='0.0.0.0', port=8000)
