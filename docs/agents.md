# ClinOps AI Agents

## Overview

The ClinOps AI system uses specialized agents, each designed for a specific task in the medical document analysis pipeline.

## Agent Design Philosophy

Each agent is:
- **Single-purpose**: Focused on one specific task
- **Composable**: Can be combined in workflows
- **Configurable**: Uses environment-based settings
- **Observable**: Comprehensive logging at all levels

---

## 1. Intake Agent

**File**: `src/agents/intake.py`

### Purpose
Document ingestion, validation, and preprocessing.

### Responsibilities
- Accept various document formats (text, PDF, images)
- Extract metadata
- Generate content hash for deduplication
- Validate document completeness
- Clean and normalize text

### Implementation

```python
def get_intake_agent() -> Agent:
    return Agent(
        name="Medical Intake Agent",
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        role="Document intake specialist",
        instructions=[
            "Accept medical documents in various formats",
            "Extract metadata from document headers",
            "Check for duplicates using content hashing",
            "Validate document completeness",
            "Pass clean document to next agent"
        ]
    )
```

### Key Function
```python
def process_document_intake(text: str) -> dict:
    """Process document intake"""
    content_hash = hashlib.sha256(text.encode()).hexdigest()
    doc_type = detect_document_type(text)
    
    return {
        "content": text,
        "content_hash": content_hash,
        "document_type": doc_type,
        "status": "processed"
    }
```

### Output
```python
{
    "content": "cleaned document text",
    "content_hash": "sha256 hash",
    "document_type": "lab_report|consultation|discharge|referral|unknown",
    "status": "processed"
}
```

---

## 2. Vision Agent

**File**: `src/agents/vision.py`

### Purpose
Image processing and OCR for scanned documents.

### Responsibilities
- Process medical document images
- Perform OCR on scanned PDFs
- Extract text from faxes
- Preserve formatting and structure
- Handle handwritten text (when possible)

### Model
- `meta-llama/llama-4-scout-17b-16e-instruct` (with vision capabilities)

### Instructions
```
- Process medical document images and scanned PDFs
- Perform OCR with high accuracy
- Handle handwritten text when present
- Preserve document structure and layout
- Clean and normalize extracted text
- Preserve important formatting and structure
```

### Use Cases
- Scanned lab reports
- Faxed referrals
- Photographed documents
- Legacy paper records

---

## 3. Understanding Agent

**File**: `src/agents/understanding.py`

### Purpose
Medical entity extraction and clinical comprehension.

### Responsibilities
- Extract symptoms and complaints
- Identify lab tests and values
- Extract diagnoses and conditions
- Identify medications
- Extract patient demographics
- Understand clinical context

### Model
- `meta-llama/llama-4-scout-17b-16e-instruct`

### Instructions
```
- Extract all symptoms mentioned in the document
- Identify all lab tests and their values
- Extract diagnoses and medical conditions
- Identify medications if present
- Extract patient and doctor information
- Understand clinical context, not just keywords
- Return structured entities in comprehendible format
```

### Entity Types Extracted

#### Patient Information
- Name
- Age
- Gender
- Medical record number

#### Symptoms
- Chief complaint
- Duration
- Severity
- Location

#### Lab Results
- Test name
- Value
- Unit
- Normal range
- Abnormal flag

#### Diagnoses
- Primary diagnosis
- Secondary diagnoses
- Impressions

#### Medications
- Drug name
- Dosage
- Frequency
- Route

---

## 4. Urgency Agent

**File**: `src/agents/urgency.py`

### Purpose
Clinical urgency and risk assessment.

### Responsibilities
- Analyze medical findings for urgency
- Assess risk level
- Consider temporal changes
- Evaluate symptom severity
- Analyze document language intensity

### Model
- `meta-llama/llama-4-scout-17b-16e-instruct`

### Urgency Levels

| Level | Indicator | Examples |
|-------|-----------|----------|
| 🟥 **Emergency** | Life-threatening | MI, stroke, severe bleeding |
| 🟧 **High Priority** | Urgent, not immediate | Abnormal labs, worsening symptoms |
| 🟨 **Routine** | Standard care | Follow-up, stable conditions |
| 🟩 **Informational** | Records only | Normal results, routine updates |

