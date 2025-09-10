# 代码生成时间: 2025-09-10 12:01:36
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

"""
Memory Analysis Service using Starlette Framework
This service provides an endpoint to analyze memory usage statistics.
"""

class MemoryUsageService:
    def __init__(self):
        pass

    def get_memory_usage(self):
        """
        Returns current memory usage statistics.
        """
        try:
            mem = psutil.virtual_memory()
            return {
                'total': mem.total,
                'available': mem.available,
                'used': mem.used,
                'free': mem.free,
                'percent': mem.percent
            }
        except Exception as e:
            raise Exception(f"Failed to retrieve memory usage: {e}")


def memory_usage_endpoint(request):
    """
    Endpoint to handle memory usage requests.
    """
    service = MemoryUsageService()
    try:
        memory_usage = service.get_memory_usage()
        return JSONResponse(status_code=HTTP_200_OK, content=memory_usage)
    except Exception as e:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={'error': str(e)})


def create_application():
    """
    Creates and returns the Starlette application.
    """
    routes = [
        Route("/memory", endpoint=memory_usage_endpoint, methods=["GET"]),
    ]
    return Starlette(routes=routes)

if __name__ == "__main__":
    app = create_application()
    app.run(debug=True)