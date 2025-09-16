# 代码生成时间: 2025-09-16 20:08:04
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK

"""
Memory Usage Analysis API using Python and Starlette framework.
This application provides an endpoint to retrieve current memory usage statistics.
"""

class MemoryUsageAnalysis:
    def __init__(self):
        self.memory = psutil.virtual_memory()

    def get_memory_usage(self):
        """
        Get current memory usage statistics.
        """
        try:
            # Get the current memory usage stats
            current_memory = psutil.virtual_memory()
            return {
                'total': current_memory.total,
                'available': current_memory.available,
                'used': current_memory.used,
                'free': current_memory.free,
                'percent': current_memory.percent,
            }
        except Exception as e:
            # Handle any exceptions that may occur
            return {'error': str(e)}

    def get_memory_usage_handler(self, request):
        """
        Endpoint handler for /memory-usage endpoint.
        """
        memory_usage = self.get_memory_usage()
        return JSONResponse(content=memory_usage, status_code=HTTP_200_OK)

# Create an instance of the MemoryUsageAnalysis class
memory_usage_analysis = MemoryUsageAnalysis()

# Define the routes for the application
routes = [
    Route("/memory-usage", memory_usage_analysis.get_memory_usage_handler, methods=["GET"]),
]

# Create a Starlette application with the defined routes
app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    # Run the application
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
