# 代码生成时间: 2025-09-13 02:56:59
import re
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.wsgi import WSGIMiddleware


class XSSProtectionMiddleware(BaseHTTPMiddleware):
    """Middleware to prevent XSS attacks by sanitizing user input."""
    def __init__(self, app):
        super().__init__(app)
        self._allowed_tags = ['b', 'em', 'i', 'strong', 'u']

    def _sanitize_input(self, input_string):
        """Sanitizes the input string by removing disallowed HTML tags."""
        # Regex pattern to match HTML tags
        pattern = re.compile(r'<[^>]*>|[^a-zA-Z0-9\s\!\@\#\$\%\^\&\*\(\)\_\+\-\=\[\]\{\}\|\;\:"\`\?\,\.\<\/]+')
        # Replace disallowed tags with nothing
        sanitized_string = re.sub(pattern, '', input_string)
        return sanitized_string

    async def dispatch(self, request: Request, call_next):
        try:
            # Sanitize form data
            if request.method == 'POST':
                for key, value in request.form.items():
                    request.form[key] = self._sanitize_input(value)
            # Sanitize query parameters
            if request.query_params:
                for key, value in request.query_params.items():
                    request.query_params[key] = self._sanitize_input(value)
            # Call the next middleware or application
            response = await call_next(request)
            return response
        except Exception as e:
            return PlainTextResponse(f"An error occurred: {str(e)}", status_code=500)

async def homepage(request: Request):
    """A simple homepage view that displays user input."""
    try:
        user_input = request.query_params.get('input', '')
        sanitized_input = request.app.middlewares[0]._sanitize_input(user_input)
        return Response(f"<h1>Your input: {sanitized_input}</h1>")
    except Exception as e:
        return PlainTextResponse(f"An error occurred: {str(e)}", status_code=500)

# Example usage of the middleware
app = WSGIMiddleware(
    homepage,
    middleware=[XSSProtectionMiddleware]
)
