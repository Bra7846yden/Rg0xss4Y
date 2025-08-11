# 代码生成时间: 2025-08-11 17:29:12
import os
import logging
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BatchFileRenamer:
    def __init__(self, directory, rename_pattern):
        self.directory = directory
        self.rename_pattern = rename_pattern

    def rename_files(self):
        """批量重命名文件夹内的文件，按照指定的模式。"""
        try:
            for filename in os.listdir(self.directory):
                file_path = os.path.join(self.directory, filename)
                if os.path.isfile(file_path):
                    new_filename = self.rename_pattern.format(filename)
                    new_file_path = os.path.join(self.directory, new_filename)
                    os.rename(file_path, new_file_path)
                    logger.info(f'Renamed {filename} to {new_filename}')
        except Exception as e:
            logger.error(f'Error renaming files: {e}')
            raise

# Starlette 应用配置
app = Starlette()
templates = Jinja2Templates(directory='templates')

# 路由配置
app.add_route('/index', templates.TemplateResponse('index.html', {'request': request}))
app.add_route('/upload', templates.TemplateResponse('upload.html', {'request': request}))
app.mount('/static', StaticFiles(directory='static'), name='static')

# 中间件配置
app.add_middleware(SessionMiddleware, secret_key='your_secret_key')

# 文件重命名工具接口
@app.route('/rename', methods=['POST'])
async def rename(request):
    """处理文件重命名请求。"""
    directory = request.form['directory']
    rename_pattern = request.form['rename_pattern']
    batch_renamer = BatchFileRenamer(directory, rename_pattern)
    try:
        batch_renamer.rename_files()
        return {
            'status': 'success',
            'message': 'Files renamed successfully.'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

if __name__ == '__main__':
    """启动 Starlette 应用。"""
    app.run(host='0.0.0.0', port=8000)