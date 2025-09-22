# 代码生成时间: 2025-09-23 01:07:36
import shutil
from starlette.applications import Starlette
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import zipfile
from pathlib import Path
import logging

"""
Decompression tool using Python and Starlette framework.
This application provides an endpoint to decompress uploaded zip files.
"""

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the application
app = Starlette(debug=True)

# Define routes
routes = [
    Route("/decompress", endpoint=decompress_file, methods=["POST"]),
]

# Register routes
app.add_routes(routes)

"""
Endpoint to handle file decompression.
This endpoint expects a multipart/form-data request containing a zip file.
It will decompress the file and return a JSON response with the result.
"""
async def decompress_file(request: Request):
    # Get the uploaded file from the request
    file = await request.form()
    zip_file = file.get('file')

    # Check if a file was uploaded
    if not zip_file:
        return JSONResponse(status_code=400, content={"message": "No file uploaded"})

    # Extract the zip file to a temporary directory
    temp_dir = Path("temp")
    temp_dir.mkdir(exist_ok=True)
    try:
        # Save the zip file to the temporary directory
        zip_file_path = temp_dir / zip_file.filename
        with open(zip_file_path, 'wb') as f:
            await zip_file.save(f)

        # Decompress the zip file
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # Return a success response
        return JSONResponse(content={"message": "File decompressed successfully"})
    except Exception as e:
        # Handle any exceptions and return an error response
        logger.error(f"Error decompressing file: {e}")
        return JSONResponse(status_code=500, content={"message": "Error decompressing file"})
    finally:
        # Clean up the temporary directory
        shutil.rmtree(temp_dir)
