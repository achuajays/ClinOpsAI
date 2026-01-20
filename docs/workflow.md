# ClinOps AI Workflow

## Overview

The workflow orchestrates the entire document analysis pipeline from input to output.

## Workflow Class: `ClinOpsAIWorkflow`

**File**: `src/workflow.py`

### Initialization

```python
def __init__(self):
    # Load environment
    self.groq_api_key = os.getenv("GROQ_API_KEY")
    
    # Initialize agents
    self.understanding_agent = get_understanding_agent()
    self.urgency_agent = get_urgency_agent()
    self.decision_agent = get_decision_agent()
    self.audit_agent = get_audit_agent()
    
    # Create team (for future use)
    self.team = Team(
        name="ClinOps Medical Intelligence Team",
        model=Groq(id="meta-llama/llama-4-scout-17b-16e-instruct"),
        members=[...]
    )
```

---

## Analysis Pipeline

### Step 1: Document Intake

**Purpose**: Validate and preprocess the input document

```python
intake_result = process_document_intake(text)
```

**Actions**:
1. Calculate content hash (SHA-256)
2. Detect document type
3. Clean and normalize text
4. Validate completeness

**Output**:
```python
{
    "content": "cleaned text",
    "content_hash": "abc123...",
    "document_type": "lab_report",
    "status": "processed"
}
```

**Logging**:
```
📄 Step 1: Document Intake Processing...
  ✓ Document Type: lab_report
  ✓ Content Hash: abc123...
  ✓ Status: processed
```

---

### Step 2: AI Analysis

**Purpose**: Comprehensive medical document analysis

#### Prompt Construction

```python
prompt = f"""You are a medical document analysis AI.

**Document Type:** {intake_result['document_type']}

**Document Content:**
{intake_result['content']}

**Your Task:**
Provide a detailed medical analysis in PLAIN MARKDOWN TEXT

# Clinical Urgency Level
[urgency classification]

# Medical Findings
[extracted entities]

# Recommended Action
[action plan]

# Clinical Reasoning
[explanation]
"""
```

#### AI Invocation

```python
response = self.understanding_agent.run(prompt)
```

**Logging**:
```
🧠 Step 2: Running AI Analysis...
  🤖 Invoking Medical AI Agent...
  Agent: Medical Understanding Agent
  Model: meta-llama/llama-4-scout-17b-16e-instruct
  ✓ AI analysis completed
  Response content length: 1234 characters
```

---

### Step 3: Response Parsing

**Purpose**: Extract structured data from AI response

```python
result = self._parse_team_response(response.content, intake_result)
```

#### Urgency Detection

The parser looks for urgency indicators in the response:

```python
if "emergency" in content.lower() or "🟥" in content:
    urgency = UrgencyLevel.EMERGENCY
elif "high priority" in content.lower() or "🟧" in content:
    urgency = UrgencyLevel.HIGH_PRIORITY
elif "routine" in content.lower() or "🟨" in content:
    urgency = UrgencyLevel.ROUTINE
elif "informational" in content.lower() or "🟩" in content:
    urgency = UrgencyLevel.INFORMATIONAL
```

#### Output Structure

```python
{
    "urgency": "🟥 Emergency",
    "document_type": "lab_report",
    "analysis": "full markdown text",
    "status": "completed"
}
```

**Logging**:
```
📊 Step 3: Parsing Response...
  🟥 Detected: EMERGENCY
  ✓ Urgency Level: 🟥 Emergency
  ✓ Document Type: lab_report
  ✓ Status: completed
```

---

## Complete Flow Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    User Input (Text)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Step 1: Document Intake                                │
│  ├─ Calculate hash                                      │
│  ├─ Detect type                                         │
│  ├─ Clean text                                          │
│  └─ Validate                                            │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: AI Analysis                                    │
│  ├─ Build comprehensive prompt                          │
│  ├─ Invoke Understanding Agent                          │
│  ├─ Receive markdown response                           │
│  └─ Log response details                                │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: Response Parsing                               │
│  ├─ Detect urgency level                                │
│  ├─ Extract key information                             │
│  ├─ Structure result                                    │
│  └─ Validate output                                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│             Return Structured Result                    │
└─────────────────────────────────────────────────────────┘
```

---

## Error Handling

### Intake Errors
```python
try:
    intake_result = process_document_intake(text)
except Exception as e:
    logger.error(f"❌ Intake processing failed: {e}", exc_info=True)
    raise
```

### AI Analysis Errors
```python
try:
    response = self.understanding_agent.run(prompt)
except Exception as e:
    logger.error(f"❌ AI analysis failed: {e}", exc_info=True)
    raise
