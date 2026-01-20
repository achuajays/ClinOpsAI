"""Urgency Agent - Clinical risk assessment"""
from agno.agent import Agent
from agno.models.groq import Groq


def get_urgency_agent() -> Agent:
    """Creates the Clinical Urgency Assessment Agent"""
    return Agent(
        name="Clinical Urgency Agent",
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        role="Clinical risk assessor - determine urgency level of medical findings",
        instructions=[
            "Analyze medical findings for urgency indicators",
            "Consider lab value thresholds (e.g., elevated Troponin = cardiac risk)",
            "Assess symptom severity and temporal changes",
            "Evaluate document language intensity (e.g., 'STAT', 'urgent', 'critical')",
            "Classify urgency as: Emergency, High Priority, Routine, or Informational",
            "Use clinical reasoning, not just rule-based logic",
            "Explain your urgency assessment clearly",
        ],

    )
