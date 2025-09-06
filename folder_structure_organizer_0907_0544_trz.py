# 代码生成时间: 2025-09-07 05:44:08
import os
import shutil
from typing import List, Tuple
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

# 文件夹结构整理器配置类
class FolderStructureConfig:
    def __init__(self, root_dir: str, target_structure: List[Tuple[str, List[str]]]):
        self.root_dir = root_dir
        self.target_structure = target_structure

# 文件夹结构整理器类
class FolderStructureOrganizer:
    def __init__(self, config: FolderStructureConfig):
        self.config = config

    def organize(self) -> bool:
        """组织文件夹结构。"""
        try:
            for folder, subfolders in self.config.target_structure:
                full_path = os.path.join(self.config.root_dir, folder)
                os.makedirs(full_path, exist_ok=True)
                for subfolder in subfolders:
                    subfolder_path = os.path.join(full_path, subfolder)
                    os.makedirs(subfolder_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            return False

# Starlette路由处理类
class FolderStructureOrganizerApp(Starlette):
    def __init__(self):
        routes = [
            Route("/organize", FolderStructureOrganizerEndpoint, methods=["POST"]),
        ]
        super().__init__(routes=routes)

# Starlette端点类
class FolderStructureOrganizerEndpoint:
    async def post(self, request):
        """处理POST请求以组织文件夹结构。"""
        try:
            data = await request.json()
            root_dir = data.get("root_dir")
            target_structure = data.get("target_structure")
            if not root_dir or not target_structure:
                return JSONResponse(
                    content={"error": "Missing required data."}, status_code=HTTP_400_BAD_REQUEST
                )
            config = FolderStructureConfig(root_dir, target_structure)
            organizer = FolderStructureOrganizer(config)
            if organizer.organize():
                return JSONResponse(content={"message": "Folder structure organized successfully."}, status_code=HTTP_200_OK)
            else:
                return JSONResponse(
                    content={"error": "Failed to organize folder structure."}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
                )
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR
            )

# 程序入口点
if __name__ == "__main__":
    FolderStructureOrganizerApp().run(debug=True)