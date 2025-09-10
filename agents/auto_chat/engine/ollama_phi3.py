#!/usr/bin/env python3
"""
Auto Chat Ollama Engine
Specialized Ollama integration for automated conversation
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from core.ollama_service import OllamaService

logger = logging.getLogger(__name__)

class AutoChatOllamaEngine:
    """Specialized Ollama engine for auto chat agent"""
    
    def __init__(self):
        self.ollama_service = OllamaService()
        self.primary_model = "phi3:14b"
        self.analysis_model = "gemma2:2b"
        self.creative_model = "qwen2.5:7b"
        
        # Conversation templates
        self.templates = {
            'greeting': "Hello! I'm your auto-chat assistant. How can I help you today?",
            'question_response': "That's an interesting question. Let me think about that...",
            'clarification': "Could you help me understand what you mean by that?",
            'empathy': "I can understand how that might feel.",
            'encouragement': "That sounds like a great approach! Keep going!",
            'wrap_up': "Is there anything else you'd like to discuss?"
        }
    
    async def generate_contextual_response(self, message: str, context: Dict[str, Any]) -> str:
        """Generate response with full context awareness"""
        try:
            system_prompt = """You are an intelligent auto-chat assistant designed to have natural, 
            engaging conversations. You should:
            1. Be contextually aware of the conversation flow
            2. Adapt your personality to match the user's communication style
            3. Provide helpful and relevant responses
            4. Maintain conversation continuity
            5. Show appropriate emotional intelligence
            
            Current conversation context and user preferences are provided."""
            
            conversation_history = context.get('history', [])
            user_preferences = context.get('preferences', {})
            current_mood = context.get('mood', 'neutral')
            
            # Build context string
            history_str = "\n".join([
                f"{'User' if msg['role'] == 'user' else 'Assistant'}: {msg['content']}"
                for msg in conversation_history[-5:]  # Last 5 messages
            ])
            
            prompt = f"""
            System: {system_prompt}
            
            Conversation History:
            {history_str}
            
            User Preferences: {user_preferences}
            Current Mood: {current_mood}
            
            Current Message: {message}
            
            Generate a natural, contextually appropriate response:
            """
            
            response = await self.ollama_service.generate(
                model=self.primary_model,
                prompt=prompt,
                temperature=0.7,
                max_tokens=150
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error in contextual response generation: {str(e)}")
            return "I'm processing your message. Could you give me a moment to respond properly?"
    
    async def analyze_conversation_flow(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze conversation flow and patterns"""
        try:
            if not messages:
                return {'flow': 'new_conversation', 'engagement': 1, 'topics': []}
            
            # Create analysis prompt
            recent_messages = messages[-10:]  # Last 10 messages
            message_text = "\n".join([
                f"{msg['role']}: {msg['content']}" for msg in recent_messages
            ])
            
            analysis_prompt = f"""
            Analyze this conversation for:
            1. Flow quality (smooth/choppy/natural)
            2. Engagement level (1-10)
            3. Main topics discussed
            4. Emotional tone progression
            5. User satisfaction indicators
            
            Conversation:
            {message_text}
            
            Respond in JSON format:
            {{
                "flow": "natural",
                "engagement": 8,
                "topics": ["topic1", "topic2"],
                "emotional_tone": "positive",
                "satisfaction_indicators": ["active_participation", "follow_up_questions"]
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.analysis_model,
                prompt=analysis_prompt,
                temperature=0.3
            )
            
            try:
                import json
                return json.loads(response)
            except:
                return {
                    'flow': 'uncertain',
                    'engagement': 5,
                    'topics': ['general'],
                    'emotional_tone': 'neutral',
                    'satisfaction_indicators': []
                }
                
        except Exception as e:
            logger.error(f"Error analyzing conversation flow: {str(e)}")
            return {'error': str(e)}
    
    async def generate_proactive_message(self, context: Dict[str, Any]) -> str:
        """Generate proactive conversation starter"""
        try:
            user_interests = context.get('interests', [])
            last_topic = context.get('last_topic', 'general')
            time_since_last = context.get('hours_since_last', 0)
            
            prompt = f"""
            Generate a natural, proactive message to re-engage a user in conversation.
            
            User interests: {user_interests}
            Last topic discussed: {last_topic}
            Hours since last interaction: {time_since_last}
            
            The message should:
            1. Feel natural and not pushy
            2. Reference previous conversations if appropriate
            3. Offer something valuable or interesting
            4. Be open-ended to encourage response
            
            Keep it casual and friendly (1-2 sentences).
            """
            
            response = await self.ollama_service.generate(
                model=self.creative_model,
                prompt=prompt,
                temperature=0.8,
                max_tokens=100
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating proactive message: {str(e)}")
            return "Hope you're having a great day! Anything interesting happening?"
    
    async def optimize_response_timing(self, context: Dict[str, Any]) -> float:
        """Calculate optimal response timing based on context"""
        try:
            urgency = context.get('urgency', 3)  # 1-5 scale
            user_patience = context.get('patience_level', 'medium')  # low/medium/high
            conversation_flow = context.get('flow_speed', 'normal')  # slow/normal/fast
            
            # Base timing in seconds
            base_timing = 2.0
            
            # Adjust for urgency
            if urgency >= 4:
                base_timing *= 0.5  # Respond faster for urgent messages
            elif urgency <= 2:
                base_timing *= 1.5  # Can take more time for casual messages
            
            # Adjust for user patience
            patience_multipliers = {'low': 0.7, 'medium': 1.0, 'high': 1.3}
            base_timing *= patience_multipliers.get(user_patience, 1.0)
            
            # Adjust for conversation flow
            flow_multipliers = {'slow': 1.5, 'normal': 1.0, 'fast': 0.8}
            base_timing *= flow_multipliers.get(conversation_flow, 1.0)
            
            # Ensure reasonable bounds
            return max(0.5, min(5.0, base_timing))
            
        except Exception as e:
            logger.error(f"Error optimizing response timing: {str(e)}")
            return 2.0  # Default timing
    
    async def personalize_response_style(self, user_profile: Dict[str, Any], message: str) -> Dict[str, Any]:
        """Personalize response style based on user profile"""
        try:
            communication_style = user_profile.get('communication_style', 'balanced')
            interests = user_profile.get('interests', [])
            formality_preference = user_profile.get('formality', 'casual')
            humor_appreciation = user_profile.get('humor_level', 0.5)
            
            style_config = {
                'temperature': 0.7,
                'max_tokens': 150,
                'personality_traits': {
                    'formality': {'casual': 0.3, 'semi_formal': 0.6, 'formal': 0.9}.get(formality_preference, 0.5),
                    'humor': humor_appreciation,
                    'enthusiasm': user_profile.get('enthusiasm_level', 0.6),
                    'empathy': user_profile.get('empathy_preference', 0.7)
                }
            }
            
            # Adjust based on communication style
            if communication_style == 'concise':
                style_config['max_tokens'] = 80
                style_config['temperature'] = 0.5
            elif communication_style == 'detailed':
                style_config['max_tokens'] = 200
                style_config['temperature'] = 0.8
            elif communication_style == 'creative':
                style_config['temperature'] = 0.9
                style_config['personality_traits']['humor'] += 0.2
            
            return style_config
            
        except Exception as e:
            logger.error(f"Error personalizing response style: {str(e)}")
            return {'temperature': 0.7, 'max_tokens': 150, 'personality_traits': {}}