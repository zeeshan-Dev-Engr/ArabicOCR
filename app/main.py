import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Import API routers
from app.api.ocr import router as ocr_router
from app.api.translation import router as translation_router
from app.api.export import router as export_router

# Create FastAPI app
app = FastAPI(title="ArabicOCR", description="Arabic OCR Web Application")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up templates
templates = Jinja2Templates(directory="app/templates")

# Include API routers
app.include_router(ocr_router, prefix="/api/ocr", tags=["OCR"])
app.include_router(translation_router, prefix="/api/translation", tags=["Translation"])
app.include_router(export_router, prefix="/api/export", tags=["Export"])


@app.get("/")
async def index(request: Request):
    """Render the main application page"""
    return templates.TemplateResponse("index.html", {"request": request})


if __name__ == "__main__":
    import uvicorn

    # Get port from environment variable or use default
    port = int(os.environ.get("PORT", 8000))
    
    # Run the application
    uvicorn.run("app.main:app", host="0.0.0.0", port=port, reload=True)