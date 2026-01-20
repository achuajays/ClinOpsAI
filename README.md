<div align="center">

# 🏥 ClinOps AI

### Autonomous Intelligence System for Medical Document Decisions

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-purple.svg)](https://groq.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Transform raw medical documents into actionable clinical intelligence with AI-powered decision making, urgency assessment, and explainable recommendations.

[Quick Start](#-quick-start) • [Documentation](docs/) • [API Reference](docs/api.md) • [Deploy Guide](docs/deployment.md)

</div>

---

## 📊 System Architecture

```mermaid
graph TB
    subgraph UI[User Interface]
        A[Web Browser] --> B[Tailwind CSS UI]
    end
    
    subgraph API[API Layer]
        B --> C[FastAPI Server]
        C --> D[CORS Middleware]
        D --> E[API Endpoint]
    end
    
    subgraph WF[Workflow Orchestrator]
        E --> F[ClinOpsAIWorkflow]
        F --> G[Document Intake]
        G --> H[AI Analysis Engine]
        H --> I[Response Parser]
    end
    
    subgraph AI[AI Layer]
        H --> J[Understanding Agent]
        J --> K[Groq LLM API]
        K --> J
    end
    
    subgraph DP[Data Processing]
        I --> L[Urgency Classifier]
        I --> M[Entity Extractor]
        I --> N[Decision Engine]
    end
    
    subgraph OUT[Output]
        L --> O[Structured Result]
        M --> O
        N --> O
        O --> P[Markdown Renderer]
        P --> B
    end
    
    style A fill:#e1f5ff
    style K fill:#f0e6ff
    style O fill:#e8f5e9
```

---

## 🔄 Analysis Workflow

```mermaid
sequenceDiagram
    participant User
    participant UI as Web Interface
    participant API as FastAPI
    participant WF as Workflow
    participant AI as AI Agent
    participant Groq as Groq LLM
    
    User->>UI: Submit Document
    UI->>API: POST /api/analyze
    API->>WF: analyze_document(text)
    
    rect rgb(240, 248, 255)
        Note over WF: Step 1: Intake Processing
        WF->>WF: Calculate hash
        WF->>WF: Detect type
        WF->>WF: Clean text
    end
    
    rect rgb(255, 240, 245)
        Note over WF,Groq: Step 2: AI Analysis
        WF->>AI: run(prompt)
        AI->>Groq: LLM Request
        Groq-->>AI: Analysis Response
        AI-->>WF: Markdown Text
    end
    
    rect rgb(240, 255, 240)
        Note over WF: Step 3: Parse Response
        WF->>WF: Detect urgency
        WF->>WF: Structure result
    end
    
    WF-->>API: JSON Result
    API-->>UI: Analysis Data
    UI->>UI: Render Markdown
    UI-->>User: Display Results
```

---

## 🔥 What Makes ClinOps AI Unique

Most systems build: **PDF → text → summary**

**ClinOps AI builds:** `PDF → understanding → decision → action`

This is **decision intelligence**, not just document processing.

---

## 🩺 The Problem

Medical organizations receive thousands of documents daily:
- 📄 Lab reports
- 📋 Referral letters
- 🏥 Discharge summaries
- 💊 Consultation notes
- 📠 Faxes (images + PDFs)

**Challenges:**
- ⚠️ Urgent cases get missed
- ⏱️ Manual triage is slow
- 😓 Doctors waste time reading irrelevant docs
- 📊 No structured intelligence layer

**ClinOps AI acts like an autonomous clinical coordinator.**

---

## ✨ Core Capabilities

### 1️⃣ Document Understanding
- Identifies document type automatically
- Extracts clinical intent and meaning
- Understands **context**, not just keywords

### 2️⃣ Clinical Urgency Reasoning
Classifies documents using AI reasoning:
- 🟥 **Emergency** - Immediate action required
- 🟧 **High Priority** - Urgent follow-up needed
- 🟨 **Routine** - Standard care pathway
- 🟩 **Informational** - For records only

### 3️⃣ Autonomous Decision Engine
Decides automatically:
- Notify doctor immediately
- Schedule specialist follow-up
- Create EMR task
- Store for records
- Escalate to emergency queue

### 4️⃣ Explainability Layer
For every decision:
- **WHY** it was made
- **Which data** triggered it
- **Confidence score**
- Complete decision trace

---

## 🧠 Agent-Based Architecture

```
┌─────────────────────┐
│   Document Input    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Intake Agent      │  (Validation, Deduplication)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Vision Agent      │  (OCR, Layout Understanding)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Understanding Agent │  (Entity Extraction, NLP)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Urgency Agent      │  (Risk Assessment)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│  Decision Agent     │  (Action Routing)
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   Audit Agent       │  (Explanation, Compliance)
└─────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Groq API Key ([Get one here](https://console.groq.com))

### Installation

```bash
# Clone the repository
cd ClinOpsAI

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Running the Application

**Option 1: Web UI (Recommended)**
```bash
uvicorn api.main:app --reload
```
Then open http://localhost:8000 in your browser

**Option 2: CLI**
```bash
# Interactive mode
python main.py

# From file
python main.py path/to/medical_document.txt
```

---

## 📡 API Endpoints

### `GET /`
Serves the Tailwind CSS dashboard

### `GET /health`
Health check endpoint

### `POST /api/analyze`
Analyze medical document

**Request:**
```json
{
  "text": "Patient presents with chest pain, elevated Troponin..."
}
```

**Response:**
```json
{
  "urgency": "🟥 Emergency",
  "decision": "Notify doctor immediately",
  "document_type": "lab_report",
  "analysis": "Detailed clinical analysis...",
  "status": "completed"
}
```

---

---

## 🔀 Data Flow

```mermaid
flowchart TD
    A[Medical Document] -->|Text Input| B{Document Type?}
    B -->|Lab Report| C[Extract Tests & Values]
    B -->|Consultation| D[Extract Symptoms & Findings]
    B -->|Discharge| E[Extract Diagnoses & Plans]
    B -->|Unknown| F[General Analysis]
    
    C --> G[AI Analysis]
    D --> G
    E --> G
    F --> G
    
    G --> H{Urgency Detection}
    H -->|🟥 Emergency| I[Immediate Action]
    H -->|🟧 High Priority| J[Urgent Follow-up]
    H -->|🟨 Routine| K[Standard Care]
    H -->|🟩 Informational| L[Archive]
    
    I --> M[Structured Output]
    J --> M
    K --> M
    L --> M
    
    M --> N[Markdown Rendering]
    N --> O[User Display]
    
    style A fill:#e1f5ff
    style G fill:#f0e6ff
    style H fill:#fff9c4
    style M fill:#e8f5e9
    style O fill:#ffe0b2
```

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **AI Framework** | [Agno](https://github.com/agno-agi/agno) |
| **LLM Provider** | [Groq](https://groq.com) (Llama 3.1 70B, Vision) |
| **Backend** | FastAPI |
| **Frontend** | HTML + Tailwind CSS |
| **Language** | Python 3.9+ |

---

## 📋 Example Use Cases

### Emergency Detection
```
Input: "Elevated Troponin I: 0.8 ng/mL, ST elevation in ECG"
Output: 🟥 Emergency - Immediate cardiology consult
```

### High Priority Referral
```
Input: "Significant decline in kidney function, eGFR: 28"
Output: 🟧 High Priority - Nephrology referral within 3 days
```

### Routine Follow-up
```
Input: "Blood pressure well controlled, continue current meds"
Output: 🟨 Routine - Schedule 6-month follow-up
```

---

## 🎯 Project Structure

```
ClinOpsAI/
├── api/
│   ├── main.py              # FastAPI application
│   └── templates/
│       └── index.html       # Tailwind UI
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── intake.py
│   │   ├── vision.py
│   │   ├── understanding.py
│   │   ├── urgency.py
│   │   ├── decision.py
│   │   └── audit.py
│   ├── models/
│   │   └── schemas.py       # Pydantic models
│   └── workflow.py          # Team orchestrator
├── main.py                  # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔐 Environment Variables

```env
GROQ_API_KEY=your_groq_api_key_here
```

---

## 🤝 Contributing

This is a demonstration project. For production use:
1. Add proper error handling
2. Implement database storage
3. Add authentication
4. Integrate with EMR systems
5. Add HIPAA compliance measures
6. Implement audit logging

---

## 📄 License

MIT License - feel free to use for your own projects

---

## 🙏 Acknowledgments

- Built with [Agno](https://docs.agno.com) multi-agent framework
- Powered by [Groq](https://groq.com) ultra-fast LLM inference
- UI designed with [Tailwind CSS](https://tailwindcss.com)

---

## 🚀 Future Roadmap

- [ ] Multi-language support
- [ ] Voice input for dictation
- [ ] Integration with FHIR standards
- [ ] Mobile app
- [ ] Real-time EMR integration
- [ ] Advanced analytics dashboard

---

---

## 🚢 Deployment Architecture

```mermaid
graph TB
    subgraph STACK[Docker Compose Stack]
        subgraph APP[Application]
            A[ClinOps AI :8000]
        end
        
        subgraph ELK[ELK Stack]
            B[Elasticsearch :9200]
            C[Logstash :5000]
            D[Kibana :5601]
            E[Filebeat]
        end
    end
    
    subgraph EXT[External Services]
        F[Groq API LLM]
    end
    
    subgraph STOR[Storage]
        G[(Elasticsearch Data)]
        H[(App Logs)]
        I[(Uploads)]
    end
    
    A -->|API Calls| F
    A -->|Write Logs| H
    E -->|Ship Logs| C
    C -->|Index| B
    B -->|Store| G
    D -->|Query| B
    A -->|Store Files| I
    
    style A fill:#667eea,color:#fff
    style B fill:#00bfb3
    style C fill:#f04e98
    style D fill:#00bfb3
    style F fill:#f0e6ff
```

### Infrastructure Components

| Component | Purpose | Port |
|-----------|---------|------|
| **ClinOps AI** | Main application | 8000 |
| **Elasticsearch** | Log storage & search | 9200 |
| **Logstash** | Log processing | 5000 |
| **Kibana** | Log visualization | 5601 |
| **Filebeat** | Log shipping | - |

### Quick Deploy

```bash
# Clone repository
git clone <repo-url>
cd ClinOpsAI

# Set API key
echo "GROQ_API_KEY=your_key" > .env

# Start with ELK stack
docker-compose up -d

# Access services
# - App: http://localhost:8000
# - Kibana: http://localhost:5601
```

---

**Built with ❤️ for healthcare professionals**
