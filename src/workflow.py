"""ClinOps AI - Medical Document Intelligence Workflow"""
import os
import json
import logging
from dotenv import load_dotenv
from agno.team import Team
from agno.models.groq import Groq

from src.agents.intake import get_intake_agent, process_document_intake
from src.agents.understanding import get_understanding_agent
from src.agents.urgency import get_urgency_agent
from src.agents.decision import get_decision_agent
from src.agents.audit import get_audit_agent
from src.models.schemas import MedicalEntities, UrgencyLevel, DecisionOutput, AuditTrace, AnalysisResponse

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Changed to DEBUG for maximum detail
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClinOpsAIWorkflow:
    """Orchestrates the medical document analysis workflow"""
    
    def __init__(self):
        logger.info("🚀 Initializing ClinOps AI Workflow...")
        
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        if not self.groq_api_key:
            logger.error("❌ GROQ_API_KEY not found in environment variables")
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        logger.info("✓ GROQ_API_KEY found")
        
        # Initialize agents
        logger.info("📦 Creating agents...")
        try:
            self.understanding_agent = get_understanding_agent()
            logger.info("  ✓ Understanding Agent created")
            
            self.urgency_agent = get_urgency_agent()
            logger.info("  ✓ Urgency Agent created")
            
            self.decision_agent = get_decision_agent()
            logger.info("  ✓ Decision Agent created")
            
            self.audit_agent = get_audit_agent()
            logger.info("  ✓ Audit Agent created")
        except Exception as e:
            logger.error(f"❌ Error creating agents: {e}", exc_info=True)
            raise
        
        # Create medical team
        logger.info("👥 Creating Medical Intelligence Team...")
        try:
            self.team = Team(
                name="ClinOps Medical Intelligence Team",
                model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
                members=[
                    self.understanding_agent,
                    self.urgency_agent,
                    self.decision_agent,
                    self.audit_agent,
                ],
                instructions=[
                    "You are the team leader coordinating medical document analysis",
                    "First, delegate to Understanding Agent to extract medical entities",
                    "Then, delegate to Urgency Agent to assess clinical urgency",
                    "Next, delegate to Decision Agent to determine actions",
                    "Finally, delegate to Audit Agent to generate explanation",
                    "Compile all results into a comprehensive analysis"
                ],
            )
            logger.info("✓ Medical Intelligence Team created successfully")
        except Exception as e:
            logger.error(f"❌ Error creating team: {e}", exc_info=True)
            raise
    
    def analyze_document(self, text: str) -> dict:
        """Analyze a medical document and return decision intelligence"""
        logger.info("=" * 60)
        logger.info("🏥 Starting Medical Document Analysis")
        logger.info("=" * 60)
        
        # Step 1: Intake processing
        logger.info("📄 Step 1: Document Intake Processing...")
        logger.debug(f"  Input text preview (first 200 chars): {text[:200]}...")
        try:
            intake_result = process_document_intake(text)
            logger.info(f"  ✓ Document Type: {intake_result['document_type']}")
            logger.info(f"  ✓ Content Hash: {intake_result['content_hash'][:16]}...")
            logger.info(f"  ✓ Status: {intake_result['status']}")
            logger.debug(f"  Full intake result: {intake_result}")
        except Exception as e:
            logger.error(f"  ❌ Intake processing failed: {e}", exc_info=True)
            raise
        
        # Step 2: Run AI analysis using Understanding Agent directly
        logger.info("🧠 Step 2: Running AI Analysis...")
        
        # Create a comprehensive prompt
        prompt = f"""You are a medical document analysis AI. Analyze this medical document and provide a comprehensive analysis in PLAIN TEXT MARKDOWN format (NOT JSON).

**Document Type:** {intake_result['document_type']}

**Document Content:**
{intake_result['content']}

**Your Task:**
Provide a detailed medical analysis in PLAIN MARKDOWN TEXT with the following sections:

# Clinical Urgency Level
Start with one of these urgency indicators:
- 🟥 **Emergency** - Life-threatening, requires immediate action
- 🟧 **High Priority** - Urgent but not immediately life-threatening  
- 🟨 **Routine** - Standard follow-up
- 🟩 **Informational** - For records only

# Medical Findings
- List all symptoms and complaints
- List lab test results with values
- List any diagnoses or impressions
- List medications if mentioned
- Include patient details if available

# Recommended Action
- What should be done next?
- Who should be notified?
- Timeline for action
- Priority level

# Clinical Reasoning
- Explain why you classified it this urgency level
- Highlight key findings that influenced the decision
- Note any concerning patterns or abnormal values

**IMPORTANT:** 
- Output ONLY plain text with markdown formatting
- DO NOT output JSON
- DO NOT use code blocks
- Use headers (# ## ###), bullet points, and **bold** text
- Keep it clear and readable for medical professionals"""
        
        logger.debug("=" * 60)
        logger.debug("PROMPT BEING SENT TO AI:")
        logger.debug(prompt)
        logger.debug("=" * 60)
        
        try:
            logger.info("  🤖 Invoking Medical AI Agent...")
            logger.debug(f"  Agent: {self.understanding_agent.name}")
            logger.debug(f"  Model: meta-llama/llama-4-scout-17b-16e-instruct")
            
            # Use the understanding agent directly
            response = self.understanding_agent.run(prompt)
            
            logger.info("  ✓ AI analysis completed")
            logger.info(f"  Response content length: {len(response.content)} characters")
            logger.debug("=" * 60)
            logger.debug("AI RESPONSE:")
            logger.debug(response.content)
            logger.debug("=" * 60)
        except Exception as e:
            logger.error(f"  ❌ AI analysis failed: {e}", exc_info=True)
            raise
        
        # Parse the response
        logger.info("📊 Step 3: Parsing Response...")
        logger.debug(f"  Response preview (first 500 chars): {response.content[:500]}...")
        try:
            result = self._parse_team_response(response.content, intake_result)
            logger.info(f"  ✓ Urgency Level: {result['urgency']}")
            logger.info(f"  ✓ Document Type: {result['document_type']}")
            logger.info(f"  ✓ Status: {result['status']}")
            logger.debug(f"  Full parsed result: {result}")
        except Exception as e:
            logger.error(f"  ❌ Response parsing failed: {e}", exc_info=True)
            raise
        
        logger.info("=" * 60)
        logger.info("✅ Analysis Complete!")
        logger.info("=" * 60)
        
        return result
    
    def _parse_team_response(self, content: str, intake_result: dict) -> dict:
        """Parse team response into structured format"""
        logger.debug("Parsing team response...")
        logger.debug(f"Looking for urgency keywords in content...")
        
        # Extract urgency level
        urgency = UrgencyLevel.ROUTINE
        content_lower = content.lower()
        
        logger.debug(f"Checking for 'emergency' or '🟥': {'emergency' in content_lower or '🟥' in content}")
        if "emergency" in content_lower or "🟥" in content:
            urgency = UrgencyLevel.EMERGENCY
            logger.info("  🟥 Detected: EMERGENCY")
        elif "high priority" in content_lower or "🟧" in content:
            urgency = UrgencyLevel.HIGH_PRIORITY
            logger.info("  🟧 Detected: HIGH PRIORITY")
        elif "routine" in content_lower or "🟨" in content:
            urgency = UrgencyLevel.ROUTINE
            logger.info("  🟨 Detected: ROUTINE")
        elif "informational" in content_lower or "🟩" in content:
            urgency = UrgencyLevel.INFORMATIONAL
            logger.info("  🟩 Detected: INFORMATIONAL")
        
        logger.debug(f"Final urgency level: {urgency.value}")
        
        result = {
            "urgency": urgency.value,
            "document_type": intake_result["document_type"],
            "analysis": content,
            "status": "completed"
        }
        
        logger.debug(f"Returning result with keys: {result.keys()}")
        return result


def analyze_text(text: str) -> dict:
    """Convenience function to analyze text"""
    workflow = ClinOpsAIWorkflow()
    return workflow.analyze_document(text)
