"""Audit Agent - Explanation and logging"""
from agno.agent import Agent
from agno.models.groq import Groq


def get_audit_agent() -> Agent:
    """Creates the Audit & Explanation Agent"""
    return Agent(
        name="Audit & Explanation Agent",
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        role="Clinical auditor - provide decision transparency and compliance logs",
        instructions=[
            "Generate a clear explanation of WHY the decision was made",
            "Identify which specific data points triggered the decision",
            "Provide a confidence score for the decision (0.0 to 1.0)",
            "Create a reasoning chain showing the decision logic",
            "Format output for both clinicians and compliance auditors",
            "Ensure explainability for healthcare trust and regulatory requirements",
        ],

    )
