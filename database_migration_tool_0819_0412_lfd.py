# 代码生成时间: 2025-08-19 04:12:39
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
import asyncio
import uvicorn
from alembic.config import Config
from alembic import command
import os


# 数据库迁移配置类
class DatabaseMigrationTool:
    def __init__(self, alembic_config_path):
        self.alembic_config_path = alembic_config_path

    def migrate_up(self):
        """执行数据库升级迁移"""
        alembic_cfg = Config(self.alembic_config_path)
        command.upgrade(alembic_cfg, 'head')

    def migrate_down(self, revision):
        """执行数据库降级迁移"""
        alembic_cfg = Config(self.alembic_config_path)
        command.downgrade(alembic_cfg, revision)


# Starlette路由和错误处理
async def migrate_up_route(request):
    """处理数据库升级迁移请求"""
    try:
        migration_tool = DatabaseMigrationTool(config_path='alembic.ini')
        migration_tool.migrate_up()
        return JSONResponse({'message': 'Database migrated successfully!'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def migrate_down_route(request, revision):
    """处理数据库降级迁移请求"""
    try:
        migration_tool = DatabaseMigrationTool(config_path='alembic.ini')
        migration_tool.migrate_down(revision)
        return JSONResponse({'message': 'Database downgraded successfully!'})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# 创建Starlette应用
app = Starlette(
    routes=[
        Route('/api/migrate/up', migrate_up_route),
        Route('/api/migrate/down/{revision}', migrate_down_route),
    ],
)


# 运行应用
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
