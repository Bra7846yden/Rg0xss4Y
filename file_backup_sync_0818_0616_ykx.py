# 代码生成时间: 2025-08-18 06:16:39
import os
import shutil
import logging
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import asyncio

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FileBackupSync:
    """文件备份和同步工具类"""
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.backup_folder = os.path.join(self.destination, "backup")

    def ensure_directory_exists(self):
        """确保备份目录存在"""
        if not os.path.exists(self.backup_folder):
            os.makedirs(self.backup_folder)

    def backup_files(self):
        """备份源目录中的文件"""
        self.ensure_directory_exists()
        for filename in os.listdir(self.source):
            src_path = os.path.join(self.source, filename)
            dst_path = os.path.join(self.backup_folder, filename)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
                logger.info(f"Backup {filename} successfully")

    def sync_files(self):
        """同步源目录和目标目录的文件"""
        for filename in os.listdir(self.source):
            src_path = os.path.join(self.source, filename)
            dst_path = os.path.join(self.destination, filename)
            if os.path.isfile(src_path):
                shutil.copy2(src_path, dst_path)
                logger.info(f"Sync {filename} successfully")

    def remove_orphaned_files(self):
        """移除目标目录中不再存在的文件"""
        for filename in os.listdir(self.destination):
            src_path = os.path.join(self.source, filename)
            if not os.path.exists(src_path):
                dst_path = os.path.join(self.destination, filename)
                os.remove(dst_path)
                logger.info(f"Removed orphaned file {filename}")

    async def handle_backup_sync(self, request):
        """处理备份和同步请求"""
        try:
            self.backup_files()
            self.sync_files()
            self.remove_orphaned_files()
            return JSONResponse(
                content={"message": "Backup and sync completed successfully"},
                status_code=HTTP_200_OK,
            )
        except Exception as e:
            logger.error(f"Error during backup and sync: {e}")
            return JSONResponse(
                content={"error": str(e)},
                status_code=HTTP_400_BAD_REQUEST,
            )

async def main():
    source_directory = "/path/to/source"
    destination_directory = "/path/to/destination"
    file_backup_sync = FileBackupSync(source_directory, destination_directory)

    app = Starlette(
        routes=[
            Route("/backup-sync", endpoint=file_backup_sync.handle_backup_sync, methods=["POST"]),
        ],
    )
    await app.startup()
    logger.info("File backup and sync service started")
    await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())