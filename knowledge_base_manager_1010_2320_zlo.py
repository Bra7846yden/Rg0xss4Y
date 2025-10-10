# 代码生成时间: 2025-10-10 23:20:52
# knowledge_base_manager.py
# This module provides a basic knowledge base management system using Starlette framework.

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_200_OK

# Define a simple in-memory knowledge base storage
knowledge_base = {}

# Define the routes for the knowledge base management system
routes = [
    Route("/knowledge/{key}", KnowledgeBase, methods=["GET", "POST", "DELETE"]),
]

# Define the KnowledgeBase class handling GET, POST, and DELETE requests
class KnowledgeBase:
    def __init__(self):
        """Initialize the KnowledgeBase handler."""
        pass

    async def get(self, request, key):
        """Retrieve knowledge by key."""
        if key in knowledge_base:
            return JSONResponse(knowledge_base[key], status_code=HTTP_200_OK)
        else:
            return JSONResponse({"detail": "Knowledge not found"}, status_code=HTTP_404_NOT_FOUND)

    async def post(self, request, key):
        """Add or update knowledge."""
        data = await request.json()
        if not data:
            return JSONResponse({"detail": "No data provided"}, status_code=HTTP_400_BAD_REQUEST)
        knowledge_base[key] = data
        return JSONResponse(knowledge_base[key], status_code=HTTP_200_OK)

    async def delete(self, request, key):
        """Delete knowledge by key."""
        if key in knowledge_base:
            del knowledge_base[key]
            return JSONResponse({"detail": "Knowledge deleted"}, status_code=HTTP_200_OK)
        else:
            return JSONResponse({"detail": "Knowledge not found"}, status_code=HTTP_404_NOT_FOUND)

# Create the Starlette application with the defined routes
app = Starlette(debug=True, routes=routes)

# This is where the application starts. In practice, this would be run by a server.
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
