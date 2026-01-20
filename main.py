"""ClinOps AI - Entry point for running the application"""
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for maximum detail
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def main():
    """Main entry point - starts the FastAPI server"""
    logger.info("=" * 60)
    logger.info("🏥 ClinOps AI - Medical Document Intelligence")
    logger.info("=" * 60)
    logger.info("\n🚀 Starting FastAPI server...\n")
    
    # Import uvicorn
    try:
        import uvicorn
    except ImportError:
        logger.error("❌ uvicorn not installed. Run: uv pip install uvicorn")
        sys.exit(1)
    
    # Run the server
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=["api", "src"],
        log_level="info"
    )


if __name__ == "__main__":
    main()
