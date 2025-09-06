# 代码生成时间: 2025-09-07 00:32:44
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import shutil
import os
import logging
from datetime import datetime


# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据备份和恢复服务
class BackupRestoreService:
    def __init__(self, backup_dir):
        self.backup_dir = backup_dir

    def backup_data(self, source_dir):
        """备份数据到指定目录。

        :param source_dir: 需要备份的数据目录
        :return: 备份结果
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            backup_path = os.path.join(self.backup_dir, f"backup_{timestamp}.zip")
            shutil.make_archive(backup_path, 'zip', source_dir)
            return {"message": "Backup successful", "backup_path": backup_path}
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return {"message": "Backup failed", "error": str(e)}

    def restore_data(self, backup_file_path, target_dir):
        """从备份文件恢复数据。

        :param backup_file_path: 备份文件的路径
        :param target_dir: 恢复的目标目录
        :return: 恢复结果
        """
        try:
            shutil.unpack_archive(backup_file_path, target_dir)
            return {"message": "Restore successful"}
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return {"message": "Restore failed", "error": str(e)}

# 创建API端点
def backup_endpoint(request):
    source_dir = request.query_params.get("source_dir")
    if not source_dir:
        return JSONResponse(
            content={"message": "Missing source directory"}, status_code=HTTP_400_BAD_REQUEST
        )
    service = BackupRestoreService("./backups")
    result = service.backup_data(source_dir)
    return JSONResponse(content=result, status_code=HTTP_200_OK)

def restore_endpoint(request):
    backup_file_path = request.query_params.get("backup_file_path")
    target_dir = request.query_params.get("target_dir")
    if not backup_file_path or not target_dir:
        return JSONResponse(
            content={"message": "Missing backup file path or target directory"}, status_code=HTTP_400_BAD_REQUEST
        )
    service = BackupRestoreService("./backups")
    result = service.restore_data(backup_file_path, target_dir)
    return JSONResponse(content=result, status_code=HTTP_200_OK)

# 创建Starlette应用
app = Starlette(routes=[
    Route("/backup", endpoint=backup_endpoint),
    Route("/restore", endpoint=restore_endpoint),
])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)