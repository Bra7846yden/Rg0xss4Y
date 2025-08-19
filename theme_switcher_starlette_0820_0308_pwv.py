# 代码生成时间: 2025-08-20 03:08:59
# theme_switcher_starlette.py

"""
Starlette application that provides theme switching functionality.
"""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.sessions import SessionMiddleware
from starlette.requests import Request
from starlette.middleware import Middleware
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

# Middleware for session management
middleware = [
    Middleware(SessionMiddleware, secret_key=\