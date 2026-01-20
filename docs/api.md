# ClinOps AI API Documentation

## Base URL
```
http://localhost:8000
```

---

## Endpoints

### 1. Health Check

#### `GET /health`

Check if the API is running and healthy.

**Request**:
```http
GET /health HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "status": "healthy",
  "service": "ClinOps AI",
  "version": "1.0.0"
}
```

**Status Codes**:
- `200 OK` - Service is healthy
- `503 Service Unavailable` - Service is down

---

### 2. Serve UI

#### `GET /`

Serves the main web interface.

**Request**:
```http
GET / HTTP/1.1
Host: localhost:8000
```

**Response**:
- HTML page with Tailwind CSS interface
- Status: `200 OK`

---

### 3. Analyze Document

#### `POST /api/analyze`

Analyze a medical document and return structured intelligence.

**Request Headers**:
```http
Content-Type: application/json
Accept: application/json
```

**Request Body**:
```json
{
  "text": "Patient presents with chest pain, elevated Troponin I (0.8 ng/mL). ECG shows ST elevation."
}
```

**Response**:
```json
{
  "urgency": "🟥 Emergency",
  "document_type": "lab_report",
  "analysis": "# Clinical Urgency Level\n\n🟥 **Emergency**\n\n# Medical Findings\n...",
  "status": "completed"
}
```

**Status Codes**:
- `200 OK` - Analysis successful
- `400 Bad Request` - No text provided
- `500 Internal Server Error` - Analysis failed

---

### 4. System Statistics

#### `GET /api/stats`

Get system statistics (placeholder).

**Request**:
```http
GET /api/stats HTTP/1.1
Host: localhost:8000
```

**Response**:
```json
{
  "total_analyses": 0,
  "uptime": "1h 23m",
  "status": "operational"
}
```

---

## Request/Response Examples

### Example 1: Emergency Case

**Request**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Patient: John Doe, Age 58. Severe chest pain radiating to left arm. Troponin I: 0.8 ng/mL. ECG shows ST elevation in leads II, III, aVF."
  }'
```

**Response**:
```json
{
  "urgency": "🟥 Emergency",
  "document_type": "unknown",
  "analysis": "# Clinical Urgency Level\n\n🟥 **Emergency** - Life-threatening condition detected\n\n# Medical Findings\n\n**Symptoms:**\n- Severe chest pain radiating to left arm\n\n**Lab Results:**\n- Troponin I: 0.8 ng/mL (Critical - Normal: <0.04)\n\n**ECG Findings:**\n- ST elevation in leads II, III, aVF\n- Indicates inferior wall MI\n\n# Recommended Action\n\n**Immediate Actions Required:**\n1. Activate STEMI protocol immediately\n2. Notify on-call cardiologist STAT\n3. Prepare for emergency cardiac catheterization\n4. Administer aspirin 325mg, nitroglycerin\n5. Continuous cardiac monitoring\n\n**Timeline:** Immediate (door-to-balloon < 90 minutes)\n\n**Notifications:**\n- On-call interventional

 cardiologist\n- Emergency department\n- Cardiac catheterization lab\n\n# Clinical Reasoning\n\n**Why Emergency:**\n\nThis patient presents with classic STEMI (ST-Elevation Myocardial Infarction):\n\n1. **Elevated Troponin** (0.8 ng/mL) indicates active myocardial injury\n2. **ST Elevation** in inferior leads confirms acute MI\n3. **Severe symptoms** with radiation suggest ongoing ischemia\n\n**Risk Level:** Extremely high - requires immediate intervention to prevent death or permanent cardiac damage.\n\n**Confidence:** 98% - Clear diagnostic criteria met",
  "status": "completed"
}
```

---

### Example 2: Routine Case

**Request**:
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Follow-up visit. Blood pressure: 128/82. Patient reports feeling well. Continue current medications."
  }'
```

