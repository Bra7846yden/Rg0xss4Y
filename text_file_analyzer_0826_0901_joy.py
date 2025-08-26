# 代码生成时间: 2025-08-26 09:01:01
# text_file_analyzer.py

"""
A simple text file analyzer built using Starlette framework.
This application reads a text file, analyzes its content,
and provides statistics such as word count, line count, and character count.
"""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
import os
import re
from collections import Counter
import mimetypes

# Define the supported text file types
SUPPORTED_MIME_TYPES = ['text/plain', 'text/markdown', 'text/html', 'application/xml']

# Define the maximum file size allowed
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

class TextFileAnalyzer:
    def __init__(self):
        self.word_count = 0
        self.line_count = 0
        self.char_count = 0

    def analyze(self, file_content):
        """Analyze the content of the text file."""
        self.word_count = len(re.findall(r'\w+', file_content))
        self.line_count = len(file_content.splitlines())
        self.char_count = len(file_content)
        return {
            'word_count': self.word_count,
            'line_count': self.line_count,
            'char_count': self.char_count
        }

async def analyze_text_file(request):
    """
    Endpoint to analyze the content of a text file sent via a POST request.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        JSONResponse: A JSON response containing the analysis results.
    """
    try:
        file = await request.form()
        text_file = file.get('file')

        # Check if a file was provided
        if not text_file:
            raise HTTPException(status_code=400, detail="No file provided.")

        # Get the file content and its MIME type
        file_content = await text_file.read()
        file_mime_type, _ = mimetypes.guess_type(text_file.filename)

        # Check if the file is a supported text file type
        if file_mime_type not in SUPPORTED_MIME_TYPES:
            raise HTTPException(status_code=400, detail="Unsupported file type.")

        # Check if the file size exceeds the maximum allowed size
        if len(file_content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File size exceeds the maximum allowed size.")

        # Analyze the file content
        analyzer = TextFileAnalyzer()
        results = analyzer.analyze(file_content.decode('utf-8'))

        return JSONResponse(results)
    except Exception as e:
        # Handle any unexpected exceptions
        return JSONResponse({'error': str(e)}, status_code=500)

# Define the routes for the application
routes = [
    Route('/api/analyze', endpoint=analyze_text_file, methods=['POST'])
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)
