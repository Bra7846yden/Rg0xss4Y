# 代码生成时间: 2025-08-30 23:22:25
import os
import sys
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.exc import SQLAlchemyError

# 配置数据库连接字符串
DATABASE_URI = 'sqlite:///example.db'  # 替换为实际的数据库连接字符串

# 定义数据库迁移工具类
class DatabaseMigrationTool:
    def __init__(self, uri):
        self.engine = create_engine(uri)
        self.metadata = MetaData()

    def migrate(self, up=True):
        """执行数据库迁移

        Args:
            up (bool): 是否向上迁移
        """
        try:
            if up:
                self.metadata.reflect(bind=self.engine)
                tables = self.metadata.sorted_tables
                for table in tables:
                    table.create(self.engine)
            else:
                self.metadata.reflect(bind=self.engine)
                tables = self.metadata.sorted_tables
                for table in reversed(tables):
                    table.drop(self.engine)
        except SQLAlchemyError as e:
            raise Exception(f'数据库迁移失败: {e}')

    def get_migration_status(self):
        """获取数据库迁移状态"""
        try:
            self.metadata.reflect(bind=self.engine)
            return {'status': '数据库迁移成功', 'tables': [table.name for table in self.metadata.sorted_tables]}
        except SQLAlchemyError as e:
            return {'status': '数据库迁移失败', 'error': str(e)}

# 定义Starlette应用
app = Starlette(
    routes=[
        Route(' migrate', lambda request: JSONResponse({'message': '执行数据库迁移'})),
        Route(' status', lambda request: JSONResponse({'message': '获取数据库迁移状态'}
    ])
)

# 添加数据库迁移功能
@app.route('/migrate/{direction}', methods=['POST'])
async def migrate(request):
    direction = request.path_params['direction']
    tool = DatabaseMigrationTool(DATABASE_URI)
    try:
        if direction == 'up':
            tool.migrate(up=True)
            return JSONResponse({'status': '数据库向上迁移成功'})
        elif direction == 'down':
            tool.migrate(up=False)
            return JSONResponse({'status': '数据库向下迁移成功'})
        else:
            return JSONResponse({'status': '无效的迁移方向'}, status_code=400)
    except Exception as e:
        return JSONResponse({'status': '数据库迁移失败', 'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 添加获取数据库迁移状态功能
@app.route('/status', methods=['GET'])
async def get_status(request):
    tool = DatabaseMigrationTool(DATABASE_URI)
    try:
        status = tool.get_migration_status()
        return JSONResponse(status)
    except Exception as e:
        return JSONResponse({'status': '获取数据库迁移状态失败', 'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# 运行Starlette应用
if __name__ == '__main__':
    app.run(debug=True)
