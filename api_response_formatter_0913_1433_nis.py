# 代码生成时间: 2025-09-13 14:33:22
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback


class APIResponseFormatterMiddleware:
    """
    Middleware to format API responses.
    This middleware catches the responses from the application and
    adds a standardized structure to them, including a status code and message.
    """
    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await send(scope, receive, send)
            return

        response = await send(scope, receive, send)

        # Check if response is a JSONResponse
        if not isinstance(response, JSONResponse):
            return response

        # Format the response
        try:
            data = response.media
            formatted_response = self.format_response(data)
            return JSONResponse(formatted_response)
        except Exception as e:
            formatted_error = self.format_error(str(e), 500)
            return JSONResponse(formatted_error, status_code=500)

    def format_response(self, data):
        """
        Formats the response data into a standardized structure.
        """
        return {
            "status": "success",
            "data": data
        }

    def format_error(self, message, status_code):
        """
        Formats the error message into a standardized structure.
        """
        return {
            "status": "error",
            "message": message,
            "status_code": status_code
        }


async def homepage(request):
    """
    Homepage endpoint.
    Returns a greeting message in a formatted response.
    """
    return JSONResponse(
        {
            "message": "Welcome to the API!"
        },
        status_code=200
    )


async def error_404(request):
    """
    404 error endpoint.
    Returns a formatted error message when a route is not found.
    """
    return JSONResponse(
        APIResponseFormatterMiddleware().format_error(
            "The requested resource was not found.",
            404
        ),
        status_code=404
    )


app = Starlette(
    routes=[
        Route("/", endpoint=homepage),
        Route("/error", endpoint=error_404),
    ],
    middleware=[
        APIResponseFormatterMiddleware(),
    ]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)