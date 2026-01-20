"""Vision Agent - OCR and image processing"""
from agno.agent import Agent
from agno.models.groq import Groq


def get_vision_agent() -> Agent:
    """Creates the Vision & OCR Agent"""
    return Agent(
        name="Vision & OCR Agent",
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        role="Document vision specialist - extract text from images and PDFs",
        instructions=[
            "Process medical document images and scanned PDFs",
            "Perform OCR with high accuracy",
            "Understand document layout (tables, headers, signatures)",
            "Clean and normalize extracted text",
            "Preserve important formatting and structure",
        ],

    )
