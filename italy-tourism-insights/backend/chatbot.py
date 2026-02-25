"""
AI Tourism Chatbot powered by Groq API
Uses advanced LLM for genuine, natural conversations
"""
from typing import List, Dict, Optional
import re
import os
from datetime import datetime
from enum import Enum
from groq import Groq
import json


class Language(Enum):
    """Supported languages"""
    ENGLISH = "en"
    ITALIAN = "it"


class ConversationContext:
    """Maintains conversation state for multi-turn conversations"""
    def __init__(self):
        self.language = Language.ENGLISH
        self.last_intent = None
        self.last_region = None
        self.conversation_turn = 0
        self.previous_recommendations = []


class TouristRecommender:
    """
    AI Tourism Recommendation Engine powered by Gemini API
    Provides natural conversations with smart filtering
    """
    
    # Reference data for context (used by Gemini for better recommendations)
    ITALIAN_CITIES = {
        "rome": "Rome - The Eternal City",
        "venice": "Venice - The City of Canals",
        "florence": "Florence - The Renaissance city",
        "milan": "Milan - Fashion capital",
        "naples": "Naples - Southern gem",
        "sicily": "Sicily - Island destination",
        "amalfi": "Amalfi Coast - Stunning coastal region",
        "bologna": "Bologna - Food capital",
        "palermo": "Palermo - Vibrant Sicilian city",
        "verona": "Verona - City of Romeo and Juliet",
    }
    
    def __init__(self):
        """Initialize Groq API and conversation history"""
        self.conversation_history = []
        self.context = ConversationContext()
        
        # Initialize Groq API
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY environment variable not set. Get one from https://console.groq.com")
        
        self.client = Groq(api_key=api_key)
        # Use llama-3.3 model (latest, free tier, very fast, high quality)
        self.model = "llama-3.3-70b-versatile"
    
    def _create_system_prompt(self, language: Language) -> str:
        """Create a smart system prompt for Gemini"""
        
        if language == Language.ITALIAN:
            return """Sei un eccellente assistente turistico IA esperto di TUTTA l'Italia.
Puoi aiutare i visitatori con raccomandazioni per qualsiasi città, regione o destinazione italiana.

FUNZIONI PRINCIPALI:
- Suggerisci hotel, ristoranti, musei, attività in tutta Italia
- Sii genuino, naturale e conversazionale (NON robotico)
- Parla italiano naturale e accogliente
- Rispondi SOLO a domande su turismo in Italia
- Rifiuta politely domande non turistiche

REGIONI ITALIANE:
Nord: Milano, Venezia, Como, Dolomiti, Torino, Bolzano
Centro: Roma, Firenze, Siena, Perugia, Assisi, Pisa
Sud: Napoli, Capri, Costiera Amalfitana, Pompei, Sorrento
Sicilia: Palermo, Messina, Siracusa, Catania
Sardegna: Cagliari, Costa Smeralda, Porto Cervo
E molte altre città e destinazioni!

QUANDO CONSIGLI HOTEL/RISTORANTI/MUSEI:
✓ Fornisci VERI nomi e link a siti ufficiali
✓ Includi prezzi stimati (€)
✓ Spiega PERCHÉ lo consiglio
✓ Usa emoji: 🏨 hotel, 🍝 ristoranti, 🏛️ cultura, 🎭 attività
✓ Fornisci indirizzi specifici e orari
✓ Formatta link come [Nome](https://sito.com)

STILE: Naturale, amichevole, utile - non fornire risposte meccaniche.
Ricorda le preferenze dell'utente. Mostra genuino interesse nel suo viaggio."""
        
        else:  # English
            return """You are an excellent AI tourism assistant for ALL of Italy.
You can help visitors with recommendations for any city, region, or Italian destination.

CORE FUNCTIONS:
- Suggest hotels, restaurants, museums, activities across all of Italy
- Be genuine, natural, and conversational (NOT robotic)
- Speak natural, welcoming English
- Answer ONLY questions about tourism in Italy
- Politely refuse non-tourism questions

ITALIAN REGIONS:
North: Milan, Venice, Lake Como, Dolomites, Turin, Bolzano
Central: Rome, Florence, Siena, Perugia, Assisi, Pisa
South: Naples, Capri, Amalfi Coast, Pompeii, Sorrento
Sicily: Palermo, Messina, Syracuse, Catania
Sardinia: Cagliari, Costa Smeralda, Porto Cervo
And many other cities and destinations!

WHEN RECOMMENDING HOTELS/RESTAURANTS/MUSEUMS:
✓ Provide REAL names and links to official websites
✓ Include estimated prices (€)
✓ Explain WHY you recommend it
✓ Use emojis: 🏨 hotels, 🍝 restaurants, 🏛️ culture, 🎭 activities
✓ Provide specific addresses and hours
✓ Format links as [Name](https://website.com)

STYLE: Natural, friendly, helpful - no mechanical responses.
Remember user preferences. Show genuine interest in their trip."""
    
    def chat(self, user_message: str, language_override: Optional[str] = None) -> Dict:
        """
        Process user message using Groq API and return response with recommendations
        """
        self.context.conversation_turn += 1
        
        # Determine language
        if language_override:
            language = Language.ITALIAN if language_override.lower() == 'it' else Language.ENGLISH
        else:
            language = self.detect_language(user_message)
        
        self.context.language = language
        
        # Create system prompt
        system_prompt = self._create_system_prompt(language)
        
        try:
            # Build messages for Groq (OpenAI-compatible format)
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add recent conversation history (up to 10 exchanges)
            for msg in self.conversation_history[-20:]:
                messages.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "")
                })
            
            # Add current user message
            messages.append({"role": "user", "content": user_message})
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content
            
            # Store in conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message,
                "timestamp": datetime.utcnow().isoformat()
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Parse recommendations from response
            recommendations = self._parse_recommendations(ai_response)
            
            # Detect intent and type
            intent = self._detect_intent(user_message)
            message_type = self._detect_message_type(ai_response, intent)
            region = self._extract_region(user_message)
            
            return {
                "response": ai_response,
                "recommendations": recommendations,
                "region": region,
                "intent": intent,
                "language": language.value,
                "type": message_type
            }
        
        except Exception as e:
            # Fallback response if API fails
            import traceback
            traceback.print_exc()
            error_str = str(e)
            print(f"ERROR in chat(): {error_str}")
            
            # Check for rate limit error
            if "quota" in error_str.lower() or "rate" in error_str.lower() or "429" in error_str:
                if language == Language.ITALIAN:
                    error_response = "Mi dispiace! Hai raggiunto il limite di velocità di Groq. Per favore attendi un momento e riprova."
                else:
                    error_response = "Sorry! You've hit Groq's rate limit. Please wait a moment and try again."
            else:
                error_response = self._get_fallback_response(language, error_str)
            return {
                "response": error_response,
                "recommendations": [],
                "region": None,
                "intent": "error",
                "language": language.value,
                "type": "error"
            }
    
    def _parse_recommendations(self, response_text: str) -> List[Dict]:
        """Extract structured recommendations and links from Gemini's response"""
        import re
        recommendations = []
        
        # Look for markdown links [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', response_text)
        
        # Look for recommendation blocks with emojis
        lines = response_text.split('\n')
        current_rec = None
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Check for recommendation headers
            for emoji, rec_type in [('🏨', 'hotel'), ('🍝', 'restaurant'), ('🏛️', 'culture'), ('🎭', 'activity')]:
                if emoji in stripped:
                    # Save previous if exists
                    if current_rec and current_rec.get('name'):
                        recommendations.append(current_rec)
                    
                    # Extract name
                    name = stripped.replace(emoji, '').replace('**', '').replace('##', '').replace('#', '').strip()
                    if name.endswith(':'):
                        name = name[:-1]
                    
                    current_rec = {
                        "type": rec_type,
                        "icon": emoji,
                        "name": name,
                        "details": "",
                        "description": "",
                        "link": None,
                        "address": None,
                        "hours": None
                    }
                    break
            
            # Extract data for current recommendation
            if current_rec:
                # Extract price
                if '€' in stripped:
                    price_match = re.search(r'€[\d,]+(\s*-\s*€?[\d,]+)?', stripped)
                    if price_match and not current_rec['details']:
                        current_rec['details'] = price_match.group(0)
                
                # Extract address (lines with commas and potential city names)
                if any(city in stripped.lower() for city in ['roma', 'rome', 'venezia', 'venice', 'firenze', 'florence', 'milano', 'milan', 'napoli', 'naples', 'palermo', 'sorrento', 'capri', 'verona', 'bologna', 'siena', 'pisa', 'assisi', 'italy']):
                    if 'http' not in stripped and '€' not in stripped:
                        if not current_rec['address']:
                            current_rec['address'] = stripped.lstrip('*-•').strip()
                
                # Extract links from this line
                line_links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', stripped)
                for link_text, url in line_links:
                    if url.startswith('http') and not current_rec['link']:
                        current_rec['link'] = url
        
        # Add last recommendation
        if current_rec and current_rec.get('name'):
            recommendations.append(current_rec)
        
        # If no structured recommendations found, try to extract from links
        if not recommendations and links:
            for link_text, url in links:
                if url.startswith('http'):
                    recommendations.append({
                        "type": "general",
                        "icon": "🔗",
                        "name": link_text,
                        "details": "",
                        "description": "",
                        "link": url,
                        "address": None,
                        "hours": None
                    })
        
        return recommendations[:6]
    
    def _detect_intent(self, text: str) -> str:
        """Detect user intent"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["hotel", "stay", "sleep", "accommodation", "where to stay", "albergo", "dove dormire", "dove alloggiare"]):
            return "hotel"
        elif any(word in text_lower for word in ["restaurant", "eat", "food", "dining", "where to eat", "ristorante", "dove mangiare", "cosa mangiare"]):
            return "restaurant"
        elif any(word in text_lower for word in ["museum", "art", "cultural", "church", "what to see", "museo", "chiesa", "galleria"]):
            return "culture"
        elif any(word in text_lower for word in ["visit", "see", "tour", "activity", "do", "cosa fare", "attività"]):
            return "activity"
        
        return "general"
    
    def _detect_message_type(self, response: str, intent: str) -> str:
        """Detect type of message (greeting, recommendation, rejection, etc)"""
        response_lower = response.lower()
        
        # Check for rejection/refusal
        if any(phrase in response_lower for phrase in ["sorry", "can only help", "tourism", "dispiace", "solo con", "riguardante il turismo"]):
            if any(phrase in response_lower for phrase in ["only help", "riguardante il turismo", "solo con"]):
                return "rejection"
        
        # Check for greeting response (short response with greeting words)
        if len(response) < 250:
            if any(word in response_lower for word in ["welcome", "hello", "hi", "benvenuto", "ciao", "buongiorno", "pleased"]):
                return "greeting"
        
        # Check if it has recommendations
        if any(emoji in response for emoji in ['🏨', '🍝', '🏛️']):
            return "recommendation"
        
        # Default to recommendation if they asked for something specific
        if intent != "general":
            return "recommendation"
        
        return "recommendation"
    
    def _extract_region(self, text: str) -> Optional[str]:
        """Extract Italian city/region from text"""
        regions = {
            "rome": ["rome", "roma", "lazio"],
            "venice": ["venice", "venezia", "veneto"],
            "florence": ["florence", "firenze", "tuscany", "toscana"],
            "milan": ["milan", "milano", "lombardy"],
            "naples": ["naples", "napoli", "campania"],
        }
        
        text_lower = text.lower()
        for region, keywords in regions.items():
            if any(keyword in text_lower for keyword in keywords):
                return region
        
        return None
    
    def detect_language(self, text: str) -> Language:
        """Detect language from text"""
        text_lower = text.lower()
        
        # Italian-specific characters
        italian_chars = ["è", "à", "ò", "ù", "ì"]
        if any(char in text_lower for char in italian_chars):
            return Language.ITALIAN
        
        # Italian words with word boundaries
        italian_words = ["che", "per", "una", "questo", "quale", "dove", "cosa", "ciao", "buongiorno", "grazie", "vorrei", "posso"]
        if sum(1 for word in italian_words if word in text_lower) >= 2:
            return Language.ITALIAN
        
        return Language.ENGLISH
    
    def _get_fallback_response(self, language: Language, error: str) -> str:
        """Get fallback response if API fails"""
        if language == Language.ITALIAN:
            return "Mi dispiace, ho avuto un problema tecnico. Riprova tra un momento. Se il problema persiste, assicurati che la tua chiave API Groq sia corretta."
        else:
            return "I apologize, I encountered a technical issue. Please try again in a moment. If the problem persists, please ensure your Groq API key is correctly configured."


# Global recommender instance
try:
    recommender = TouristRecommender()
except ValueError as e:
    # API key not set - will show error when trying to use
    recommender = None
    print(f"Warning: {e}")
