# 代码生成时间: 2025-09-08 11:35:36
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import shutil


class BatchRenameTool:
    """批量文件重命名工具类"""
    def __init__(self, directory):
        self.directory = directory

    def rename_files(self, new_names, extensions=None):
        """根据新的文件名列表批量重命名文件

        :param new_names: 新文件名列表
        :param extensions: 要重命名的文件扩展名列表
        :return: 重命名结果
        """
        if extensions is None:
            extensions = []

        try:
            for i, filename in enumerate(os.listdir(self.directory)):
                file_path = os.path.join(self.directory, filename)
                if os.path.isfile(file_path) and (not extensions or any(filename.endswith(ext) for ext in extensions)):
                    # 如果没有指定新的文件名，则保持原文件名不变
                    new_filename = new_names[i] if i < len(new_names) else filename
                    new_file_path = os.path.join(self.directory, new_filename)
                    shutil.move(file_path, new_file_path)
            return {'status': 'success', 'message': 'Files renamed successfully'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}


def rename_files_endpoint(request):
    """重命名文件的API端点"""
    data = request.json()
    directory = data.get('directory')
    new_names = data.get('new_names')
    extensions = data.get('extensions', [])

    if not directory or not new_names:
        return JSONResponse({'status': 'error', 'message': 'Missing required parameters'}, status_code=HTTP_400_BAD_REQUEST)

    try:
        tool = BatchRenameTool(directory)
        result = tool.rename_files(new_names, extensions)
        return JSONResponse(result, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({'status': 'error', 'message': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


# 创建Starlette应用
app = Starlette(routes=[
    Route('/rename', rename_files_endpoint)
])


if __name__ == '__main__':
    # 使用Uvicorn作为ASGI服务器运行应用
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)