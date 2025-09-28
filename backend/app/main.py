import json
import os
from datetime import datetime
from typing import Dict, Any

import openai
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from decouple import config

# Initialize FastAPI app
app = FastAPI(
    title="Healthcare Chatbot API",
    description="AI-powered healthcare assistance with OpenAI GPT-4",
    version="1.0.0"
)

# CORS configuration for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# OpenAI configuration
try:
    openai.api_key = config('OPENAI_API_KEY')
    client = openai.OpenAI(api_key=config('OPENAI_API_KEY'))
except Exception as e:
    print(f"Warning: OpenAI API key not found or invalid: {e}")
    client = None

# Pydantic models
class SymptomRequest(BaseModel):
    symptoms: str

class DiagnosisResponse(BaseModel):
    advice: str
    severity: str
    timestamp: str

# Healthcare system prompt
SYSTEM_PROMPT = """
You are a helpful healthcare assistant. Analyze the user's symptoms and provide appropriate guidance.

For MILD symptoms (common cold, mild headache, minor cuts):
- Provide home remedies and self-care advice
- Suggest over-the-counter treatments if appropriate
- Mark severity as "mild"

For SERIOUS symptoms (chest pain, severe fever >102°F, difficulty breathing, severe injuries):
- Recommend immediate medical attention
- Advise contacting a doctor or emergency services
- Mark severity as "serious"

Always include appropriate disclaimers about consulting healthcare professionals.
Be concise but helpful. Do not diagnose specific medical conditions.
"""

# Fallback responses for when OpenAI is unavailable
FALLBACK_RESPONSES = {
    "mild": {
        "headache": "For mild headaches, try: Rest in a quiet, dark room; Stay hydrated; Apply a cold or warm compress to your head; Consider over-the-counter pain relievers like ibuprofen or acetaminophen. If headaches persist or worsen, consult a healthcare provider.",
        "cold": "For common cold symptoms: Get plenty of rest; Stay hydrated with water, warm tea, or clear broths; Use a humidifier or breathe steam from a hot shower; Gargle with warm salt water for sore throat. Most cold symptoms resolve within 7-10 days. Consult a doctor if symptoms worsen or persist beyond 10 days.",
        "fever": "For mild fever (under 102°F): Rest and stay hydrated; Use over-the-counter fever reducers like acetaminophen or ibuprofen; Dress lightly and use cool compresses; Monitor temperature regularly. Seek medical attention if fever exceeds 102°F, persists more than 3 days, or is accompanied by severe symptoms.",
        "default": "Based on your symptoms, here are some general recommendations: Get adequate rest; Stay well-hydrated; Monitor your symptoms; Consider over-the-counter remedies if appropriate. However, if symptoms worsen, persist, or you have concerns, please consult with a healthcare professional for proper evaluation and treatment."
    },
    "serious": {
        "chest": "⚠️ CHEST PAIN requires immediate medical attention. Please contact emergency services (911) or go to the nearest emergency room immediately. Do not delay seeking medical care for chest pain.",
        "breathing": "⚠️ DIFFICULTY BREATHING is a serious symptom. Seek immediate medical attention by calling emergency services (911) or going to the nearest emergency room. This requires urgent evaluation by healthcare professionals.",
        "severe": "⚠️ Based on your symptoms, this appears to require immediate medical attention. Please contact emergency services (911) or go to the nearest emergency room right away. Do not delay seeking professional medical care.",
        "default": "⚠️ Your symptoms suggest you should seek medical attention promptly. Please contact your healthcare provider, urgent care center, or emergency services if symptoms are severe. Professional medical evaluation is recommended."
    }
}

# Conversations storage
CONVERSATIONS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "conversations.json")

