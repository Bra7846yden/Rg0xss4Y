# 代码生成时间: 2025-08-03 17:29:46
import os
from PIL import Image
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from typing import List, Dict


class ImageResizer:
    """批量调整图片尺寸的类。"""

    def __init__(self, output_folder: str):
        self.output_folder = output_folder

    def resize_images(self, image_paths: List[str], size: tuple) -> List[Dict[str, str]]:
        """批量调整图片尺寸。

        Args:
        image_paths (List[str]): 需要调整尺寸的图片路径列表。
        size (tuple): 目标尺寸（宽度，高度）。

        Returns:
        List[Dict[str, str]]: 包含每张图片原始路径和调整尺寸后的路径的列表。
        """
        resized_images = []
        for image_path in image_paths:
            try:
                with Image.open(image_path) as img:
                    img = img.resize(size, Image.ANTIALIAS)
                    output_path = os.path.join(self.output_folder, os.path.basename(image_path))
                    img.save(output_path)
                    resized_images.append({'original': image_path, 'resized': output_path})
            except Exception as e:
                resized_images.append({'original': image_path, 'error': str(e)})
        return resized_images


async def resize_endpoint(request):
    """处理图片尺寸调整请求的端点。"""
    data = await request.json()
    image_paths = data.get('image_paths', [])
    size = data.get('size', (0, 0))
    resizer = ImageResizer('resized_images')
    resized_images = resizer.resize_images(image_paths, size)
    return JSONResponse({'resized_images': resized_images})


routes = [
    Route('/', resize_endpoint),
]

app = Starlette(debug=True, routes=routes)

# Example usage of the ImageResizer class outside of a Starlette application:
if __name__ == '__main__':
    original_images = ['path/to/image1.jpg', 'path/to/image2.jpg']
    resizer = ImageResizer('resized_images')
    results = resizer.resize_images(original_images, (800, 600))
    print(results)