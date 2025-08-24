from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import FileResponse
import os
import tempfile
from typing import Dict, Optional
import uuid
from pathlib import Path

# Import utility functions
from app.utils.document_export import create_docx

# Create router
router = APIRouter()

# Temporary directory for file exports
TEMP_DIR = Path("./temp")
TEMP_DIR.mkdir(exist_ok=True)


@router.post("/docx")
async def export_docx(
    data: Dict[str, str] = Body(...),
):
    """Export Arabic text, translation, and transliteration to a DOCX file"""
    try:
        # Get text, translation, and transliteration from request body
        arabic_text = data.get("arabic_text")
        translated_text = data.get("translated_text", "")
        transliterated_text = data.get("transliterated_text", "")
        
        if not arabic_text:
            raise HTTPException(status_code=400, detail="Arabic text is required")
        
        # Create a unique filename
        filename = f"arabic_ocr_{uuid.uuid4()}.docx"
        output_path = TEMP_DIR / filename
        
        # Create the DOCX file
        create_docx(
            str(output_path),
            arabic_text,
            translated_text,
            transliterated_text
        )
        
        # Return the file as a download
        return FileResponse(
            path=str(output_path),
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document export error: {str(e)}")