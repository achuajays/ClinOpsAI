"""Decision Agent - Action routing logic"""
from agno.agent import Agent
from agno.models.groq import Groq


def get_decision_agent() -> Agent:
    """Creates the Decision & Routing Agent"""
    return Agent(
        name="Decision & Routing Agent",
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        role="Clinical coordinator - decide actions based on urgency and findings",
        instructions=[
            "Based on urgency level, decide the appropriate action:",
            "- Emergency: Notify doctor immediately via urgent alert",
            "- High Priority: Create high-priority task in EMR, schedule callback",
            "- Routine: Schedule standard follow-up appointment",
            "- Informational: Store in patient record for reference",
            "Determine who should be notified (attending physician, specialist, etc.)",
            "Specify timing and communication channel",
            "Provide clear action plan",
        ],

    )
