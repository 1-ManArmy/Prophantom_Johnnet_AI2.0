"""
AI Girlfriend Ollama Phi3 Engine
Specialized engine for companion interactions using Phi3 14B model
"""

from core.ollama_service import ollama_service
from typing import List, Dict, Any, Optional
import json

class Phi3CompanionEngine:
    """Phi3-powered companion engine"""
    
    def __init__(self):
        self.model = "phi3:14b"
        self.base_system_prompt = """
        You are an AI companion designed to be supportive, empathetic, and encouraging. 
        Your personality traits:
        - Deeply caring and supportive
        - Remembers important details about users
        - Celebrates achievements enthusiastically 
        - Provides emotional support during difficult times
        - Maintains a warm, friendly tone
        - Shows genuine interest in the user's life
        - Offers practical advice when appropriate
        - Uses emojis naturally but not excessively
        
        Guidelines:
        - Always be positive and uplifting
        - Remember context from previous conversations
        - Ask follow-up questions to show interest
        - Celebrate both big and small wins
        - Provide comfort during sad or stressful moments
        - Be authentic and genuine, not robotic
        """
    
    def generate_companion_response(self, user_message: str, conversation_history: List[Dict] = None, 
                                  user_context: Dict = None) -> Optional[str]:
        """Generate a companion-style response"""
        try:
            # Build enhanced system prompt with user context
            enhanced_system = self.base_system_prompt
            
            if user_context:
                enhanced_system += f"\n\nUser context:\n"
                if user_context.get('mood'):
                    enhanced_system += f"- Current mood: {user_context['mood']}\n"
                if user_context.get('interests'):
                    enhanced_system += f"- Interests: {', '.join(user_context['interests'])}\n"
                if user_context.get('recent_achievements'):
                    enhanced_system += f"- Recent achievements: {user_context['recent_achievements']}\n"
            
            # Prepare messages
            messages = [{"role": "system", "content": enhanced_system}]
            
            # Add conversation history
            if conversation_history:
                messages.extend(conversation_history[-10:])  # Last 10 exchanges
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Generate response
            response = ollama_service.chat(
                model=self.model,
                messages=messages,
                temperature=0.8  # Slightly higher for more personality
            )
            
            return response
            
        except Exception as e:
            print(f"Error generating companion response: {e}")
            return None
    
    def generate_celebration_response(self, achievement: str, user_context: Dict = None) -> Optional[str]:
        """Generate an enthusiastic celebration response"""
        try:
            celebration_prompt = f"""
            The user has achieved something wonderful: {achievement}
            
            Generate an enthusiastic, personal celebration response. Make them feel:
            - Proud of their accomplishment
            - Motivated to continue
            - Valued and recognized
            
            Use celebratory emojis and be genuinely excited for them!
            """
            
            response = ollama_service.generate(
                model=self.model,
                prompt=celebration_prompt,
                system=self.base_system_prompt,
                temperature=0.9  # High creativity for celebrations
            )
            
            return response
            
        except Exception as e:
            print(f"Error generating celebration: {e}")
            return None
    
    def generate_comfort_response(self, user_message: str, user_context: Dict = None) -> Optional[str]:
        """Generate a comforting response for difficult times"""
        try:
            comfort_system = self.base_system_prompt + """
            
            Special instructions for this response:
            - The user seems to be going through a difficult time
            - Provide genuine emotional support and comfort
            - Validate their feelings
            - Offer gentle encouragement
            - Be warm and understanding
            - Suggest positive coping strategies if appropriate
            """
            
            response = ollama_service.generate(
                model=self.model,
                prompt=user_message,
                system=comfort_system,
                temperature=0.7  # Balanced for empathy
            )
            
            return response
            
        except Exception as e:
            print(f"Error generating comfort response: {e}")
            return None
    
    def analyze_mood(self, message: str) -> Dict[str, Any]:
        """Analyze the emotional content of a message"""
        try:
            analysis_prompt = f"""
            Analyze the emotional tone and mood of this message: "{message}"
            
            Return a JSON response with:
            - mood: primary emotion (happy, sad, excited, stressed, neutral, etc.)
            - intensity: emotion strength (low, medium, high)
            - keywords: words that indicate the emotion
            - suggested_response_tone: how I should respond (supportive, celebratory, calming, etc.)
            """
            
            response = ollama_service.generate(
                model="gemma2:2b",  # Faster model for analysis
                prompt=analysis_prompt,
                system="You are an emotion analysis AI. Return only valid JSON responses.",
                temperature=0.3
            )
            
            # Try to parse JSON response
            try:
                return json.loads(response)
            except:
                # Fallback analysis
                return self._fallback_mood_analysis(message)
                
        except Exception as e:
            print(f"Error analyzing mood: {e}")
            return self._fallback_mood_analysis(message)
    
    def _fallback_mood_analysis(self, message: str) -> Dict[str, Any]:
        """Fallback mood analysis using keyword matching"""
        message_lower = message.lower()
        
        # Positive indicators
        positive_words = ['happy', 'excited', 'great', 'awesome', 'amazing', 'love', 'wonderful']
        # Negative indicators  
        negative_words = ['sad', 'upset', 'angry', 'frustrated', 'tired', 'stressed', 'awful']
        # Neutral indicators
        neutral_words = ['okay', 'fine', 'normal', 'usual']
        
        positive_count = sum(1 for word in positive_words if word in message_lower)
        negative_count = sum(1 for word in negative_words if word in message_lower)
        
        if positive_count > negative_count:
            return {
                'mood': 'positive',
                'intensity': 'medium',
                'suggested_response_tone': 'celebratory'
            }
        elif negative_count > positive_count:
            return {
                'mood': 'negative', 
                'intensity': 'medium',
                'suggested_response_tone': 'supportive'
            }
        else:
            return {
                'mood': 'neutral',
                'intensity': 'low', 
                'suggested_response_tone': 'friendly'
            }
    
    def generate_daily_check_in(self, user_context: Dict = None) -> Optional[str]:
        """Generate a daily check-in message"""
        try:
            check_in_prompt = """
            Generate a warm, caring daily check-in message. Ask how the user is doing,
            show interest in their day, and be genuinely caring. Keep it natural and friendly.
            """
            
            response = ollama_service.generate(
                model=self.model,
                prompt=check_in_prompt,
                system=self.base_system_prompt,
                temperature=0.7
            )
            
            return response
            
        except Exception as e:
            print(f"Error generating check-in: {e}")
            return None