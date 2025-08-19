# 代码生成时间: 2025-08-19 18:45:36
import os
import subprocess
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

"""
A simple process manager using the Starlette framework.
It allows starting, stopping, and listing processes.
"""

class ProcessManager:
    def __init__(self):
        self.processes = {}  # Store process information

    def start_process(self, command):
        """
        Start a new process and store its information.
        :param command: The command to run the process with.
        :return: The process ID.
        """
        try:
            process = subprocess.Popen(command, shell=True)
            self.processes[process.pid] = {'pid': process.pid, 'command': command, 'status': 'running'}
            return process.pid
        except Exception as e:
            raise Exception(f"Failed to start process: {e}")

    def stop_process(self, pid):
        """
        Stop a process by its PID.
        :param pid: The process ID to stop.
        :return: A success message.
        """
        if pid in self.processes:
            try:
                os.kill(pid, 9)  # SIGKILL signal
                self.processes[pid]['status'] = 'stopped'
                return f"Process {pid} stopped successfully."
            except Exception as e:
                raise Exception(f"Failed to stop process {pid}: {e}")
        else:
            raise Exception(f"No process found with PID {pid}.")

    def list_processes(self):
        """
        List all processes with their status.
        :return: A list of process information.
        """
        return self.processes


def start_process(request):
    command = request.query_params.get('command')
    if not command:
        return JSONResponse({'error': 'Missing command parameter.'}, status_code=HTTP_400_BAD_REQUEST)
    
    process_manager = ProcessManager()
    pid = process_manager.start_process(command)
    return JSONResponse({'message': f'Process started with PID {pid}', 'pid': pid}, status_code=HTTP_200_OK)


def stop_process(request):
    pid = request.query_params.get('pid')
    if not pid:
        return JSONResponse({'error': 'Missing PID parameter.'}, status_code=HTTP_400_BAD_REQUEST)
    try:
        pid = int(pid)
    except ValueError:
        return JSONResponse({'error': 'Invalid PID parameter.'}, status_code=HTTP_400_BAD_REQUEST)
    
    process_manager = ProcessManager()
    try:
        message = process_manager.stop_process(pid)
        return JSONResponse({'message': message}, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)


def list_processes_endpoint(request):
    process_manager = ProcessManager()
    processes = process_manager.list_processes()
    return JSONResponse({'processes': processes}, status_code=HTTP_200_OK)

# Set up the Starlette application
app = Starlette(
    routes=[
        Route('/start', endpoint=start_process),
        Route('/stop', endpoint=stop_process),
        Route('/list', endpoint=list_processes_endpoint),
    ]
)
