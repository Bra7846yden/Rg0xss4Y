# 代码生成时间: 2025-08-26 20:09:48
import os
from PIL import Image
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from typing import List, Dict
import shutil
import tempfile

"""
An image resizing application using Starlette framework.
"""

class ImageResizerApp(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route('/', self.index),
                Route('/resize', self.resize_image),
            ],
            middleware=[
            ],
            debug=True,
        )

    async def index(self, request):
        """
        The index page that renders the form for uploading images.
        """
        return FileResponse('index.html')

    async def resize_image(self, request):
        """
        Handles the resizing of images.
        """
        try:
            # Extract the uploaded file from the request
            file = await request.form()
            image_file = file.get('file')

            # Ensure the file is an image
            if not image_file:
                return JSONResponse({'error': 'No image uploaded'}, status_code=400)

            # Save the uploaded image to a temporary directory
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(image_file.file.read())
                tmp_file.flush()

                # Open the image and resize it
                with Image.open(tmp_file.name) as img:
                    target_size = (800, 600)  # Target size
                    resized_img = img.resize(target_size, Image.ANTIALIAS)

                    # Save the resized image to the specified directory
                    resized_img.save('resized_image.jpg')

            return JSONResponse({'message': 'Image resized successfully', 'resized_image_url': '/static/resized_image.jpg'})
        except Exception as e:
            return JSONResponse({'error': str(e)}, status_code=500)

# Assume index.html is a static HTML file that contains the form for uploading images

if __name__ == '__main__':
    app = ImageResizerApp()
    app.mount('/static', StaticFiles(directory='static'))
    app.run()
