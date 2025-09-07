# 代码生成时间: 2025-09-07 16:15:46
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Router
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from starlette.requests import Request
# 改进用户体验
from starlette.exceptions import ExceptionMiddleware

# 数据备份恢复服务
class DataBackupRestoreService:
    def __init__(self, backup_dir):
        """
        数据备份恢复服务初始化
        :param backup_dir: 备份文件存放目录
# FIXME: 处理边界情况
        """
        self.backup_dir = backup_dir

    def backup_data(self, source_dir):
        """
# FIXME: 处理边界情况
        备份数据
        :param source_dir: 数据源目录
        """
        try:
            shutil.copytree(source_dir, os.path.join(self.backup_dir, os.path.basename(source_dir)))
            return True, "Backup successful"
        except Exception as e:
            return False, str(e)

    def restore_data(self, backup_name, destination_dir):
# 扩展功能模块
        """
        恢复数据
# 改进用户体验
        :param backup_name: 备份文件名称
        :param destination_dir: 目标恢复目录
        """
# 添加错误处理
        try:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
            shutil.copytree(os.path.join(self.backup_dir, backup_name), destination_dir, dirs_exist_ok=True)
            return True, "Restore successful"
        except Exception as e:
            return False, str(e)

# API路由
# NOTE: 重要实现细节
def create_router():
    router = Router()
# TODO: 优化性能

    # 数据备份接口
    @router.add_route("/backup", methods=["POST"])
    async def backup(request: Request):
        backup_dir = request.json().get("backupDir")
        source_dir = request.json().get("sourceDir")
        if not backup_dir or not source_dir:
            return JSONResponse({"error": "Missing backupDir or sourceDir"}, status_code=HTTP_400_BAD_REQUEST)
# TODO: 优化性能

        service = DataBackupRestoreService(backup_dir)
        success, message = service.backup_data(source_dir)
        if success:
            return JSONResponse({"message": message}, status_code=HTTP_200_OK)
# TODO: 优化性能
        else:
            return JSONResponse({"error": message}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    # 数据恢复接口
    @router.add_route("/restore", methods=["POST"])
    async def restore(request: Request):
        backup_dir = request.json().get("backupDir\)
        backup_name = request.json().get("backupName")
        destination_dir = request.json().get("destinationDir\)
        if not backup_dir or not backup_name or not destination_dir:
# 添加错误处理
            return JSONResponse({"error": "Missing backupDir, backupName or destinationDir"}, status_code=HTTP_400_BAD_REQUEST)

        service = DataBackupRestoreService(backup_dir)
        success, message = service.restore_data(backup_name, destination_dir)
        if success:
# 添加错误处理
            return JSONResponse({"message": message}, status_code=HTTP_200_OK)
        else:
            return JSONResponse({"error": message}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

    return router

# 创建Starlette应用
# 优化算法效率
app = Starlette(middleware=[ExceptionMiddleware()], routes=create_router().routes)
