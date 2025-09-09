# 代码生成时间: 2025-09-10 05:19:11
# url_validator_service.py
"""
A Starlette-based service to validate the validity of a URL.
"""

import re
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST
from urllib.parse import urlparse, parse_qs


def is_valid_url(url):
    """
    Validates if the provided URL is well-formed.
    """
    try:
        result = urlparse(url)
        # Check for scheme, netloc and path to ensure it's a valid URL
        if all([result.scheme, result.netloc, result.path]):
            return True
        return False
    except ValueError:
        return False


def url_validator(request):
    """
    Handles the request to validate a URL.
    """
    url = request.query_params.get('url')
    if not url:
        return JSONResponse({'error': 'No URL provided.'}, status_code=HTTP_400_BAD_REQUEST)

    if is_valid_url(url):
        return JSONResponse({'message': 'The URL is valid.', 'url': url})
    else:
        return JSONResponse({'error': 'The URL is invalid.'}, status_code=HTTP_400_BAD_REQUEST)


def create_app():
    """
    Creates a Starlette application with the URL validator endpoint.
    """
    routes = [
        Route('/', url_validator)
    ]
    return Starlette(debug=True, routes=routes)

if __name__ == '__main__':
    app = create_app()
    app.run()
    # Note: In a production environment, you would use a WSGI server like uvicorn to serve the application.
