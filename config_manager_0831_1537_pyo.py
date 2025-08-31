# 代码生成时间: 2025-08-31 15:37:28
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.exceptions import HTTPException as StarletteHTTPException


class ConfigManager:
    """
    A class for managing application configurations.
    """
    def __init__(self, config_file):
        self.config_file = config_file
        self.config_data = self.load_config()

    def load_config(self):
        """
        Load the configuration from a JSON file.
        """
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            raise Exception(f"Configuration file '{self.config_file}' not found.")
        except json.JSONDecodeError:
            raise Exception(f"Invalid JSON in configuration file '{self.config_file}'.")

    def get_config(self):
        """
        Return the loaded configuration data.
        """
        return self.config_data

    def update_config(self, key, value):
        """
        Update a configuration value.
        """
        if key in self.config_data:
            self.config_data[key] = value
            with open(self.config_file, 'w') as file:
                json.dump(self.config_data, file, indent=4)
        else:
            raise KeyError(f"Key '{key}' not found in configuration.")


async def get_config_endpoint(request):
    """
    Endpoint to retrieve the current configuration.
    """
    try:
        config_manager = ConfigManager('config.json')
        return JSONResponse(config_manager.get_config())
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

async def update_config_endpoint(request):
    """
    Endpoint to update the configuration.
    """
    data = await request.json()
    try:
        config_manager = ConfigManager('config.json')
        config_manager.update_config(data['key'], data['value'])
        return JSONResponse({'message': 'Configuration updated successfully.'})
    except KeyError as ke:
        return JSONResponse({'error': str(ke)}, status_code=HTTP_404_NOT_FOUND)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


# Define the Starlette application with routes
app = Starlette(
    routes=[
        Route('/get-config', endpoint=get_config_endpoint, methods=['GET']),
        Route('/update-config', endpoint=update_config_endpoint, methods=['POST']),
    ],
    exception_handlers={
        HTTP_404_NOT_FOUND: lambda request, exc: JSONResponse({'error': 'Not found'}, status_code=HTTP_404_NOT_FOUND),
        HTTP_500_INTERNAL_SERVER_ERROR: lambda request, exc: JSONResponse({'error': 'Internal server error'}, status_code=HTTP_500_INTERNAL_SERVER_ERROR),
    },
)
