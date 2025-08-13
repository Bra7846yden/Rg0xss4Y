# 代码生成时间: 2025-08-14 07:02:05
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import json

# Define the directory where backups will be stored
BACKUP_DIRECTORY = 'backups/'

class BackupRestoreService:
    def __init__(self, backup_dir=BACKUP_DIRECTORY):
        self.backup_dir = backup_dir
        # Ensure the backup directory exists
        os.makedirs(self.backup_dir, exist_ok=True)

    def create_backup(self, source_path):
        """Creates a backup of the specified source path."""
        try:
            backup_path = os.path.join(self.backup_dir, os.path.basename(source_path) + '_backup')
            shutil.copytree(source_path, backup_path)
            return True, backup_path
        except Exception as e:
            return False, str(e)

    def restore_backup(self, backup_path, destination_path):
        """Restores a backup to the specified destination path."""
        try:
            shutil.copytree(backup_path, destination_path)
            return True, "Backup restored successfully."
        except Exception as e:
            return False, str(e)

# Define the API routes
def backup(request):
    """API endpoint to create a backup."""
    source_path = request.query_params.get('source')
    if not source_path:
        return JSONResponse({'error': 'Source path is required.'}, status_code=HTTP_400_BAD_REQUEST)
    service = BackupRestoreService()
    success, message = service.create_backup(source_path)
    if success:
        return JSONResponse({'message': message}, status_code=HTTP_200_OK)
    else:
        return JSONResponse({'error': message}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

def restore(request):
    """API endpoint to restore a backup."""
    backup_path = request.query_params.get('backup')
    destination_path = request.query_params.get('destination')
    if not backup_path or not destination_path:
        return JSONResponse({'error': 'Backup and destination paths are required.'}, status_code=HTTP_400_BAD_REQUEST)
    service = BackupRestoreService()
    success, message = service.restore_backup(backup_path, destination_path)
    if success:
        return JSONResponse({'message': message}, status_code=HTTP_200_OK)
    else:
        return JSONResponse({'error': message}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# Create the Starlette application with the defined routes
app = Starlette(
    routes=[
        Route('/create-backup', endpoint=backup, methods=['GET']),
        Route('/restore-backup', endpoint=restore, methods=['GET'])
    ]
)

# If run as a script, start the server
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)