def load_conversations():
    """Load existing conversations from JSON file"""
    if os.path.exists(CONVERSATIONS_FILE):
        try:
            with open(CONVERSATIONS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading conversations: {e}")
    return {"conversations": []}

def save_conversation(user_input: str, ai_response: str, severity: str):
    """Save new conversation to JSON file"""
    try:
        data = load_conversations()
        conversation = {
            "user": user_input,
            "response": ai_response,
            "severity": severity,
            "timestamp": datetime.now().isoformat()
        }
        data["conversations"].append(conversation)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(CONVERSATIONS_FILE), exist_ok=True)
        
        with open(CONVERSATIONS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Error saving conversation: {e}")

def get_fallback_response(symptoms: str):
    """Generate fallback response when OpenAI is unavailable"""
    symptoms_lower = symptoms.lower()
    
    # Check for serious symptoms first
    serious_keywords = ["chest pain", "chest", "breathing", "breath", "severe", "emergency", "unconscious", "bleeding heavily"]
    if any(keyword in symptoms_lower for keyword in serious_keywords):
        if "chest" in symptoms_lower:
            return FALLBACK_RESPONSES["serious"]["chest"], "serious"
        elif "breath" in symptoms_lower:
            return FALLBACK_RESPONSES["serious"]["breathing"], "serious"
        else:
            return FALLBACK_RESPONSES["serious"]["severe"], "serious"
    
    # Check for mild symptoms
    if "headache" in symptoms_lower or "head" in symptoms_lower:
        return FALLBACK_RESPONSES["mild"]["headache"], "mild"
    elif "cold" in symptoms_lower or "cough" in symptoms_lower or "runny nose" in symptoms_lower:
        return FALLBACK_RESPONSES["mild"]["cold"], "mild"
    elif "fever" in symptoms_lower and "mild" in symptoms_lower:
        return FALLBACK_RESPONSES["mild"]["fever"], "mild"
    
    # Default responses
    mild_indicators = ["mild", "slight", "little", "minor"]
    if any(indicator in symptoms_lower for indicator in mild_indicators):
        return FALLBACK_RESPONSES["mild"]["default"], "mild"
    else:
        return FALLBACK_RESPONSES["serious"]["default"], "serious"

@app.get("/")
async def root():
    """Root endpoint to verify API is running"""
    return {
        "message": "Healthcare Chatbot API is running",
        "version": "1.0.0",
        "endpoints": ["/diagnose", "/history"],
        "openai_available": client is not None
    }

@app.post("/diagnose", response_model=DiagnosisResponse)
async def diagnose_symptoms(request: SymptomRequest):
    """Main endpoint to process symptoms and return healthcare advice"""
    try:
        ai_response = ""
        severity = "mild"
        
        if client:
            # Try OpenAI API first
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": f"Symptoms: {request.symptoms}"}
                    ],
                    max_tokens=300,
                    temperature=0.7
                )
                
                ai_response = response.choices[0].message.content.strip()
                
                # Determine severity based on keywords in AI response
                serious_keywords = [
                    "doctor", "emergency", "hospital", "serious", "severe", 
                    "immediate", "urgent", "medical attention", "911", "seek care"
                ]
                
                severity = "serious" if any(keyword in ai_response.lower() for keyword in serious_keywords) else "mild"
                
            except Exception as openai_error:
                print(f"OpenAI API error: {openai_error}")
                # Fall back to predefined responses
                ai_response, severity = get_fallback_response(request.symptoms)
        else:
            # Use fallback responses when OpenAI is not available
            ai_response, severity = get_fallback_response(request.symptoms)
        
        # Always add disclaimer
        disclaimer = "\n\n⚠️ Disclaimer: This advice is for informational purposes only and does not replace professional medical consultation. Please consult a qualified healthcare provider for proper diagnosis and treatment."
        ai_response += disclaimer
        
        # Save conversation
        save_conversation(request.symptoms, ai_response, severity)
        
        return DiagnosisResponse(
            advice=ai_response,
            severity=severity,
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        print(f"Error in diagnose_symptoms: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")

@app.get("/history")
async def get_conversation_history():
    """Get all stored conversation history"""
    try:
        return load_conversations()
    except Exception as e:
        print(f"Error getting history: {e}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation history: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "openai_configured": client is not None,
        "conversations_file_exists": os.path.exists(CONVERSATIONS_FILE)
    }

if __name__ == "__main__":
    print("🏥 Healthcare Chatbot Backend Starting...")
    print(f"OpenAI API Available: {client is not None}")
    print(f"Conversations will be stored at: {CONVERSATIONS_FILE}")
    print("\n🌐 Backend will be available at: http://localhost:8000")
    print("🎯 Frontend should connect to: http://localhost:3000\n")
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
