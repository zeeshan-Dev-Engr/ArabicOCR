from fastapi import APIRouter, UploadFile, File, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
import os
import shutil
import tempfile
from typing import List, Optional
import uuid
from pdf2image import convert_from_path
from pathlib import Path
import json

# Import utility functions
from app.utils.ocr_engines import process_with_qari, process_with_mistral
from app.utils.file_utils import validate_file, save_upload_file

# Create router
router = APIRouter()

# Temporary directory for file uploads
TEMP_DIR = Path("./temp")
TEMP_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    engine: str = Form("qari"),  # Options: qari, mistral, both
    background_tasks: BackgroundTasks = None,
):
    """Upload a file for OCR processing"""
    # Validate file type
    if not validate_file(file.filename):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF, PNG, JPG, and JPEG are allowed.")

    # Create a unique ID for this upload
    upload_id = str(uuid.uuid4())
    temp_folder = TEMP_DIR / upload_id
    temp_folder.mkdir(exist_ok=True)

    # Save the uploaded file
    file_path = await save_upload_file(file, temp_folder)
    
    # Process the file based on its type
    file_extension = os.path.splitext(file.filename)[1].lower()
    
    try:
        extracted_text = ""
        
        # Process PDF files
        if file_extension == ".pdf":
            # Convert PDF to images
            images = convert_from_path(file_path)
            
            # Save images temporarily
            image_paths = []
            for i, image in enumerate(images):
                img_path = temp_folder / f"page_{i+1}.png"
                image.save(img_path, "PNG")
                image_paths.append(img_path)
            
            # Process each image with the selected OCR engine
            page_texts = []
            for img_path in image_paths:
                if engine == "qari":
                    page_text = process_with_qari(str(img_path))
                elif engine == "mistral":
                    page_text = process_with_mistral(str(img_path))
                elif engine == "both":
                    qari_text = process_with_qari(str(img_path))
                    mistral_text = process_with_mistral(str(img_path))
                    page_text = f"Qari OCR:\n{qari_text}\n\nMistral OCR:\n{mistral_text}"
                else:
                    raise HTTPException(status_code=400, detail="Invalid OCR engine selection")
                
                page_texts.append(page_text)
            
            # Combine all page texts
            extracted_text = "\n\n--- Page Break ---\n\n".join(page_texts)
        
        # Process image files
        else:
            if engine == "qari":
                extracted_text = process_with_qari(str(file_path))
            elif engine == "mistral":
                extracted_text = process_with_mistral(str(file_path))
            elif engine == "both":
                qari_text = process_with_qari(str(file_path))
                mistral_text = process_with_mistral(str(file_path))
                extracted_text = f"Qari OCR:\n{qari_text}\n\nMistral OCR:\n{mistral_text}"
            else:
                raise HTTPException(status_code=400, detail="Invalid OCR engine selection")
        
        # Schedule cleanup of temporary files
        if background_tasks:
            background_tasks.add_task(lambda: shutil.rmtree(temp_folder, ignore_errors=True))
        
        return JSONResponse(
            content={
                "success": True,
                "text": extracted_text,
                "upload_id": upload_id,
            }
        )
    
    except Exception as e:
        # Clean up on error
        shutil.rmtree(temp_folder, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"OCR processing error: {str(e)}")