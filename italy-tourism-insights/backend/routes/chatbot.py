"""
Advanced Chatbot API endpoints with multi-language support
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
from chatbot import recommender
from datetime import datetime

router = APIRouter()


class ChatMessage(BaseModel):
    """Chat message request"""
    message: str = Field(..., min_length=1, max_length=1000, description="User message in English or Italian")
    language: Optional[str] = Field(default=None, description="Force language: 'en' or 'it' (auto-detected if not provided)")


class Recommendation(BaseModel):
    """Enhanced recommendation item with links"""
    type: str = Field(..., description="Type: hotel, restaurant, culture")
    icon: str = Field(..., description="Emoji icon")
    name: str = Field(..., description="Name of recommendation")
    details: str = Field(..., description="Price, cuisine type, rating")
    description: str = Field(..., description="Detailed description")
    link: Optional[str] = Field(default=None, description="Website link")
    address: Optional[str] = Field(default=None, description="Physical address")
    hours: Optional[str] = Field(default=None, description="Opening hours")


class ChatResponse(BaseModel):
    """Enhanced chat response with recommendations and metadata"""
    response: str = Field(..., description="AI assistant message")
    recommendations: List[Recommendation] = Field(default=[], description="Relevant recommendations")
    region: Optional[str] = Field(default=None, description="Detected region")
    intent: str = Field(..., description="Detected user intent")
    language: str = Field(..., description="Detected language code")
    message_type: str = Field(..., description="Type: recommendation, greeting, farewell, rejection")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Response timestamp")


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatMessage):
    """
    Chat with the advanced AI tourism assistant
    
    Supports queries in English and Italian:
    - "Recommend hotels in Rome"
    - "Best restaurants in Venice?"
    - "What to see in Florence?"
    - "Mi raccomandi alberghi a Roma?"
    - "Ciao! Come stai?"
    
    Also handles:
    - Greetings (automatic greeting response)
    - Farewell (goodbye response)
    - Multi-turn conversations (context-aware)
    - Rejection of non-tourism topics (polite refusal)
    
    Returns personalized recommendations with:
    - Direct links to official websites
    - Addresses and contact info
    - Prices and ratings
    - Opening hours
    """
    if not request.message or len(request.message.strip()) == 0:
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    if len(request.message) > 1000:
        raise HTTPException(status_code=400, detail="Message too long (max 1000 characters)")
    
    try:
        # Process message through recommender with language preference
        result = recommender.chat(request.message, language_override=request.language)
        
        # Map to response model with enhanced fields
        recommendations = [
            Recommendation(
                type=rec["type"],
                icon=rec["icon"],
                name=rec["name"],
                details=rec["details"],
                description=rec["description"],
                link=rec.get("link"),
                address=rec.get("address"),
                hours=rec.get("hours")
            )
            for rec in result.get("recommendations", [])
        ]
        
        return ChatResponse(
            response=result["response"],
            recommendations=recommendations,
            region=result.get("region"),
            intent=result["intent"],
            language=result.get("language", "en"),
            message_type=result.get("type", "recommendation"),
            timestamp=datetime.utcnow().isoformat()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")


@router.get("/chat/suggestions")
async def get_chat_suggestions():
    """
    Get suggested questions for the chatbot (bilingual)
    
    Returns example prompts to get users started
    """
    return {
        "english_suggestions": [
            "🏨 Where should I stay in Rome?",
            "🍝 Best restaurants in Venice?",
            "🏛️ What cultural sites in Florence?",
            "🚶 Things to do in Milan?",
            "🎨 Museums and galleries?",
            "🍷 Wine tour suggestions?",
            "🎭 Entertainment options?",
            "🛞 Day trips and excursions?"
        ],
        "italian_suggestions": [
            "🏨 Mi raccomandi alberghi a Roma?",
            "🍝 I migliori ristoranti a Venezia?",
            "🏛️ Cosa vedere a Firenze?",
            "🚶 Cosa fare a Milano?",
            "🎨 Musei e gallerie?",
            "🍷 Tour enologici?",
            "🎭 Opzioni di intrattenimento?",
            "🛞 Gite di un giorno?"
        ]
    }


@router.get("/chat/examples")
async def get_chat_examples():
    """
    Get example conversations (bilingual)
    
    Shows what the chatbot can do
    """
    return {
        "english_examples": [
            {
                "user": "I'm visiting Rome for 3 days",
                "intent": "general",
                "response_type": "recommendation",
                "bot_response": "Great! I can help you plan your Roman holiday. I recommend visiting the Colosseum and Vatican Museums, and dining at authentic trattorias."
            },
            {
                "user": "Looking for luxury hotels in Venice",
                "intent": "hotel",
                "response_type": "recommendation",
                "bot_response": "Venice has wonderful luxury options on the Grand Canal! I'm recommending 5-star properties with stunning architecture and city views."
            },
            {
                "user": "What's there to do in Tuscany?",
                "intent": "activity",
                "response_type": "recommendation",
                "bot_response": "Tuscany is wonderful! Beyond Florence's museums, you can enjoy wine tours, Siena's medieval beauty, and countryside villas."
            },
            {
                "user": "Hello!",
                "intent": "greeting",
                "response_type": "greeting",
                "bot_response": "Hello! Welcome to Italy! I'm your AI tourism guide. Where are you planning to go?"
            }
        ],
        "italian_examples": [
            {
                "user": "Sto visitando Firenze per la prima volta",
                "intent": "general",
                "response_type": "recommendation",
                "bot_response": "Che bello! Posso aiutarti a pianificare la tua visita fiorentina. Ti raccomando gli Uffizi e il Duomo, e ristoranti autentici nel centro storico."
            },
            {
                "user": "Cerco ristoranti di alta cucina a Milano",
                "intent": "restaurant",
                "response_type": "recommendation",
                "bot_response": "Milano ha eccellenti opzioni di ristorazione fine dining! Ti consiglio ristoranti con stelle Michelin e viste spettacolari della città."
            },
            {
                "user": "Cosa consigli a Napoli?",
                "intent": "general",
                "response_type": "recommendation",
                "bot_response": "Napoli è incredibile! Ti raccomando la vera pizza napoletana, Pompeii, il Museo Archeologico, e la vista del Vesuvio."
            },
            {
                "user": "Ciao!",
                "intent": "greeting",
                "response_type": "greeting",
                "bot_response": "Ciao! Benvenuto in Italia! Sono la tua guida turistica AI. Dove pensi di andare?"
            }
        ]
    }


@router.get("/chat/conversation-history")
async def get_conversation_history(limit: int = 50):
    """
    Get conversation history for the current session
    
    Returns recent messages and recommendations
    """
    history = recommender.conversation_history[-limit:]
    return {
        "messages": history,
        "total_turns": len(recommender.conversation_history),
        "current_language": recommender.context.language.value,
        "last_region": recommender.context.last_region,
        "last_intent": recommender.context.last_intent
    }
