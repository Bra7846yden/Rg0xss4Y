# 代码生成时间: 2025-09-20 11:38:49
import aiohttp
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.background import BackgroundTask
from urllib.parse import urljoin

"""
A web scraper tool using Python and Starlette framework.
It fetches the content of a webpage and returns it in JSON format.
"""

# Define a function to fetch web page content
async def fetch_content(session, url):
    try:
        # Send a GET request to the URL
        async with session.get(url) as response:
            # Check if the request was successful
            if response.status == 200:
                # Return the text content of the response
                return await response.text()
            else:
                # Return an error message if the request failed
                return f"Error: Unable to fetch content, status code {response.status}"
    except Exception as e:
        # Return the error message if an exception occurs
        return f"Error: {str(e)}"

# Define a route to handle web scraping requests
async def scrape_web_page(request):
    url = request.query_params.get('url')
    if not url:
        # Return an error if the URL is not provided
        return JSONResponse({"error": "URL parameter is missing"}, status_code=400)

    # Create a background task to fetch the web page content
    background_task = BackgroundTask(fetch_content, url)
    request.app.add_background_task(background_task)

    # Return a success response immediately
    return JSONResponse({"message": "Web scraping started"}, status_code=202)

# Create a Starlette application with the defined route
app = Starlette(routes=[
    Route("/scrape", scrape_web_page, methods=["GET"]),
])

# Example usage:
# To start the web server, run the following command in your terminal:
# python web_scraper.py
# Then, you can send a GET request to http://localhost:8000/scrape?url=http://example.com
# to start scraping the content of the webpage.
