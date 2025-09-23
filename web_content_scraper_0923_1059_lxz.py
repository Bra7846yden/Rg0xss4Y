# 代码生成时间: 2025-09-23 10:59:12
# web_content_scraper.py
# A Starlette application for scraping web content.
# NOTE: 重要实现细节

import aiohttp
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
# 增强安全性
from bs4 import BeautifulSoup

# Define the endpoint for scraping web content.
APP_ROUTES = [
    Route('/scrape', endpoint=ScrapeEndpoint, methods=['POST']),
]

class ScrapeEndpoint:
# NOTE: 重要实现细节
    async def __call__(self, request):
        # Extract the URL from the request body.
        try:
            data = await request.json()
            url = data.get('url')
            if not url:
                return JSONResponse(
                    content={'error': 'Missing URL parameter.'},
                    status_code=HTTP_400_BAD_REQUEST
                )
        except ValueError:
            return JSONResponse(
                content={'error': 'Invalid JSON format.'},
                status_code=HTTP_400_BAD_REQUEST
            )

        # Perform the web scraping.
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != HTTP_200_OK:
                        return JSONResponse(
                            content={'error': 'Failed to fetch the webpage.'},
                            status_code=response.status
                        )
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    content = soup.get_text(separator=' ', strip=True)
                    return JSONResponse(
                        content={'url': url, 'content': content},
                        status_code=HTTP_200_OK
                    )
        except aiohttp.ClientError as e:
# 改进用户体验
            return JSONResponse(
                content={'error': f'HTTP client error: {e}'},
# 添加错误处理
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            return JSONResponse(
                content={'error': f'Unexpected error: {e}'},
                status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

# Create the application instance.
app = Starlette(debug=True, routes=APP_ROUTES)

# Run the application if this script is executed directly.
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
