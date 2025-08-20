# 代码生成时间: 2025-08-20 14:08:20
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
System Performance Monitor using Python and Starlette Framework.
This application provides REST API endpoints to monitor system performance.
"""

class SystemPerformanceMonitor:
    def __init__(self):
        # Initialize system performance monitor
        pass

    def get_cpu_usage(self):
        """Get the current CPU usage as a percentage."""
        try:
            cpu_usage = psutil.cpu_percent()
            return cpu_usage
        except Exception as e:
            # Handle any exception that occurs during CPU usage calculation
            return {"error": str(e)}

    def get_memory_usage(self):
        """Get the current memory usage."""
        try:
            memory = psutil.virtual_memory()
            memory_usage = memory.percent
            return memory_usage
        except Exception as e:
            # Handle any exception that occurs during memory usage calculation
            return {"error": str(e)}

    def get_disk_usage(self):
        """Get the current disk usage."""
        try:
            disk_usage = psutil.disk_usage('/')
            disk_usage_percent = disk_usage.percent
            return disk_usage_percent
        except Exception as e:
            # Handle any exception that occurs during disk usage calculation
            return {"error": str(e)}


# Create a Starlette application instance
app = Starlette(debug=True)

# Define routes for the application
routes = [
    Route("/cpu_usage", endpoint=lambda request: JSONResponse(content={"cpu_usage": system_monitor.get_cpu_usage()}), methods=["GET"]),
    Route("/memory_usage", endpoint=lambda request: JSONResponse(content={"memory_usage": system_monitor.get_memory_usage()}), methods=["GET"]),
    Route("/disk_usage", endpoint=lambda request: JSONResponse(content={"disk_usage": system_monitor.get_disk_usage()}), methods=["GET"]),
]

# Add routes to the application
app.add_routes(routes)

# Create an instance of the SystemPerformanceMonitor class
system_monitor = SystemPerformanceMonitor()
