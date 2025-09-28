# 🔌 Healthcare Chatbot API Reference

Complete documentation for the Healthcare Chatbot FastAPI backend.

## 📋 Overview

The Healthcare Chatbot API provides endpoints for processing health-related queries using OpenAI GPT-4, with fallback responses when the AI service is unavailable.

**Base URL**: `http://localhost:8000`  
**Content-Type**: `application/json`  
**CORS**: Enabled for `http://localhost:3000`

## 🛡️ Authentication

Currently, no authentication is required for local development. In production, consider implementing:
- API key authentication
- Rate limiting
- Request validation

## 📡 Endpoints

### 1. Root Endpoint

**`GET /`**

Health check and basic API information.

#### Response
```json
{
  "message": "Healthcare Chatbot API is running",
  "version": "1.0.0",
  "endpoints": ["/diagnose", "/history"],
  "openai_available": true
}
```

#### Status Codes
- `200` - API is running successfully

---

### 2. Diagnose Symptoms

**`POST /diagnose`**

Main endpoint for processing user symptoms and returning healthcare advice.

#### Request Body
```json
{
  "symptoms": "I have a headache and feel dizzy"
}
```

#### Request Schema
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| symptoms | string | Yes | User's symptom description |

#### Response
```json
{
  "advice": "For mild headaches and dizziness, try: Rest in a quiet, dark room; Stay hydrated...",
  "severity": "mild",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

#### Response Schema
| Field | Type | Description |
|-------|------|-------------|
| advice | string | Healthcare advice and recommendations |
| severity | string | Either "mild" or "serious" |
| timestamp | string | ISO 8601 formatted timestamp |

#### Severity Classification
- **"mild"**: Common cold, minor headaches, mild fever
- **"serious"**: Chest pain, difficulty breathing, severe symptoms

#### Status Codes
- `200` - Successful diagnosis
- `422` - Invalid request body
- `500` - Internal server error

#### Example Requests

**Mild Symptoms:**
```bash
curl -X POST http://localhost:8000/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "I have a minor headache"}'
```

**Serious Symptoms:**
```bash
curl -X POST http://localhost:8000/diagnose \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "chest pain and difficulty breathing"}'
```

---

### 3. Conversation History

**`GET /history`**

Retrieve all stored conversation history.

#### Response
```json
{
  "conversations": [
    {
      "user": "I have a headache",
      "response": "For mild headaches, try rest and hydration...",
      "severity": "mild",
      "timestamp": "2024-01-15T10:30:45.123456"
    }
  ]
}
```

#### Response Schema
| Field | Type | Description |
|-------|------|-------------|
| conversations | array | Array of conversation objects |

**Conversation Object:**
| Field | Type | Description |
|-------|------|-------------|
| user | string | User's original input |
| response | string | AI-generated response |
| severity | string | Assessed severity level |
| timestamp | string | ISO 8601 formatted timestamp |

#### Status Codes
- `200` - Successfully retrieved history
- `500` - Error reading conversation file

---

### 4. Health Check

**`GET /health`**

Detailed system health and configuration status.

#### Response
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:45.123456",
  "openai_configured": true,
  "conversations_file_exists": true
}
```

#### Response Schema
| Field | Type | Description |
|-------|------|-------------|
| status | string | Overall system status |
| timestamp | string | Current server timestamp |
| openai_configured | boolean | Whether OpenAI API is available |
| conversations_file_exists | boolean | Whether conversation history file exists |

#### Status Codes
- `200` - System is healthy
- `500` - System issues detected

---

## 🤖 AI Integration

### OpenAI GPT-4 Configuration
```python
MODEL = "gpt-4"
MAX_TOKENS = 300
TEMPERATURE = 0.7
```

### System Prompt
The AI uses a healthcare-focused system prompt that:
- Provides appropriate medical guidance
- Classifies symptom severity
- Includes safety disclaimers
- Avoids specific medical diagnoses

### Fallback System
When OpenAI is unavailable, the API provides:
- Pre-written responses for common symptoms
- Appropriate severity classification
- Medical disclaimers and safety warnings

## 📁 Data Storage

### Conversation Storage
- **File**: `conversations.json` in project root
- **Format**: JSON with conversation array
- **Auto-created**: File is created automatically on first use

### Example Storage Structure
```json
{
  "conversations": [
    {
      "user": "I have a fever",
      "response": "For mild fever (under 102°F): Rest and stay hydrated...",
      "severity": "mild",
      "timestamp": "2024-01-15T10:30:45.123456"
    }
  ]
}
```

## ⚠️ Error Handling

### Common Error Responses

**Invalid Request Body (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "symptoms"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

**OpenAI API Error (500):**
```json
{
  "detail": "Error processing request: OpenAI API error message"
}
```

**File System Error (500):**
```json
{
  "detail": "Error retrieving conversation history: File not found"
}
```

## 🔒 Security Considerations

### Input Validation
- Request body validation via Pydantic models
- SQL injection prevention (no SQL database used)
- XSS prevention through proper response handling

### API Security
- CORS configured for specific origins
- No sensitive data in responses
- OpenAI API key stored in environment variables

### Rate Limiting
Consider implementing rate limiting for production:
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/diagnose")
@limiter.limit("10/minute")
async def diagnose_symptoms(...):
    # endpoint logic
```

## 🧪 Testing

### Unit Tests
```python
# Test diagnostic endpoint
def test_diagnose_mild_symptoms():
    response = client.post("/diagnose", json={"symptoms": "headache"})
    assert response.status_code == 200
    assert response.json()["severity"] == "mild"

def test_diagnose_serious_symptoms():
    response = client.post("/diagnose", json={"symptoms": "chest pain"})
    assert response.status_code == 200
    assert response.json()["severity"] == "serious"
```

### Integration Tests
```bash
# Test all endpoints
curl http://localhost:8000/
curl http://localhost:8000/health
curl -X POST http://localhost:8000/diagnose -H "Content-Type: application/json" -d '{"symptoms": "test"}'
curl http://localhost:8000/history
```

## 📊 Performance

### Response Times
- **Root endpoint**: < 10ms
- **Health check**: < 50ms  
- **Diagnose (with OpenAI)**: 1-5 seconds
- **Diagnose (fallback)**: < 100ms
- **History retrieval**: < 50ms

### Scalability Considerations
- Implement database for production (PostgreSQL, MongoDB)
- Add caching layer (Redis)
- Use connection pooling for OpenAI API
- Implement background task processing

## 🚀 Production Deployment

### Environment Variables
```bash
# Required
OPENAI_API_KEY=sk-your-production-key

# Optional
HOST=0.0.0.0
PORT=8000
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ app/
WORKDIR app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes Configuration
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthcare-chatbot-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: healthcare-chatbot-api
  template:
    metadata:
      labels:
        app: healthcare-chatbot-api
    spec:
      containers:
      - name: api
        image: healthcare-chatbot:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: api-secrets
              key: openai-key
```

## 📝 Changelog

### v1.0.0 (Current)
- Initial API implementation
- OpenAI GPT-4 integration
- Fallback response system
- JSON file storage
- Basic CORS support
- Health check endpoints

### Planned Features
- User authentication
- Database integration
- Advanced analytics
- Multi-language support
- Voice input processing
- Integration with EHR systems

---

**For additional support, see the main README.md or SETUP_GUIDE.md files.**