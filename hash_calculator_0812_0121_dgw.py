# 代码生成时间: 2025-08-12 01:21:34
# hash_calculator.py
"""
A simple hash calculator tool using the Starlette framework.
This tool allows users to calculate the hash value of a given input.
"""
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import hashlib
import hmac
import secrets
import asyncio

# Define the main application class
class HashCalculator(Starlette):
    def __init__(self):
        # Define the routes for the application
        routes = [
            Route("/hash", endpoint=self.calculate_hash, methods=["POST"]),
        ]
        super().__init__(routes=routes)

    # Define the endpoint for calculating hash values
    async def calculate_hash(self, request: Request):
        # Get the input data from the request body
        data = await request.json()
        
        # Check if the input data is valid
        if not isinstance(data, dict) or 'input' not in data:
            return JSONResponse(
                content={"error": "Invalid input data"}, status_code=400
            )
        
        # Extract the input string to be hashed
        input_string = data['input']
        
        # Calculate the hash value
        try:
            hash_value = hashlib.sha256(input_string.encode()).hexdigest()
        except Exception as e:
            # Handle any unexpected errors during hashing
            return JSONResponse(
                content={"error": str(e)}, status_code=500
            )
        
        # Return the calculated hash value in the response
        return JSONResponse(content={"hash": hash_value})

# Run the application
if __name__ == '__main__':
    application = HashCalculator()
    asyncio.run(application.run(host='127.0.0.1', port=8000))