**Response**:
```json
{
  "urgency": "🟨 Routine",
  "document_type": "unknown",
  "analysis": "# Clinical Urgency Level\n\n🟨 **Routine** - Standard follow-up care\n\n# Medical Findings\n\n**Vital Signs:**\n- Blood pressure: 128/82 mmHg (Well controlled)\n\n**Patient Status:**\n- Feeling well\n- No new complaints\n\n# Recommended Action\n\n**Next Steps:**\n1. Continue current medications\n2. Schedule routine follow-up in 3-6 months\n3. Reinforce lifestyle modifications\n\n**Timeline:** Routine scheduling (3-6 months)\n\n**Notifications:** None required\n\n# Clinical Reasoning\n\n**Why Routine:**\n\nThis is a straightforward follow-up visit with:\n\n1. **Controlled blood pressure** within target range\n2. **No new symptoms** or concerns\n3. **Stable clinical status**\n\nNo urgent intervention needed. Continue current management plan.\n\n**Confidence:** 95%",
  "status": "completed"
}
```

---

## Error Handling

### 400 Bad Request

**Cause**: No text provided in request

**Response**:
```json
{
  "detail": "No text or file provided"
}
```

### 500 Internal Server Error

**Cause**: Analysis failed (AI error, parsing error, etc.)

**Response**:
```json
{
  "detail": "Agent.__init__() got an unexpected keyword argument 'response_model'"
}
```

---

## Rate Limiting

**Current**: No rate limiting implemented

**Future**: 
- 100 requests per minute per IP
- 1000 requests per hour per API key

---

## Authentication

**Current**: None (open API)

**Future**:
- API Key authentication
- JWT tokens
- OAuth 2.0

---

## CORS Configuration

**Allowed Origins**: All (`*`)

**Allowed Methods**: 
- `GET`
- `POST`
- `OPTIONS`

**Allowed Headers**:
- `Content-Type`
- `Authorization`

---

## Response Field Descriptions

### Analysis Response

| Field | Type | Description |
|-------|------|-------------|
| `urgency` | string | Urgency level with emoji (🟥🟧🟨🟩) |
| `document_type` | string | Detected document type |
| `analysis` | string | Full markdown-formatted analysis |
| `status` | string | Processing status (`completed`, `failed`) |

---

## Performance

### Typical Response Times
- **Health check**: <10ms
- **Analysis**: 3-6 seconds
- **UI serving**: <50ms

### Payload Limits
- **Max request size**: 10MB
- **Max text length**: 50,000 characters

---

## WebSocket Support

**Status**: Not currently implemented

**Future**: Real-time streaming of analysis results

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/analyze');
ws.send(JSON.stringify({ text: document }));
ws.onmessage = (event) => {
  console.log('Partial result:', event.data);
};
```

---

## Testing with cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Analyze Document
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Patient has fever and cough"}'
```

### Pretty Print Response
```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Patient has fever"}' | jq .
```

---

## Testing with Python

```python
import requests

# Analyze document
response = requests.post(
    "http://localhost:8000/api/analyze",
    json={"text": "Patient presents with chest pain"}
)

result = response.json()
print(f"Urgency: {result['urgency']}")
print(f"Analysis:\n{result['analysis']}")
```

---

## Testing with JavaScript

```javascript
// Analyze document
fetch('http://localhost:8000/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ 
    text: 'Patient presents with chest pain' 
  })
})
.then(res => res.json())
.then(data => {
  console.log('Urgency:', data.urgency);
  console.log('Analysis:', data.analysis);
})
.catch(err => console.error('Error:', err));
```

---

## API Versioning

**Current**: No versioning

**Future**: 
- URL-based: `/api/v1/analyze`, `/api/v2/analyze`
- Header-based: `API-Version: 1.0`

---

## Deprecation Policy

When endpoints are deprecated:
1. Announcement 90 days in advance
2. Warning headers in responses
3. Documentation updated
4. Support for 6 months after deprecation

---

## Support

For API issues:
- Check logs: `docker logs clinops-ai`
- Debug mode: Set `LOG_LEVEL=DEBUG`
- Report issues: Create GitHub issue
