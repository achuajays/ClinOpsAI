"""Pydantic models for ClinOps AI"""
from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class UrgencyLevel(str, Enum):
    """Clinical urgency classification"""
    EMERGENCY = "🟥 Emergency"
    HIGH_PRIORITY = "🟧 High Priority"
    ROUTINE = "🟨 Routine"
    INFORMATIONAL = "🟩 Informational"


class MedicalDocument(BaseModel):
    """Input medical document"""
    text: str = Field(..., description="Raw text from medical document")
    document_type: Optional[str] = Field(None, description="Type of document (lab, referral, etc.)")
    metadata: Optional[dict] = Field(default_factory=dict)


class MedicalEntities(BaseModel):
    """Extracted medical entities"""
    symptoms: List[str] = Field(default_factory=list)
    tests: List[dict] = Field(default_factory=list, description="Test name and values")
    diagnoses: List[str] = Field(default_factory=list)
    medications: List[str] = Field(default_factory=list)
    patient_info: Optional[dict] = Field(None)
    doctor_info: Optional[dict] = Field(None)


class DecisionOutput(BaseModel):
    """Decision routing output"""
    action: str = Field(..., description="Action to take")
    priority: str = Field(..., description="Priority level")
    recipients: List[str] = Field(default_factory=list)
    details: str = Field(...)


class AuditTrace(BaseModel):
    """Explanation and audit trail"""
    why: str = Field(..., description="Why this decision was made")
    trigger_data: str = Field(..., description="Data that triggered the decision")
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning_chain: List[str] = Field(default_factory=list)


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    urgency: UrgencyLevel
    decision: DecisionOutput
    entities: MedicalEntities
    explanation: AuditTrace
