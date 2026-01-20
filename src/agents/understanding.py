"""Understanding Agent - Medical entity extraction"""
from agno.agent import Agent
from agno.models.groq import Groq


def get_understanding_agent() -> Agent:
    """Creates the Medical Understanding Agent"""
    return Agent(
        name="Medical Understanding Agent",
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        role="Medical NLP specialist - extract clinical entities from documents",
        instructions=[
            "Extract all symptoms mentioned in the document",
            "Identify all lab tests and their values",
            "Extract diagnoses and medical conditions",
            "Identify medications if present",
            "Extract patient and doctor information",
            "Understand clinical context, not just keywords",
            "Return structured entities in JSON format",
        ],

    )
