#!/usr/bin/env python3
"""
Auto Chat Prediction Engine
Predicts user responses and conversation patterns
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from core.ollama_service import OllamaService

logger = logging.getLogger(__name__)

class AutoChatPredictor:
    """Prediction engine for auto chat conversations"""
    
    def __init__(self):
        self.ollama_service = OllamaService()
        self.prediction_model = "gemma2:2b"
        self.analysis_model = "qwen2.5:7b"
        
        # Conversation pattern templates
        self.conversation_patterns = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good evening'],
            'question': ['what', 'how', 'why', 'when', 'where', 'who', 'which'],
            'request': ['can you', 'could you', 'would you', 'please', 'help me'],
            'farewell': ['bye', 'goodbye', 'see you', 'talk later', 'have a good'],
            'agreement': ['yes', 'okay', 'sure', 'absolutely', 'definitely'],
            'disagreement': ['no', 'not really', 'i disagree', 'actually', 'but']
        }
    
    async def predict_user_response(self, conversation_history: List[Dict[str, Any]], bot_message: str) -> Dict[str, Any]:
        """Predict likely user responses to bot message"""
        try:
            # Build conversation context
            history_text = self._build_history_text(conversation_history)
            
            prediction_prompt = f"""
            Analyze this conversation and predict the most likely user responses to the bot's latest message.
            
            Conversation History:
            {history_text}
            
            Bot's Latest Message: "{bot_message}"
            
            Predict 3 most likely user responses with probability scores:
            1. Consider the conversation context and flow
            2. Analyze user's communication patterns
            3. Factor in the bot message's tone and content
            
            Respond in JSON format:
            {{
                "predictions": [
                    {{"response": "predicted response 1", "probability": 0.45, "category": "question"}},
                    {{"response": "predicted response 2", "probability": 0.35, "category": "statement"}},
                    {{"response": "predicted response 3", "probability": 0.20, "category": "request"}}
                ],
                "confidence": 0.75,
                "reasoning": "Brief explanation of prediction logic"
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.prediction_model,
                prompt=prediction_prompt,
                temperature=0.3
            )
            
            try:
                predictions = json.loads(response)
                return predictions
            except json.JSONDecodeError:
                # Fallback predictions
                return {
                    "predictions": [
                        {"response": "That's interesting", "probability": 0.4, "category": "statement"},
                        {"response": "Tell me more", "probability": 0.3, "category": "request"},
                        {"response": "I see", "probability": 0.3, "category": "acknowledgment"}
                    ],
                    "confidence": 0.5,
                    "reasoning": "Fallback predictions due to parsing error"
                }
                
        except Exception as e:
            logger.error(f"Error predicting user response: {str(e)}")
            return {"error": str(e), "predictions": []}
    
    async def predict_conversation_direction(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict where the conversation is heading"""
        try:
            if len(conversation_history) < 3:
                return {
                    "direction": "exploration",
                    "confidence": 0.6,
                    "suggested_topics": ["getting to know each other", "interests", "preferences"]
                }
            
            history_text = self._build_history_text(conversation_history)
            
            direction_prompt = f"""
            Analyze this conversation to predict its likely direction and trajectory.
            
            Conversation:
            {history_text}
            
            Predict:
            1. Overall conversation direction (exploration/problem_solving/casual_chat/support/learning)
            2. Likely next topics
            3. Conversation end probability
            4. User engagement trend
            
            Respond in JSON format:
            {{
                "direction": "problem_solving",
                "confidence": 0.8,
                "next_topics": ["specific_solution", "implementation", "follow_up"],
                "end_probability": 0.2,
                "engagement_trend": "increasing",
                "recommended_approach": "provide detailed guidance"
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.analysis_model,
                prompt=direction_prompt,
                temperature=0.3
            )
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "direction": "uncertain",
                    "confidence": 0.5,
                    "next_topics": ["clarification"],
                    "end_probability": 0.3,
                    "engagement_trend": "stable"
                }
                
        except Exception as e:
            logger.error(f"Error predicting conversation direction: {str(e)}")
            return {"error": str(e)}
    
    async def predict_optimal_response_length(self, context: Dict[str, Any]) -> Dict[str, int]:
        """Predict optimal response length based on context"""
        try:
            user_message_length = len(context.get('user_message', ''))
            conversation_depth = context.get('message_count', 1)
            topic_complexity = context.get('complexity_score', 0.5)
            user_engagement = context.get('engagement_level', 0.5)
            
            # Base length calculation
            if user_message_length < 20:
                base_length = 40  # Short response for short input
            elif user_message_length < 100:
                base_length = 80  # Medium response
            else:
                base_length = 120  # Longer response for detailed input
            
            # Adjust for conversation depth
            if conversation_depth > 10:
                base_length += 20  # More detailed in deeper conversations
            
            # Adjust for topic complexity
            complexity_modifier = int(topic_complexity * 50)
            base_length += complexity_modifier
            
            # Adjust for user engagement
            if user_engagement > 0.7:
                base_length += 30  # More detailed for engaged users
            elif user_engagement < 0.3:
                base_length -= 20  # Shorter for disengaged users
            
            # Ensure reasonable bounds
            optimal_length = max(30, min(200, base_length))
            
            return {
                "optimal_min": optimal_length - 20,
                "optimal_max": optimal_length + 20,
                "recommended": optimal_length
            }
            
        except Exception as e:
            logger.error(f"Error predicting response length: {str(e)}")
            return {"optimal_min": 50, "optimal_max": 100, "recommended": 75}
    
    async def predict_user_intent_next(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict user's next likely intent"""
        try:
            # Analyze recent intents
            recent_intents = []
            for msg in conversation_history[-5:]:
                if msg.get('role') == 'user':
                    recent_intents.append(msg.get('intent', 'unknown'))
            
            history_text = self._build_history_text(conversation_history)
            
            intent_prompt = f"""
            Based on this conversation, predict the user's most likely next intent.
            
            Conversation:
            {history_text}
            
            Recent user intents: {recent_intents}
            
            Predict the next intent category and specific intent:
            - Categories: question, request, statement, complaint, compliment, farewell, agreement, disagreement
            - Consider conversation flow and user patterns
            
            Respond in JSON format:
            {{
                "predicted_intent": "question",
                "specific_intent": "asking for clarification",
                "probability": 0.7,
                "alternative_intents": [
                    {{"intent": "request", "probability": 0.2}},
                    {{"intent": "statement", "probability": 0.1}}
                ]
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.prediction_model,
                prompt=intent_prompt,
                temperature=0.3
            )
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "predicted_intent": "statement",
                    "specific_intent": "general response",
                    "probability": 0.5,
                    "alternative_intents": []
                }
                
        except Exception as e:
            logger.error(f"Error predicting user intent: {str(e)}")
            return {"error": str(e)}
    
    async def predict_conversation_satisfaction(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Predict user satisfaction with conversation"""
        try:
            if len(conversation_history) < 2:
                return {"satisfaction": 0.7, "confidence": 0.3, "factors": ["conversation_too_short"]}
            
            history_text = self._build_history_text(conversation_history)
            
            satisfaction_prompt = f"""
            Analyze this conversation to predict user satisfaction level.
            
            Conversation:
            {history_text}
            
            Consider:
            1. Response relevance and helpfulness
            2. Conversation flow and naturalness
            3. Bot's understanding of user needs
            4. User engagement indicators
            5. Problem resolution (if applicable)
            
            Predict satisfaction score (0.0-1.0) and key factors:
            
            Respond in JSON format:
            {{
                "satisfaction": 0.8,
                "confidence": 0.7,
                "factors": ["helpful_responses", "good_understanding", "natural_flow"],
                "areas_for_improvement": ["response_timing", "more_personalization"],
                "overall_assessment": "positive interaction"
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.analysis_model,
                prompt=satisfaction_prompt,
                temperature=0.3
            )
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "satisfaction": 0.6,
                    "confidence": 0.5,
                    "factors": ["standard_interaction"],
                    "areas_for_improvement": ["analysis_error"]
                }
                
        except Exception as e:
            logger.error(f"Error predicting satisfaction: {str(e)}")
            return {"error": str(e)}
    
    def _build_history_text(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Build formatted conversation history text"""
        if not conversation_history:
            return "No previous conversation"
        
        history_lines = []
        for msg in conversation_history[-10:]:  # Last 10 messages
            role = "User" if msg.get('role') == 'user' else "Bot"
            content = msg.get('content', msg.get('message', ''))
            timestamp = msg.get('timestamp', '')
            history_lines.append(f"{role}: {content}")
        
        return "\n".join(history_lines)
    
    def calculate_pattern_match_score(self, text: str, pattern_category: str) -> float:
        """Calculate how well text matches a conversation pattern"""
        try:
            if pattern_category not in self.conversation_patterns:
                return 0.0
            
            text_lower = text.lower()
            patterns = self.conversation_patterns[pattern_category]
            
            matches = sum(1 for pattern in patterns if pattern in text_lower)
            return min(1.0, matches / len(patterns))
            
        except Exception as e:
            logger.error(f"Error calculating pattern match: {str(e)}")
            return 0.0
    
    async def predict_conversation_end_likelihood(self, conversation_history: List[Dict[str, Any]]) -> float:
        """Predict likelihood that conversation is ending"""
        try:
            if not conversation_history:
                return 0.1
            
            recent_messages = conversation_history[-3:]
            
            # Check for farewell patterns
            farewell_indicators = 0
            for msg in recent_messages:
                if msg.get('role') == 'user':
                    text = msg.get('content', msg.get('message', '')).lower()
                    if any(pattern in text for pattern in self.conversation_patterns['farewell']):
                        farewell_indicators += 1
            
            # Check message length trend (declining suggests ending)
            message_lengths = [
                len(msg.get('content', msg.get('message', ''))) 
                for msg in recent_messages 
                if msg.get('role') == 'user'
            ]
            
            length_trend = 0
            if len(message_lengths) >= 2:
                if message_lengths[-1] < message_lengths[0]:
                    length_trend = 0.3
            
            # Base probability
            base_prob = 0.1
            
            # Add farewell indicators
            farewell_prob = farewell_indicators * 0.4
            
            # Conversation length factor (longer conversations more likely to end)
            length_factor = min(0.3, len(conversation_history) * 0.02)
            
            total_probability = base_prob + farewell_prob + length_trend + length_factor
            
            return min(1.0, total_probability)
            
        except Exception as e:
            logger.error(f"Error predicting conversation end: {str(e)}")
            return 0.2