```

### Parsing Errors
```python
try:
    result = self._parse_team_response(response.content, intake_result)
except Exception as e:
    logger.error(f"❌ Response parsing failed: {e}", exc_info=True)
    raise
```

---

## Logging Strategy

### Log Levels

| Level | Use Case |
|-------|----------|
| **DEBUG** | Detailed execution traces, prompts, responses |
| **INFO** | Major steps, milestones, results |
| **WARNING** | Unexpected but handled conditions |
| **ERROR** | Failures requiring attention |

### Example Logs

```
2026-01-20 12:54:08,090 - src.workflow - INFO - ============================================================
2026-01-20 12:54:08,091 - src.workflow - INFO - 🏥 Starting Medical Document Analysis
2026-01-20 12:54:08,092 - src.workflow - INFO - ============================================================
2026-01-20 12:54:08,093 - src.workflow - INFO - 📄 Step 1: Document Intake Processing...
2026-01-20 12:54:08,094 - src.workflow - DEBUG -   Input text preview (first 200 chars): Patient: John Doe, Age 58...
2026-01-20 12:54:08,095 - src.workflow - INFO -   ✓ Document Type: unknown
2026-01-20 12:54:08,096 - src.workflow - INFO -   ✓ Content Hash: 5f4dcc3b5aa765...
2026-01-20 12:54:08,097 - src.workflow - INFO -   ✓ Status: processed
```

---

## Performance Optimization

### Current Bottlenecks
1. **AI Inference Time**: 2-5 seconds
2. **Network Latency**: Variable
3. **Response Parsing**: <100ms

### Optimization Strategies

#### 1. Prompt Optimization
- Keep prompts concise but comprehensive
- Use clear structure and formatting
- Avoid unnecessary verbosity

#### 2. Caching
```python
# Future implementation
cache = {}
cache_key = f"{doc_type}_{content_hash}"
if cache_key in cache:
    return cache[cache_key]
```

#### 3. Async Processing
```python
# Future implementation
async def analyze_document(self, text: str):
    intake_result = await async_process_intake(text)
    response = await self.understanding_agent.arun(prompt)
    return self._parse_response(response)
```

#### 4. Parallel Agent Execution
```python
# Future implementation
results = await asyncio.gather(
    understanding_agent.arun(prompt),
    urgency_agent.arun(prompt),
    decision_agent.arun(prompt)
)
```

---

## Testing Workflows

### Unit Test Example
```python
def test_workflow_initialization():
    workflow = ClinOpsAIWorkflow()
    assert workflow.understanding_agent is not None
    assert workflow.groq_api_key is not None
```

### Integration Test Example
```python
def test_complete_analysis():
    workflow = ClinOpsAIWorkflow()
    sample_doc = "Patient presents with chest pain..."
    
    result = workflow.analyze_document(sample_doc)
    
    assert "urgency" in result
    assert "document_type" in result
    assert "analysis" in result
    assert result["status"] == "completed"
```

### End-to-End Test
```python
def test_emergency_detection():
    workflow = ClinOpsAIWorkflow()
    emergency_doc = """
    Elevated Troponin, ST elevation, severe chest pain.
    STAT cardiology consult.
    """
    
    result = workflow.analyze_document(emergency_doc)
    assert "🟥" in result["urgency"] or "Emergency" in result["urgency"]
```

---

## Future Enhancements

### 1. Team-Based Orchestration
Enable multi-agent collaboration:
```python
self.team.run(document)  # Agents collaborate automatically
```

### 2. Streaming Responses
Real-time updates to UI:
```python
async for chunk in workflow.analyze_stream(text):
    yield chunk  # Stream to frontend
```

### 3. Batch Processing
Handle multiple documents:
```python
results = workflow.analyze_batch(documents)
```

### 4. Historical Analysis
Learn from past decisions:
```python
workflow.learn_from_history(past_analyses)
```

---

## Configuration

### Environment Variables
```bash
GROQ_API_KEY=your_api_key_here
LOG_LEVEL=DEBUG  # Optional: INFO, WARNING, ERROR
```

### Runtime Settings
```python
# In workflow initialization
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

## Troubleshooting

### Common Issues

#### 1. Empty Response
**Problem**: AI returns empty or None response
**Solution**: Check prompt structure and model availability

#### 2. Wrong Urgency Detection
**Problem**: System misclassifies urgency
**Solution**: Update urgency detection keywords

#### 3. Slow Performance
**Problem**: Analysis takes >10 seconds
**Solution**: Optimize prompt, check network, verify API limits

#### 4. Parsing Errors
**Problem**: Cannot extract structured data
**Solution**: Enhance response parser, add fallback logic
