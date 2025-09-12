# 代码生成时间: 2025-09-12 13:51:31
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import random
import json

# Random Number Generator API
class RandomNumberAPI:
    def __init__(self):
        # Define routes
        self.routes = [
            Route("/random", self.generate_random, methods=["GET"]),
        ]

    def generate_random(self, request):
        """
        Generates a random number and returns it as a JSON response.
        If no parameters are provided, it returns a random integer between 1 and 100.
        If parameters are provided, it uses the parameters to define the range.
        """
        # Default parameters
        low = 1
        high = 100
        try:
            # Parse query parameters
            query_params = request.query_params
            if "low" in query_params:
                low = int(query_params["low"])
            if "high" in query_params:
                high = int(query_params["high"])
            # Validate parameters
            if low > high:
                raise ValueError("Low value cannot be greater than high value.")
        except ValueError as e:
            return JSONResponse(
                content={"error": str(e)}, status_code=HTTP_400_BAD_REQUEST
            )
        # Generate random number
        random_number = random.randint(low, high)
        return JSONResponse(content={"random_number": random_number}, status_code=HTTP_200_OK)

# Create an instance of the RandomNumberAPI
app = RandomNumberAPI()

# Start the server
if __name__ == "__main__":
    app = Starlette(routes=app.routes)
    uvicorn.run(app, host="0.0.0.0", port=8000)