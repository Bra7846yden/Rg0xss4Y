# 代码生成时间: 2025-09-17 16:02:31
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import uvicorn
from alembic.config import Config as AlembicConfig
from alembic import command
from alembic.util import CommandError

# 数据库迁移工具的配置类
class DatabaseMigrationTool:
    def __init__(self, alembic_config_file):
        self.alembic_config = AlembicConfig(alembic_config_file)

    # 执行数据库迁移
    def migrate(self):
        try:
            command.upgrade(self.alembic_config, 'head')
        except CommandError as e:
            raise Exception(f"Migration failed: {e}")

# REST API 端点
async def migrate_endpoint(request):
    tool = DatabaseMigrationTool('alembic.ini')
    try:
        tool.migrate()
        return JSONResponse({'message': 'Migration successful'}, status_code=200)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 创建Starlette应用
app = Starlette(
    routes=[
        Route('/migrate', migrate_endpoint, methods=['POST']),
    ],
    debug=True
)

# 启动服务器
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
