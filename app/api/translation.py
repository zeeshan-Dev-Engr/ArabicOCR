from fastapi import APIRouter, Body, HTTPException
from fastapi.responses import JSONResponse
import os
from typing import Dict, Optional
from dotenv import load_dotenv

# Import utility functions
from app.utils.translation import translate_text
from app.utils.transliteration import transliterate_text

# Load environment variables
load_dotenv()

# Create router
router = APIRouter()


@router.post("/translate")
async def translate(
    data: Dict[str, str] = Body(...),
):
    """Translate Arabic text to English or other languages"""
    try:
        # Get text and target language from request body
        text = data.get("text")
        target_language = data.get("target_language", "en")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Translate the text
        translated_text = translate_text(text, target_language)
        
        return JSONResponse(
            content={
                "success": True,
                "translated_text": translated_text,
                "source_language": "ar",
                "target_language": target_language,
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@router.post("/transliterate")
async def transliterate(
    data: Dict[str, str] = Body(...),
):
    """Transliterate Arabic text to Latin script"""
    try:
        # Get text from request body
        text = data.get("text")
        
        if not text:
            raise HTTPException(status_code=400, detail="Text is required")
        
        # Transliterate the text
        transliterated_text = transliterate_text(text)
        
        return JSONResponse(
            content={
                "success": True,
                "transliterated_text": transliterated_text,
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transliteration error: {str(e)}")