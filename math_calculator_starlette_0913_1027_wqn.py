# 代码生成时间: 2025-09-13 10:27:44
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.status
from starlette.requests import Request

"""
A simple math calculator API using Starlette framework.
"""

# Define the MathCalculator class with methods for various mathematical operations.
class MathCalculator:
    def add(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers."""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divide two numbers."""
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b

# Create a route handler for each mathematical operation.
async def add_route(request: Request) -> starlette.responses.Response:
    a = float(request.query_params['a'])
    b = float(request.query_params['b'])
    calculator = MathCalculator()
    result = calculator.add(a, b)
    return starlette.responses.JSONResponse({'result': result})

async def subtract_route(request: Request) -> starlette.responses.Response:
    a = float(request.query_params['a'])
    b = float(request.query_params['b'])
    calculator = MathCalculator()
    result = calculator.subtract(a, b)
    return starlette.responses.JSONResponse({'result': result})

async def multiply_route(request: Request) -> starlette.responses.Response:
    a = float(request.query_params['a'])
    b = float(request.query_params['b'])
    calculator = MathCalculator()
    result = calculator.multiply(a, b)
    return starlette.responses.JSONResponse({'result': result})

async def divide_route(request: Request) -> starlette.responses.Response:
    a = float(request.query_params['a'])
    b = float(request.query_params['b'])
    calculator = MathCalculator()
    try:
        result = calculator.divide(a, b)
        return starlette.responses.JSONResponse({'result': result})
    except ValueError as e:
        return starlette.responses.Response(str(e), status_code=starlette.status.HTTP_400_BAD_REQUEST)

# Define the routing for the API.
routes = [
    starlette.routing.Route('/add', add_route, methods=['GET']),
    starlette.routing.Route('/subtract', subtract_route, methods=['GET']),
    starlette.routing.Route('/multiply', multiply_route, methods=['GET']),
    starlette.routing.Route('/divide', divide_route, methods=['GET']),
]

# Create the Starlette application.
app = starlette.applications Starlette(debug=True, routes=routes)

# If this module is the main program, run the application.
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)