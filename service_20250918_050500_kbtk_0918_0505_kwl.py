# 代码生成时间: 2025-09-18 05:05:00
import os\
import shutil\
from starlette.applications import Starlette\
from starlette.responses import JSONResponse\
from starlette.routing import Route, Mount\
from pathlib import Path\
\
# 定义一个文件夹结构整理器类\
class FolderOrganizer:\
    def __init__(self, source_folder, target_folder):\
        self.source_folder = Path(source_folder)\
        self.target_folder = Path(target_folder)\
        self.extensions = {'images': ['.jpg', '.jpeg', '.png', '.gif'], 'documents': ['.pdf', '.doc', '.docx', '.txt'], 'videos': ['.mp4', '.mov', '.avi'], 'audio': ['.mp3', '.wav', '.aac']}\
\
    def organize(self):\
        """整理文件夹"""\
        try:\
            # 确保源文件夹存在\
            self.source_folder.exists() or raise FileNotFoundError('源文件夹不存在')\
            # 确保目标文件夹存在\
            not self.target_folder.exists() and self.target_folder.mkdir(parents=True, exist_ok=True)\
            self._move_files()\
        except Exception as e:\
            return JSONResponse({'error': str(e)}, status_code=500)\
\
    def _move_files(self):\
        """移动文件到目标文件夹"""\
        for item in self.source_folder.iterdir():\
            if item.is_file():\
                self._move_file(item)\
            elif item.is_dir():\
                self._move_folder(item)\
\
    def _move_file(self, file):\
        """移动单个文件"