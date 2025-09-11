# 代码生成时间: 2025-09-12 07:50:05
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request

"""
Memory Usage Analyzer

This Starlette application provides a simple API endpoint to get the current memory usage
statistics of the system. It uses the psutil library to collect memory usage data.
"""

# Define the API endpoint for memory usage statistics
routes = [
    Route("/memory-usage", endpoint=MemoryUsage, methods=["GET"]),
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)

class MemoryUsage:
    """
    A class-based view to handle memory usage requests.
    It provides a GET method to retrieve memory usage statistics.
    """
    async def __call__(self, request: Request):
        """
        The method called when the endpoint is accessed.
        Returns a JSON response with the memory usage statistics.
        """
        try:
            # Get memory usage statistics
            mem_stats = psutil.virtual_memory()
            # Create a response dictionary with the memory usage statistics
            response_data = {
                "total": mem_stats.total,
                "available": mem_stats.available,
                "used": mem_stats.used,
                "free": mem_stats.free,
                "percent": mem_stats.percent,
            }
            # Return the response with a 200 status code
            return JSONResponse(response_data, status_code=200)
        except Exception as e:
            # Handle any exceptions and return a 500 status code
            return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    # Run the application if the script is run directly
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)