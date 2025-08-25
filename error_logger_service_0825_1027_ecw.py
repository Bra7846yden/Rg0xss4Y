# 代码生成时间: 2025-08-25 10:27:54
import logging
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
import traceback

# Configure the logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ErrorLoggerMiddleware:
    """
    Starlette middleware that logs exceptions and sends a 500 response.
    """
    async def __call__(self, scope, receive, send):
        if scope['type'] == 'lifespan':
            await receive()
        else:
            try:
                await send(scope, receive)
            except Exception as exc:
                self.log_exception(scope, exc)
                await send(scope, receive)
                raise

    async def log_exception(self, scope, exc):
        # Log the exception details
        logger.error(f"Exception: {exc!r}")
        traceback_details = traceback.format_exc()
        logger.error(f"Traceback: {traceback_details}")

app = Starlette(middleware=[ErrorLoggerMiddleware()])

# Define a route that intentionally raises an exception to test the error logging
@app.route("/trigger-error")
async def trigger_error(request):
    raise ValueError("Intentional error for testing.")

# Define a route to retrieve the error logs
@app.route("/error-logs")
async def error_logs(request):
    # This is a mock-up for returning error logs
    # In a real-world scenario, you would query the log storage
    return JSONResponse({'message': 'Error logs retrieved successfully', 'logs': logger.handlers[0].records})

# Define a route for handling HTTP exceptions
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    # Log the HTTP exception details
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)

if __name__ == '__main__':
    from uvicorn import run
    run(app, host='0.0.0.0', port=8000)