### Decision Factors
- **Lab Values**: Critically abnormal results
- **Symptoms**: Severity and acuity
- **Temporal Changes**: Rapid deterioration
- **Document Language**: "STAT", "urgent", "immediately"
- **Context**: Patient history and risk factors

---

## 5. Decision Agent

**File**: `src/agents/decision.py`

### Purpose
Action recommendation and routing logic.

### Responsibilities
- Decide appropriate actions based on urgency
- Determine notification recipients
- Specify timelines
- Route to appropriate care pathway

### Model
- `meta-llama/llama-4-scout-17b-16e-instruct`

### Decision Matrix

| Urgency | Action | Timeline | Notification |
|---------|--------|----------|-------------|
| 🟥 Emergency | Immediate intervention | Now | On-call physician, ER |
| 🟧 High Priority | Urgent consultation | 24-48 hours | Primary physician |
| 🟨 Routine | Schedule follow-up | Days to weeks | Care coordinator |
| 🟩 Informational | File in EMR | N/A | None |

### Output Format
```markdown
# Recommended Action

**Urgency**: 🟥 Emergency

**Immediate Actions**:
- Notify on-call cardiologist immediately
- Prepare for possible cardiac catheterization
- Continuous cardiac monitoring

**Timeline**: Immediate (within 15 minutes)

**Notifications**:
- Dr. Smith (on-call cardiology)
- Emergency department
- Patient's primary physician
```

---

## 6. Audit Agent

**File**: `src/agents/audit.py`

### Purpose
Decision explanation and compliance logging.

### Responsibilities
- Generate clear explanations of WHY decisions were made
- Document evidence used
- Provide confidence scores
- Create audit trails
- Ensure regulatory compliance

### Model
- `meta-llama/llama-4-scout-17b-16e-instruct`

### Output Structure
```markdown
# Clinical Reasoning

**Decision Basis**:
- Elevated Troponin I (0.8 ng/mL) indicates myocardial injury
- ST elevation in leads II, III, aVF suggests inferior wall MI
- Acute presentation with severe symptoms

**Evidence Used**:
- Lab result: Troponin I
- ECG findings: ST elevation
- Symptom severity: 9/10 chest pain

**Confidence**: 95%

**Compliance Notes**:
- Meets criteria for STEMI protocol activation
- Documented at 2026-01-20 12:30:45
- Reviewed by: AI System (ClinOps)
```

---

## Agent Communication

### Current Implementation
Agents operate independently, called sequentially by the workflow orchestrator.

```python
# Workflow order
intake_result = process_document_intake(text)
ai_response = understanding_agent.run(prompt)
parsed_result = parse_response(ai_response)
```

### Future: Team-based Communication
```python
team = Team(
    members=[understanding_agent, urgency_agent, decision_agent],
    instructions="Coordinate to analyze medical document"
)
result = team.run(document)
```

---

## Agent Configuration

### Common Parameters
- **name**: Human-readable agent name
- **model**: Groq model specification
- **role**: Agent's primary responsibility
- **instructions**: List of specific directives

### Example
```python
Agent(
    name="Medical Understanding Agent",
    model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
    role="Medical NLP specialist",
    instructions=[
        "Extract symptoms",
        "Identify lab tests",
        "Extract diagnoses"
    ]
)
```

---

## Testing Agents

### Unit Testing
```python
def test_understanding_agent():
    agent = get_understanding_agent()
    result = agent.run("Patient has fever and cough")
    assert "fever" in result.content.lower()
    assert "cough" in result.content.lower()
```

### Integration Testing
```python
def test_full_workflow():
    workflow = ClinOpsAIWorkflow()
    result = workflow.analyze_document(sample_document)
    assert result["urgency"] in ["🟥 Emergency", "🟧 High Priority", ...]
```

---

## Best Practices

### Agent Design
1. **Single Responsibility**: Each agent does one thing well
2. **Clear Instructions**: Specific, actionable directives
3. **Appropriate Models**: Match model capability to task complexity
4. **Error Handling**: Graceful degradation on failures

### Prompt Engineering
1. **Be Specific**: Clear expectations for output format
2. **Provide Context**: Include relevant background information
3. **Show Examples**: Demonstrate desired output format
4. **Constrain Output**: Explicitly state what NOT to do

### Performance
1. **Concise Prompts**: Reduce token usage
2. **Efficient Models**: Use smaller models when possible
3. **Caching**: Cache common entities and patterns
4. **Async**: Run independent agents in parallel
