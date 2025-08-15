# 代码生成时间: 2025-08-15 12:02:44
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
from starlette.routing import Route
import shutil
import os
import tarfile
import tempfile
import json

# Global variables for backup and restore
BACKUP_DIR = 'backups/'
BACKUP_FILE = 'backup.tar.gz'

class DataBackupAndRestore:
    def __init__(self, backup_dir=BACKUP_DIR, backup_file=BACKUP_FILE):
        self.backup_dir = backup_dir
        self.backup_file = backup_file

    def create_backup(self, source_dir):
        """Create a backup of the specified directory."""
        try:
            # Create temporary directory
            with tempfile.TemporaryDirectory() as tmp_dir:
                # Create tarball in temporary directory
                tar_name = os.path.join(tmp_dir, self.backup_file)
                with tarfile.open(tar_name, 'w:gz') as tar:
                    for root, dirs, files in os.walk(source_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, source_dir)
                            tar.add(file_path, arcname)

                # Move tarball to backup directory
                shutil.move(tar_name, os.path.join(self.backup_dir, self.backup_file))
                return {
                    'status': 'success',
                    'message': 'Backup created successfully.'
                }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

    def restore_backup(self, backup_file_path):
        """Restore the backup to the original directory."""
        try:
            # Extract tarball to original directory
            with tarfile.open(backup_file_path, 'r:gz') as tar:
                tar.extractall(self.backup_dir)
            return {
                'status': 'success',
                'message': 'Backup restored successfully.'
            }
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e)
            }

# Create Starlette application
app = Starlette(debug=True)

# Define routes for backup and restore
app.add_route('/backup', lambda request: JSONResponse(
    DataBackupAndRestore().create_backup('data/')))
app.add_route('/restore', lambda request: JSONResponse(
    DataBackupAndRestore().restore_backup(BACKUP_DIR + BACKUP_FILE)))

# Run the application
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)