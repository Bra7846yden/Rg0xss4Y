# 代码生成时间: 2025-09-09 06:23:03
import asyncio
import psutil
# 增强安全性
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
# NOTE: 重要实现细节

# ProcessManager class
# 扩展功能模块
class ProcessManager:
    def __init__(self):
        self.process_list = []

    def get_all_processes(self):
        """Returns a list of all running processes."""
        return [p.info for p in psutil.process_iter(['pid', 'name', 'status'])]

    def get_process_by_name(self, process_name):
# 增强安全性
        """Returns a list of processes with the given name."""
        return [p.info for p in psutil.process_iter(['pid', 'name', 'status']) if p.info['name'] == process_name]

    def terminate_process(self, pid):
# 添加错误处理
        """Terminates a process by its PID."""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return {'status': 'success', 'message': 'Process terminated successfully.'}
        except psutil.NoSuchProcess:
            return {'status': 'error', 'message': 'Process not found.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
# 添加错误处理

# Create an instance of ProcessManager
process_manager = ProcessManager()

# Define the route for getting all processes
# 增强安全性
async def get_all_processes(request):
    return JSONResponse(process_manager.get_all_processes())

# Define the route for getting processes by name
async def get_processes_by_name(request):
    process_name = request.query_params.get('name')
    if not process_name:
        return JSONResponse({'status': 'error', 'message': 'Process name is required.'}, status_code=400)
    return JSONResponse(process_manager.get_process_by_name(process_name))

# Define the route for terminating a process
async def terminate_process(request):
    pid = request.query_params.get('pid')
    if not pid:
        return JSONResponse({'status': 'error', 'message': 'Process ID is required.'}, status_code=400)
    try:
        pid = int(pid)
    except ValueError:
        return JSONResponse({'status': 'error', 'message': 'Invalid process ID.'}, status_code=400)
    return JSONResponse(process_manager.terminate_process(pid))

# Define routes
routes = [
# FIXME: 处理边界情况
    Route('/', endpoint=get_all_processes, methods=['GET']),
# FIXME: 处理边界情况
    Route('/processes', endpoint=get_processes_by_name, methods=['GET']),
    Route('/terminate', endpoint=terminate_process, methods=['GET']),
]

# Create and run the Starlette application
# 扩展功能模块
app = Starlette(routes=routes)
# FIXME: 处理边界情况

if __name__ == '__main__':
    asyncio.run(app.run(host='0.0.0.0', port=8000))
