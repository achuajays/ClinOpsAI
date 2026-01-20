"""Intake Agent - File handling and metadata extraction"""
from agno.agent import Agent
from pathlib import Path
import hashlib


def get_intake_agent() -> Agent:
    """Creates the Intake Agent for document handling"""
    return Agent(
        name="Intake Agent",
        role="Document intake specialist - validate and prepare medical documents",
        instructions=[
            "Accept medical documents in text or file format",
            "Extract basic metadata (document type, date if present)",
            "Perform deduplication checks using content hash",
            "Validate document completeness",
            "Pass clean document to next agent",
        ],

    )


def process_document_intake(content: str, filename: str = None) -> dict:
    """Process document intake without agent execution"""
    content_hash = hashlib.md5(content.encode()).hexdigest()
    
    # Basic document type detection
    doc_type = "unknown"
    if any(kw in content.lower() for kw in ["lab", "test result", "specimen"]):
        doc_type = "lab_report"
    elif any(kw in content.lower() for kw in ["referral", "refer to"]):
        doc_type = "referral"
    elif any(kw in content.lower() for kw in ["discharge", "summary"]):
        doc_type = "discharge_summary"
    elif any(kw in content.lower() for kw in ["consultation", "progress note"]):
        doc_type = "consultation"
    
    return {
        "content": content,
        "document_type": doc_type,
        "content_hash": content_hash,
        "filename": filename,
        "status": "validated"
    }
