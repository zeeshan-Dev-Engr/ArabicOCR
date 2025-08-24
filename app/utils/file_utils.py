import os
import shutil
from fastapi import UploadFile
from pathlib import Path
from typing import List, Set

# Allowed file extensions
ALLOWED_EXTENSIONS = {".pdf", ".png", ".jpg", ".jpeg"}

# Maximum file size (10 MB)
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB in bytes


def validate_file(filename: str) -> bool:
    """Validate file extension"""
    if not filename:
        return False
    
    file_extension = os.path.splitext(filename)[1].lower()
    return file_extension in ALLOWED_EXTENSIONS


def validate_file_size(file_size: int) -> bool:
    """Validate file size"""
    return file_size <= MAX_FILE_SIZE


async def save_upload_file(upload_file: UploadFile, destination: Path) -> Path:
    """Save an uploaded file to the specified destination"""
    # Create destination directory if it doesn't exist
    destination.mkdir(parents=True, exist_ok=True)
    
    # Generate file path
    file_path = destination / upload_file.filename
    
    # Save the file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)
    
    return file_path


def clean_temp_files(file_paths: List[Path]):
    """Clean up temporary files"""
    for file_path in file_paths:
        if file_path.exists():
            if file_path.is_file():
                file_path.unlink()
            elif file_path.is_dir():
                shutil.rmtree(file_path)