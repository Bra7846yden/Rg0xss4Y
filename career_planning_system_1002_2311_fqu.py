# 代码生成时间: 2025-10-02 23:11:56
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Any, Dict

# Define the CareerPlanner class to handle career planning data
class CareerPlanner:
    def __init__(self):
        self.careers = {
            'developer': {'description': 'Develop software applications', 'requirements': ['programming languages', 'algorithms']},
            'designer': {'description': 'Design user interfaces and experiences', 'requirements': ['UX design', 'visual design']},
        }

    def get_career_info(self, career_name: str) -> Dict[str, Any]:
        """
        Get career information by name.
        :param career_name: The name of the career to retrieve information for.
        :return: A dictionary containing career details.
        """
        return self.careers.get(career_name, {})

    def add_career(self, career_name: str, career_info: Dict[str, Any]) -> bool:
        """
        Add a new career to the system.
        :param career_name: The name of the career to add.
        :param career_info: A dictionary containing career details.
        :return: True if the career was added successfully, False otherwise.
        """
        if career_name in self.careers:
            return False
        self.careers[career_name] = career_info
        return True

# Define the API routes
routes = [
    Route('/api/careers/{career_name}', endpoint=CareerPlanner.as_view()),
]

# Define the Starlette application
app = Starlette(debug=True, routes=routes)

# Implement the ASGI endpoint for handling requests
@app.route('/api/careers/{career_name}')
async def get_career(app: Starlette, request: Request, career_name: str):
    """
    Handle GET request for career information.
    :param app: The Starlette application instance.
    :param request: The incoming request.
    :param career_name: The name of the career to retrieve information for.
    :return: A JSON response containing career details.
    """
    try:
        planner = CareerPlanner()
        career_info = planner.get_career_info(career_name)
        if not career_info:
            return JSONResponse({'detail': f'Career {career_name} not found'}, status_code=HTTP_404_NOT_FOUND)
        return JSONResponse(career_info)
    except Exception as e:
        return JSONResponse({'detail': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# Implement the ASGI endpoint for adding new careers
@app.route('/api/careers', methods=['POST'])
async def add_career(request: Request):
    """
    Handle POST request for adding a new career.
    :param request: The incoming request.
    :return: A JSON response indicating success or failure.
    """
    try:
        planner = CareerPlanner()
        data = await request.json()
        career_name = data.get('career_name')
        career_info = data.get('career_info')
        if not career_name or not career_info:
            return JSONResponse({'detail': 'Missing career name or information'}, status_code=HTTP_400_BAD_REQUEST)
        if not planner.add_career(career_name, career_info):
            return JSONResponse({'detail': f'Career {career_name} already exists'}, status_code=HTTP_400_BAD_REQUEST)
        return JSONResponse({'detail': f'Career {career_name} added successfully'}, status_code=HTTP_201_CREATED)
    except Exception as e:
        return JSONResponse({'detail': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)