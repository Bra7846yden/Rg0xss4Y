# 代码生成时间: 2025-08-04 23:02:43
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST
from typing import List


class FolderOrganizer:
    def __init__(self, root_path: str):
        "