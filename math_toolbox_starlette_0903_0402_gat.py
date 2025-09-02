# 代码生成时间: 2025-09-03 04:02:41
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.status
from starlette.requests import Request
import math
"""
Math Toolbox API using Starlette framework
This application provides a simple REST API for various mathematical calculations.
"""

class MathToolbox:
    def __init__(self):
        pass

    def add(self, x: float, y: float) -> float:
        """
        Adds two numbers and returns the result.
        :param x: First number
        :param y: Second number
        :return: Sum of x and y
        """
        return x + y

    def subtract(self, x: float, y: float) -> float:
        """
        Subtracts y from x and returns the result.
        :param x: First number
        :param y: Second number
        :return: Difference of x and y
        """
        return x - y

    def multiply(self, x: float, y: float) -> float:
        """
        Multiplies two numbers and returns the result.
        :param x: First number
        :param y: Second number
        :return: Product of x and y
        """
        return x * y

    def divide(self, x: float, y: float) -> float:
        """
        Divides x by y and returns the result.
        :param x: First number
        :param y: Second number
        :return: Quotient of x and y
        :raises: ZeroDivisionError if y is zero
        """
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return x / y

    def calculate(self, operation: str, x: float, y: float) -> float:
        """
        Performs a mathematical calculation based on the given operation.
        :param operation: The operation to perform (add, subtract, multiply, divide)
        :param x: First number
        :param y: Second number
        :return: Result of the operation
        :raises: ValueError if the operation is not supported
        """
        operations = {
            "add": self.add,
            "subtract": self.subtract,
            "multiply": self.multiply,
            "divide": self.divide
        }

        if operation not in operations:
            raise ValueError("Unsupported operation.")

        return operations[operation](x, y)


def math_operation(request: Request, operation: str, x: float = None, y: float = None):
    """
    Handles the math operation requests.
    :param request: The incoming Starlette request object
    :param operation: The operation to perform (add, subtract, multiply, divide)
    :param x: First number
    :param y: Second number
    :return: A JSON response with the result of the operation
    """
    try:
        toolbox = MathToolbox()
        result = toolbox.calculate(operation, x, y)
        return starlette.responses.JSONResponse(content={"result": result}, media_type="application/json")
    except Exception as e:
        return starlette.responses.JSONResponse(content={"error": str(e)}, media_type="application/json", status_code=starlette.status.HTTP_400_BAD_REQUEST)


def app(**kwargs):
    return starlette.applications.starlette_app(
        routes=[
            starlette.routing.Route("/math/{operation}", endpoint=math_operation),
        ],
        **kwargs
    )
