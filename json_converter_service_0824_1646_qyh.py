# 代码生成时间: 2025-08-24 16:46:50
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
def convert_json(data: dict) -> dict:
    """Converts a JSON-like dictionary to a JSON serializable format.

    Args:
        data (dict): The dictionary to be converted.

    Returns:
        dict: A JSON serializable dictionary.
    """
    # Use jsonable_encoder to ensure the dictionary is JSON serializable
    return jsonable_encoder(data)

async def json_converter(request: Request) -> JSONResponse:
    """Endpoint to convert JSON data format.

    Args:
        request (Request): The incoming request object.

    Returns:
        JSONResponse: A JSON response with the converted data.
    """
    try:
        # Extract JSON data from the request body
        json_data = await request.json()
        # Convert the JSON data to a serializable format
        converted_data = convert_json(json_data)
        # Return the converted data as a JSON response
        return JSONResponse(content=converted_data)
    except json.JSONDecodeError:
        # Handle JSON decoding errors
        raise StarletteHTTPException(status_code=400, detail="Invalid JSON format")
    except Exception as e:
        # Handle any other unexpected errors
        raise StarletteHTTPException(status_code=500, detail=str(e))

def create_json_converter_app() -> Starlette:
    """Creates a Starlette application with the JSON converter endpoint.

    Returns:
        Starlette: The Starlette application instance.
    """
    # Define the routes for the application
    routes = [
        Route("/convert", endpoint=json_converter, methods=["POST"]),
    ]
    # Create and return the Starlette application
    return Starlette(routes=routes)

# If this script is run directly, create and run the application
if __name__ == "__main__":
    app = create_json_converter_app()
    app.run(debug=True)