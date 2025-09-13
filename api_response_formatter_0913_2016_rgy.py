# 代码生成时间: 2025-09-13 20:16:21
import json
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR


class APIResponseFormatter:
    """
    A utility class to format API responses in a standardized way.
    """

    def __init__(self):
        pass

    def format_response(self, data, status_code=HTTP_200_OK, message=None):
        """
        Formats the API response with data and an optional message.
        
        Args:
            data (any): The data to be returned in the response.
            status_code (int): The HTTP status code for the response.
            message (str): An optional message to include in the response.
        
        Returns:
            JSONResponse: A JSON response with the formatted data.
        """
        response_data = {
            'status': 'success',
            'data': data,
            'message': message or ''
        }
        return JSONResponse(response_data, status_code=status_code)

    def format_error(self, message, status_code=HTTP_500_INTERNAL_SERVER_ERROR):
        """
        Formats an error response with a message.
        
        Args:
            message (str): The error message to be returned.
            status_code (int): The HTTP status code for the error response.
        
        Returns:
            JSONResponse: A JSON response with the error message.
        """
        response_data = {
            'status': 'error',
            'message': message
        }
        return JSONResponse(response_data, status_code=status_code)


# Example usage of the APIResponseFormatter
if __name__ == '__main__':
    formatter = APIResponseFormatter()
    
    # Example successful response
    response = formatter.format_response({'key': 'value'}, HTTP_200_OK, 'Data retrieved successfully')
    print(response.body)
    
    # Example error response
    error_response = formatter.format_error('An error has occurred', HTTP_500_INTERNAL_SERVER_ERROR)
    print(error_response.body)