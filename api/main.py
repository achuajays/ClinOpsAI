"""FastAPI application for ClinOps AI"""
import os
import logging
from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for maximum detail
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from src.workflow import ClinOpsAIWorkflow

logger.info("🏥 ClinOps AI FastAPI Application Starting...")

app = FastAPI(
    title="ClinOps AI",
    description="Autonomous Intelligence System for Medical Document Decisions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize workflow
workflow = None

def get_workflow():
    global workflow
    if workflow is None:
        logger.info("Initializing ClinOps AI Workflow instance...")
        try:
            workflow = ClinOpsAIWorkflow()
            logger.info("✓ Workflow initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize workflow: {e}", exc_info=True)
            raise
    return workflow


class TextAnalysisRequest(BaseModel):
    text: str


@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main UI"""
    html_path = Path(__file__).parent / "templates" / "index.html"
    with open(html_path, "r", encoding="utf-8") as f:
        return f.read()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ClinOps AI"}


@app.post("/api/analyze")
async def analyze_document(request: Request = None, file: UploadFile = File(None)):
    """
    Analyze a medical document
    Accepts either JSON with text field or file upload
    """
    logger.info("📥 Received analysis request")
    
    try:
        content_text = None
        
        # Try to get from JSON body
        if request:
            try:
                body = await request.json()
                if 'text' in body:
                    content_text = body['text']
                    logger.info(f"  Source: JSON body (length: {len(content_text)} chars)")
            except:
                pass
        
        # Try file upload
        if not content_text and file:
            logger.info(f"  Source: File upload ({file.filename})")
            content = await file.read()
            content_text = content.decode("utf-8")
            logger.info(f"  File content length: {len(content_text)} chars")
        
        if not content_text:
            logger.warning("  ❌ No text or file provided")
            raise HTTPException(status_code=400, detail="No text or file provided")
        
        # Run analysis
        logger.info("🔍 Starting document analysis...")
        wf = get_workflow()
        result = wf.analyze_document(content_text)
        
        logger.info("✅ Analysis completed successfully")
        return JSONResponse(content=result)
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Analysis failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
async def get_stats():
    """Get system statistics"""
    return {
        "total_analyzed": 0,
        "emergency_cases": 0,
        "high_priority": 0,
        "routine": 0,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
