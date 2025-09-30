# backend/ai_model.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User
import requests
import os
from typing import Dict, List
import json

router = APIRouter(prefix="/ai", tags=["ai_model"])

# Configuration for your custom model
CUSTOM_MODEL_URL = os.getenv("CUSTOM_MODEL_URL", "https://your-model-endpoint.com/api/predict")
CUSTOM_MODEL_API_KEY = os.getenv("CUSTOM_MODEL_API_KEY", "your-api-key-here")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health context for your model
HEALTH_CONTEXT = """
You are a helpful AI health assistant. You provide general health information, 
wellness tips, and answer health-related questions. However, you always include 
important disclaimers:

IMPORTANT: I am an AI assistant and cannot provide medical diagnosis, 
treatment recommendations, or emergency advice. Please consult with qualified 
healthcare professionals for medical concerns. In case of emergency, 
contact your local emergency services immediately.

When responding:
1. Be empathetic and supportive
2. Provide general wellness information
3. Suggest consulting healthcare professionals for specific medical concerns
4. Never diagnose conditions or recommend specific treatments
5. Encourage healthy lifestyle choices
6. Be clear about your limitations as an AI
"""

@router.post("/chat")
async def chat_with_ai(
    message: str,
    conversation_history: List[Dict] = None,
    db: Session = Depends(get_db)
):
    """
    Chat endpoint that connects to your custom hosted AI model
    """
    try:
        # Prepare the payload for your custom model
        # Adjust this structure based on your model's expected input format
        payload = {
            "message": message,
            "conversation_history": conversation_history[-6:] if conversation_history else [],
            "system_prompt": HEALTH_CONTEXT,
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        # Call your custom model API
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CUSTOM_MODEL_API_KEY}"
        }
        
        response = requests.post(
            CUSTOM_MODEL_URL,
            headers=headers,
            json=payload,
            timeout=30  # 30 second timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract the response based on your model's output format
            # Adjust these field names based on your model's response structure
            ai_response = data.get("response") or data.get("answer") or data.get("output")
            
            if not ai_response:
                raise ValueError("No response found in model output")
                
            return {
                "response": ai_response,
                "conversation_id": data.get("conversation_id"),
                "timestamp": data.get("timestamp")
            }
        else:
            # Handle API errors
            error_detail = f"Model API returned status {response.status_code}"
            try:
                error_data = response.json()
                error_detail = error_data.get('error', error_detail)
            except:
                pass
                
            raise HTTPException(
                status_code=response.status_code,
                detail=error_detail
            )
            
    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=408,
            detail="Model request timeout - please try again"
        )
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to AI model service"
        )
    except Exception as e:
        # Fallback response if AI service is unavailable
        print(f"AI Service Error: {e}")
        return {
            "response": f"I understand you're asking about health-related matters. Currently, I'm experiencing technical difficulties. For immediate health concerns, please consult with a healthcare professional. You can try again shortly. (Error: {str(e)})",
            "error": "AI service temporarily unavailable",
            "timestamp": "2024-01-01T00:00:00Z"
        }

# Alternative: If your model uses a different endpoint structure
@router.post("/chat/custom")
async def chat_with_custom_model(
    message: str,
    conversation_history: List[Dict] = None,
    db: Session = Depends(get_db)
):
    """
    Alternative endpoint for models with different API structures
    """
    try:
        # Build conversation context
        messages = []
        
        # Add system message
        messages.append({"role": "system", "content": HEALTH_CONTEXT})
        
        # Add conversation history
        if conversation_history:
            for msg in conversation_history[-6:]:
                messages.append(msg)
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Custom payload - adjust based on your model's requirements
        payload = {
            "messages": messages,
            "max_tokens": 500,
            "temperature": 0.7
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CUSTOM_MODEL_API_KEY}"
        }
        
        response = requests.post(
            CUSTOM_MODEL_URL,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract response - adjust based on your model's output format
            # Common patterns:
            choices = data.get("choices", [{}])
            if choices:
                ai_response = choices[0].get("message", {}).get("content")
            else:
                ai_response = data.get("text") or data.get("generated_text")
            
            if not ai_response:
                ai_response = "I received your message but couldn't generate a proper response."
                
            return {
                "response": ai_response,
                "conversation_id": data.get("id"),
                "timestamp": data.get("created")
            }
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Model API error: {response.text}"
            )
            
    except Exception as e:
        print(f"Custom model error: {e}")
        return {
            "response": "I'm having trouble connecting to my AI capabilities right now. Please try again in a moment.",
            "error": str(e),
            "timestamp": "2024-01-01T00:00:00Z"
        }

# Mock endpoint for testing without a real model
@router.post("/chat/mock")
async def chat_with_mock_model(
    message: str,
    conversation_history: List[Dict] = None,
    db: Session = Depends(get_db)
):
    """
    Mock endpoint for testing without a real AI model
    """
    # Simple mock responses based on keywords
    message_lower = message.lower()
    
    if any(word in message_lower for word in ["hello", "hi", "hey"]):
        response = "Hello! I'm your Health AI assistant. How can I help you with your health and wellness questions today?"
    elif any(word in message_lower for word in ["headache", "pain"]):
        response = "I understand you're asking about headaches. While I can provide general information about common headache types, it's important to consult with a healthcare professional for proper diagnosis and treatment, especially if the pain is severe or persistent."
    elif any(word in message_lower for word in ["sleep", "tired"]):
        response = "Sleep is crucial for overall health. Most adults need 7-9 hours of quality sleep per night. Good sleep hygiene includes maintaining a consistent schedule, creating a restful environment, and avoiding screens before bedtime. If you're experiencing ongoing sleep issues, consider discussing them with a healthcare provider."
    elif any(word in message_lower for word in ["diet", "nutrition", "eat"]):
        response = "A balanced diet with plenty of fruits, vegetables, lean proteins, and whole grains supports overall health. Remember to stay hydrated and practice portion control. For personalized nutrition advice, a registered dietitian can provide guidance tailored to your specific needs."
    else:
        response = f"Thank you for your message about '{message}'. As a health AI assistant, I focus on providing general wellness information and encouraging healthy lifestyle choices. For specific medical concerns, please consult with qualified healthcare professionals who can provide personalized advice based on your complete health history."
    
    return {
        "response": response,
        "conversation_id": "mock_conversation_123",
        "timestamp": "2024-01-01T00:00:00Z"
    }

@router.get("/health-check")
async def ai_health_check():
    """Check if AI services are available"""
    try:
        # Test connection to your custom model
        test_payload = {
            "message": "Test connection",
            "max_tokens": 10
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {CUSTOM_MODEL_API_KEY}"
        }
        
        response = requests.post(
            CUSTOM_MODEL_URL,
            headers=headers,
            json=test_payload,
            timeout=10
        )
        
        if response.status_code == 200:
            return {"status": "healthy", "ai_service": "responsive"}
        else:
            return {"status": "degraded", "ai_service": "responding_with_errors"}
            
    except Exception as e:
        return {"status": "unavailable", "ai_service": "offline", "error": str(e)}