#!/usr/bin/env python3
"""
Auto Chat Logic Module
Handles intelligent conversation automation and context management
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from core.ollama_service import OllamaService
from core.database import get_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ConversationContext:
    """Represents conversation context for auto chat"""
    user_id: str
    conversation_history: List[Dict[str, Any]]
    current_topic: str
    sentiment_score: float
    engagement_level: int
    last_interaction: datetime
    personality_traits: Dict[str, float]

class AutoChatLogic:
    """Core logic for automated conversation management"""
    
    def __init__(self):
        self.ollama_service = OllamaService()
        self.conversation_contexts = {}
        self.personality_profiles = {
            'friendly': {'warmth': 0.8, 'humor': 0.6, 'formality': 0.3},
            'professional': {'warmth': 0.4, 'humor': 0.2, 'formality': 0.9},
            'casual': {'warmth': 0.7, 'humor': 0.8, 'formality': 0.1},
            'supportive': {'warmth': 0.9, 'humor': 0.4, 'formality': 0.4}
        }
    
    async def process_auto_response(self, user_id: str, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process and generate automatic response"""
        try:
            # Get or create conversation context
            conv_context = self.get_conversation_context(user_id)
            
            # Analyze message sentiment and intent
            analysis = await self.analyze_message(message)
            
            # Update conversation context
            conv_context.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user_message': message,
                'sentiment': analysis['sentiment'],
                'intent': analysis['intent']
            })
            
            # Generate contextual response
            response = await self.generate_response(conv_context, message, analysis)
            
            # Update engagement metrics
            self.update_engagement_metrics(user_id, analysis)
            
            # Store conversation in database
            await self.store_conversation(user_id, message, response, analysis)
            
            return {
                'success': True,
                'response': response,
                'context': {
                    'sentiment': analysis['sentiment'],
                    'engagement_level': conv_context.engagement_level,
                    'topic': conv_context.current_topic
                }
            }
            
        except Exception as e:
            logger.error(f"Error in auto response processing: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': "I'm having trouble processing that right now. Could you try again?"
            }
    
    def get_conversation_context(self, user_id: str) -> ConversationContext:
        """Get or create conversation context for user"""
        if user_id not in self.conversation_contexts:
            self.conversation_contexts[user_id] = ConversationContext(
                user_id=user_id,
                conversation_history=[],
                current_topic="general",
                sentiment_score=0.0,
                engagement_level=1,
                last_interaction=datetime.now(),
                personality_traits=self.personality_profiles['friendly'].copy()
            )
        return self.conversation_contexts[user_id]
    
    async def analyze_message(self, message: str) -> Dict[str, Any]:
        """Analyze message for sentiment, intent, and topic"""
        try:
            analysis_prompt = f"""
            Analyze this message for:
            1. Sentiment (positive/negative/neutral with score -1 to 1)
            2. Intent (question/statement/request/complaint/greeting)
            3. Topic category
            4. Urgency level (1-5)
            
            Message: "{message}"
            
            Respond in JSON format:
            {{
                "sentiment": {{"label": "positive", "score": 0.7}},
                "intent": "question",
                "topic": "technology",
                "urgency": 2,
                "keywords": ["example", "keywords"]
            }}
            """
            
            response = await self.ollama_service.generate(
                model="gemma2:2b",
                prompt=analysis_prompt,
                temperature=0.3
            )
            
            # Parse JSON response
            try:
                analysis = json.loads(response)
                return analysis
            except json.JSONDecodeError:
                # Fallback analysis
                return {
                    "sentiment": {"label": "neutral", "score": 0.0},
                    "intent": "statement",
                    "topic": "general",
                    "urgency": 1,
                    "keywords": []
                }
                
        except Exception as e:
            logger.error(f"Error in message analysis: {str(e)}")
            return {
                "sentiment": {"label": "neutral", "score": 0.0},
                "intent": "statement",
                "topic": "general",
                "urgency": 1,
                "keywords": []
            }
    
    async def generate_response(self, context: ConversationContext, message: str, analysis: Dict[str, Any]) -> str:
        """Generate contextual response based on conversation history"""
        try:
            # Build conversation history for context
            history_context = ""
            if context.conversation_history:
                recent_history = context.conversation_history[-5:]  # Last 5 interactions
                history_context = "\n".join([
                    f"User: {item['user_message']}" 
                    for item in recent_history
                ])
            
            # Determine response style based on personality and analysis
            personality = context.personality_traits
            response_style = self.determine_response_style(personality, analysis)
            
            generation_prompt = f"""
            You are an intelligent auto-chat assistant with the following characteristics:
            - Warmth level: {personality['warmth']}
            - Humor level: {personality['humor']}
            - Formality level: {personality['formality']}
            
            Recent conversation context:
            {history_context}
            
            Current message: "{message}"
            Message sentiment: {analysis['sentiment']['label']} ({analysis['sentiment']['score']})
            Intent: {analysis['intent']}
            Topic: {analysis['topic']}
            
            Response style: {response_style}
            
            Generate an appropriate response that:
            1. Acknowledges the user's message appropriately
            2. Matches the conversation tone and context
            3. Provides helpful and engaging content
            4. Maintains conversation flow
            5. Shows personality based on the traits above
            
            Keep response concise but meaningful (50-150 words).
            """
            
            response = await self.ollama_service.generate(
                model="phi3:14b",
                prompt=generation_prompt,
                temperature=0.7,
                max_tokens=200
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return "I understand what you're saying. Could you tell me more about that?"
    
    def determine_response_style(self, personality: Dict[str, float], analysis: Dict[str, Any]) -> str:
        """Determine appropriate response style"""
        sentiment = analysis['sentiment']['score']
        intent = analysis['intent']
        
        if sentiment < -0.3:
            return "supportive and empathetic"
        elif sentiment > 0.3:
            return "enthusiastic and engaging"
        elif intent == "question":
            return "informative and helpful"
        elif personality['humor'] > 0.6:
            return "friendly with light humor"
        else:
            return "warm and conversational"
    
    def update_engagement_metrics(self, user_id: str, analysis: Dict[str, Any]):
        """Update user engagement metrics"""
        context = self.conversation_contexts[user_id]
        
        # Update engagement based on sentiment and urgency
        sentiment_score = analysis['sentiment']['score']
        urgency = analysis['urgency']
        
        # Boost engagement for positive interactions
        if sentiment_score > 0.2:
            context.engagement_level = min(5, context.engagement_level + 1)
        elif sentiment_score < -0.2:
            context.engagement_level = max(1, context.engagement_level - 1)
        
        # Update current topic
        context.current_topic = analysis['topic']
        context.last_interaction = datetime.now()
    
    async def store_conversation(self, user_id: str, user_message: str, bot_response: str, analysis: Dict[str, Any]):
        """Store conversation in database"""
        try:
            db = get_db()
            
            query = """
            INSERT INTO conversations (user_id, agent_type, user_message, bot_response, 
                                    sentiment_score, intent, topic, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                user_id,
                'auto_chat',
                user_message,
                bot_response,
                analysis['sentiment']['score'],
                analysis['intent'],
                analysis['topic'],
                datetime.now().isoformat()
            )
            
            db.execute(query, params)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing conversation: {str(e)}")
    
    async def get_conversation_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about user's conversation patterns"""
        try:
            context = self.get_conversation_context(user_id)
            
            # Analyze conversation patterns
            total_messages = len(context.conversation_history)
            if total_messages == 0:
                return {'insights': 'No conversation history available'}
            
            # Calculate metrics
            recent_sentiment = [msg.get('sentiment', {}).get('score', 0) 
                             for msg in context.conversation_history[-10:]]
            avg_sentiment = sum(recent_sentiment) / len(recent_sentiment) if recent_sentiment else 0
            
            topics = [msg.get('intent', 'unknown') for msg in context.conversation_history]
            most_common_intent = max(set(topics), key=topics.count) if topics else 'unknown'
            
            return {
                'total_interactions': total_messages,
                'engagement_level': context.engagement_level,
                'average_sentiment': round(avg_sentiment, 2),
                'most_common_intent': most_common_intent,
                'current_topic': context.current_topic,
                'last_interaction': context.last_interaction.isoformat(),
                'personality_match': context.personality_traits
            }
            
        except Exception as e:
            logger.error(f"Error getting insights: {str(e)}")
            return {'error': str(e)}
    
    def cleanup_old_contexts(self, hours: int = 24):
        """Clean up old conversation contexts"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        contexts_to_remove = [
            user_id for user_id, context in self.conversation_contexts.items()
            if context.last_interaction < cutoff_time
        ]
        
        for user_id in contexts_to_remove:
            del self.conversation_contexts[user_id]
        
        logger.info(f"Cleaned up {len(contexts_to_remove)} old conversation contexts")