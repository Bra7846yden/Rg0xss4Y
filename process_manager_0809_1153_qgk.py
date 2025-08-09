# 代码生成时间: 2025-08-09 11:53:57
import subprocess
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import signal
import os
import psutil

class ProcessManager:
    """进程管理器类，用于管理进程的启动和停止。"""
    def __init__(self):
        self.processes = {}

    def start_process(self, name, command):
        """启动一个进程。"""
        try:
            process = subprocess.Popen(command, shell=True)
            self.processes[name] = process
            return {'status': 'success', 'message': f'Process {name} started.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def stop_process(self, name):
        """停止一个进程。"""
        try:
            process = self.processes.get(name)
            if process:
                process.terminate()
                process.wait()
                del self.processes[name]
                return {'status': 'success', 'message': f'Process {name} stopped.'}
            else:
                return {'status': 'error', 'message': f'Process {name} not found.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def list_processes(self):
        """列出所有管理的进程。"""
        return {'status': 'success', 'processes': list(self.processes.keys())}

    def kill_process(self, name):
        """强制结束一个进程。"""
        try:
            process = self.processes.get(name)
            if process:
                os.kill(process.pid, signal.SIGKILL)
                del self.processes[name]
                return {'status': 'success', 'message': f'Process {name} killed.'}
            else:
                return {'status': 'error', 'message': f'Process {name} not found.'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

async def start_process_endpoint(request):
    """启动进程的API端点。"""
    name = request.query_params.get('name')
    command = request.query_params.get('command')
    process_manager = ProcessManager()
    result = process_manager.start_process(name, command)
    return JSONResponse(result)

async def stop_process_endpoint(request):
    """停止进程的API端点。"""
    name = request.query_params.get('name')
    process_manager = ProcessManager()
    result = process_manager.stop_process(name)
    return JSONResponse(result)

async def list_processes_endpoint(request):
    """列出所有进程的API端点。"""
    process_manager = ProcessManager()
    result = process_manager.list_processes()
    return JSONResponse(result)

async def kill_process_endpoint(request):
    """强制结束进程的API端点。"""
    name = request.query_params.get('name')
    process_manager = ProcessManager()
    result = process_manager.kill_process(name)
    return JSONResponse(result)

app = Starlette(
    routes=[
        Route('/start-process', endpoint=start_process_endpoint, methods=['GET']),
        Route('/stop-process', endpoint=stop_process_endpoint, methods=['GET']),
        Route('/list-processes', endpoint=list_processes_endpoint, methods=['GET']),
        Route('/kill-process', endpoint=kill_process_endpoint, methods=['GET']),
    ]
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)