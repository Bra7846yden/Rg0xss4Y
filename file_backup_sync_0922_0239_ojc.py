# 代码生成时间: 2025-09-22 02:39:41
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

# Define constants
BACKUP_SOURCE_DIR = "/source/directory"
BACKUP_DEST_DIR = "/destination/directory"

class FileBackupSync:
    """Class responsible for file backup and synchronization."""
    def __init__(self, source_dir, dest_dir):
        self.source_dir = source_dir
        self.dest_dir = dest_dir

    def backup_files(self):
        """Backup files from source directory to destination directory."""
        try:
            # Check if source directory exists
            if not os.path.exists(self.source_dir):
                raise FileNotFoundError("Source directory does not exist.")
            
            # Check if destination directory exists, if not create it
            os.makedirs(self.dest_dir, exist_ok=True)

            # Walk through the source directory
            for root, dirs, files in os.walk(self.source_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, self.source_dir)
                    dest_file_path = os.path.join(self.dest_dir, rel_path)
                    
                    # Create intermediate directories if they don't exist
                    os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                    
                    # Copy file from source to destination
                    shutil.copy2(file_path, dest_file_path)

            return True
        except Exception as e:
            return str(e)

    def sync_files(self):
        """Synchronize files between source and destination directories."""
        try:
            # Check if both directories exist
            if not os.path.exists(self.source_dir) or not os.path.exists(self.dest_dir):
                raise FileNotFoundError("Both source and destination directories must exist.")
            
            # Get lists of files in both directories
            source_files = set(os.listdir(self.source_dir))
            dest_files = set(os.listdir(self.dest_dir))

            # Find files to add and remove
            files_to_add = source_files - dest_files
            files_to_remove = dest_files - source_files

            # Add new files
            for file in files_to_add:
                file_path = os.path.join(self.source_dir, file)
                dest_file_path = os.path.join(self.dest_dir, file)
                shutil.copy2(file_path, dest_file_path)

            # Remove missing files
            for file in files_to_remove:
                file_path = os.path.join(self.dest_dir, file)
                os.remove(file_path)

            return True
        except Exception as e:
            return str(e)

# Create an instance of FileBackupSync
file_backup_sync = FileBackupSync(BACKUP_SOURCE_DIR, BACKUP_DEST_DIR)

# Define the Starlette application
app = Starlette(debug=True)

# Define routes
@app.route("/backup", methods=["POST"])
async def backup(request):
    """Endpoint to trigger file backup."""
    result = file_backup_sync.backup_files()
    if isinstance(result, bool):
        return JSONResponse({'message': 'Backup successful'}, status_code=HTTP_200_OK)
    else:
        return JSONResponse({'error': result}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

@app.route("/sync", methods=["POST"])
async def sync(request):
    """Endpoint to trigger file synchronization."""
    result = file_backup_sync.sync_files()
    if isinstance(result, bool):
        return JSONResponse({'message': 'Sync successful'}, status_code=HTTP_200_OK)
    else:
        return JSONResponse({'error': result}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

@app.exception_handler(FileNotFoundError)
async def file_not_found_exception(request, exc):
    """Handle file not found exceptions."""
    return JSONResponse({'error': str(exc)}, status_code=HTTP_400_BAD_REQUEST)
