# 代码生成时间: 2025-08-05 08:40:17
import requests
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import asyncio
import socket


class NetworkStatusChecker:
    """A class to check network connection status."""
    def __init__(self, timeout=10):
        self.timeout = timeout

    async def check_connection(self, url):
        """Check the connection to a specified URL."""
        try:
            response = await asyncio.get_event_loop().run_in_executor(
                None, lambda: requests.get(url, timeout=self.timeout)
            )
            if response.status_code == 200:
                return {'status': 'connected', 'url': url}
            else:
                return {'status': 'disconnected', 'url': url}
        except requests.RequestException as e:
            return {'status': 'disconnected', 'url': url, 'error': str(e)}
        except Exception as e:
            return {'status': 'error', 'url': url, 'error': str(e)}

    async def check_host(self, host, port=80):
        """Check if a host is reachable on a given port."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            if result == 0:
                return {'status': 'connected', 'host': host, 'port': port}
            else:
                return {'status': 'disconnected', 'host': host, 'port': port}
        except socket.error as e:
            return {'status': 'error', 'host': host, 'port': port, 'error': str(e)}
        except Exception as e:
            return {'status': 'error', 'host': host, 'port': port, 'error': str(e)}


async def check_url(request):
    """Endpoint to check URL connection status."""
    url = request.query_params.get('url')
    if not url:
        return JSONResponse({'error': 'Missing URL parameter'}, status_code=HTTP_400_BAD_REQUEST)
    checker = NetworkStatusChecker()
    result = await checker.check_connection(url)
    return JSONResponse(result, status_code=HTTP_200_OK)

async def check_host_status(request):
    """Endpoint to check host connection status."""
    host = request.query_params.get('host')
    port = request.query_params.get('port', '80')
    if not host:
        return JSONResponse({'error': 'Missing host parameter'}, status_code=HTTP_400_BAD_REQUEST)
    checker = NetworkStatusChecker()
    result = await checker.check_host(host, int(port))
    return JSONResponse(result, status_code=HTTP_200_OK)


app = Starlette(
    routes=[
        Route('/status/url', check_url, methods=['GET']),
        Route('/status/host', check_host_status, methods=['GET']),
    ],
)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)