#!/usr/bin/env python3
"""
Emotional Intelligence And Support Agent Logic Module
Core intelligence and decision-making for emo_ai agent
"""

import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from core.ollama_service import OllamaService
from core.database import get_db

logger = logging.getLogger(__name__)

@dataclass
class EmoAiContext:
    """Context management for emo_ai agent"""
    user_id: str
    session_data: Dict[str, Any]
    interaction_history: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]
    performance_metrics: Dict[str, float]
    last_interaction: datetime

class EmoAiLogic:
    """Core logic for emo_ai agent - Emotional intelligence and support agent"""
    
    def __init__(self):
        self.ollama_service = OllamaService()
        self.primary_model = "phi3:14b"
        self.analysis_model = "gemma2:2b"
        self.creative_model = "mistral:7b"
        self.specialization = "emotional_support"
        self.features = ['emotion_detection', 'empathy_responses', 'mental_health_support']
        
        # Agent-specific configuration
        self.agent_config = {
            'max_context_length': 10,
            'response_temperature': 0.7,
            'analysis_temperature': 0.3,
            'creative_temperature': 0.9,
            'specialization_focus': "emotional_support"
        }
        
        # Context storage
        self.active_contexts = {}
    
    async def process_request(self, user_id: str, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process user request with emotional_support focus"""
        try:
            # Get or create user context
            user_context = self.get_user_context(user_id)
            
            # Analyze request with specialization
            analysis = await self.analyze_request(request, user_context)
            
            # Generate specialized response
            response = await self.generate_specialized_response(request, analysis, user_context)
            
            # Update context and metrics
            self.update_context(user_id, request, response, analysis)
            
            # Store interaction
            await self.store_interaction(user_id, request, response, analysis)
            
            return {
                'success': True,
                'response': response,
                'analysis': analysis,
                'specialization': self.specialization,
                'features_used': self.features,
                'context_updates': user_context.performance_metrics
            }
            
        except Exception as e:
            logger.error(f"Error in {self.specialization} processing: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'response': f"I'm having trouble with {self.specialization} right now. Please try again."
            }
    
    def get_user_context(self, user_id: str) -> EmoAiContext:
        """Get or create user context"""
        if user_id not in self.active_contexts:
            self.active_contexts[user_id] = EmoAiContext(
                user_id=user_id,
                session_data={},
                interaction_history=[],
                user_preferences={},
                performance_metrics={'satisfaction': 0.0, 'engagement': 0.0, 'success_rate': 0.0},
                last_interaction=datetime.now()
            )
        return self.active_contexts[user_id]
    
    async def analyze_request(self, request: str, context: EmoAiContext) -> Dict[str, Any]:
        """Analyze request with emotional_support expertise"""
        try:
            analysis_prompt = f"""
            As a specialist in {self.specialization}, analyze this request:
            
            Request: "{request}"
            
            User Context:
            - Previous interactions: {len(context.interaction_history)}
            - User preferences: {context.user_preferences}
            - Performance metrics: {context.performance_metrics}
            
            Specialization focus: {self.specialization}
            Available features: {self.features}
            
            Provide analysis in JSON format:
            {{
                "intent": "primary intent",
                "complexity": "low/medium/high",
                "specialization_match": 0.8,
                "required_features": ["feature1", "feature2"],
                "user_context_relevance": 0.7,
                "processing_approach": "recommended approach"
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.analysis_model,
                prompt=analysis_prompt,
                temperature=self.agent_config['analysis_temperature']
            )
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "intent": "general_inquiry",
                    "complexity": "medium",
                    "specialization_match": 0.5,
                    "required_features": [],
                    "user_context_relevance": 0.5,
                    "processing_approach": "standard"
                }
                
        except Exception as e:
            logger.error(f"Error in request analysis: {str(e)}")
            return {"error": str(e)}
    
    async def generate_specialized_response(self, request: str, analysis: Dict[str, Any], context: EmoAiContext) -> str:
        """Generate response specialized for emotional_support"""
        try:
            # Build specialized prompt
            specialization_prompt = f"""
            You are an expert AI agent specializing in {self.specialization}.
            
            Your key capabilities:
            {self.features}
            
            User request: "{request}"
            
            Analysis results:
            - Intent: {analysis.get('intent', 'unknown')}
            - Complexity: {analysis.get('complexity', 'medium')}
            - Specialization match: {analysis.get('specialization_match', 0.5)}
            - Required features: {analysis.get('required_features', [])}
            
            User context:
            - Interaction history: {len(context.interaction_history)} previous interactions
            - User preferences: {context.user_preferences}
            - Performance metrics: {context.performance_metrics}
            
            Generate a specialized response that:
            1. Leverages your {self.specialization} expertise
            2. Uses appropriate features from {self.features}
            3. Considers user context and preferences
            4. Provides actionable, valuable insights
            5. Maintains engaging, professional communication
            
            Response should be comprehensive yet concise (100-300 words).
            """
            
            # Select appropriate model based on request complexity
            model = self.primary_model
            temperature = self.agent_config['response_temperature']
            
            if analysis.get('complexity') == 'high':
                model = self.creative_model
                temperature = self.agent_config['creative_temperature']
            elif analysis.get('intent') == 'analysis':
                temperature = self.agent_config['analysis_temperature']
            
            response = await self.ollama_service.generate(
                model=model,
                prompt=specialization_prompt,
                temperature=temperature,
                max_tokens=400
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error generating specialized response: {str(e)}")
            return f"I understand you're looking for help with {self.specialization}. Let me provide some guidance on that."
    
    def update_context(self, user_id: str, request: str, response: str, analysis: Dict[str, Any]):
        """Update user context with interaction data"""
        try:
            context = self.active_contexts[user_id]
            
            # Add to interaction history
            interaction = {
                'timestamp': datetime.now().isoformat(),
                'request': request,
                'response': response,
                'analysis': analysis,
                'specialization': self.specialization
            }
            
            context.interaction_history.append(interaction)
            
            # Keep only recent interactions
            if len(context.interaction_history) > self.agent_config['max_context_length']:
                context.interaction_history = context.interaction_history[-self.agent_config['max_context_length']:]
            
            # Update performance metrics
            specialization_match = analysis.get('specialization_match', 0.5)
            context.performance_metrics['engagement'] = (
                context.performance_metrics['engagement'] * 0.8 + specialization_match * 0.2
            )
            
            context.last_interaction = datetime.now()
            
        except Exception as e:
            logger.error(f"Error updating context: {str(e)}")
    
    async def store_interaction(self, user_id: str, request: str, response: str, analysis: Dict[str, Any]):
        """Store interaction in database"""
        try:
            db = get_db()
            
            query = """
            INSERT INTO conversations (user_id, agent_type, user_message, bot_response, 
                                    analysis_data, specialization, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                user_id,
                'emo_ai',
                request,
                response,
                json.dumps(analysis),
                self.specialization,
                datetime.now().isoformat()
            )
            
            db.execute(query, params)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing interaction: {str(e)}")
    
    async def get_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Get insights about user interactions with this agent"""
        try:
            context = self.get_user_context(user_id)
            
            return {
                'agent_type': 'emo_ai',
                'specialization': self.specialization,
                'total_interactions': len(context.interaction_history),
                'performance_metrics': context.performance_metrics,
                'user_preferences': context.user_preferences,
                'last_interaction': context.last_interaction.isoformat(),
                'specialization_effectiveness': context.performance_metrics.get('engagement', 0.0),
                'features_utilized': self.features
            }
            
        except Exception as e:
            logger.error(f"Error getting user insights: {str(e)}")
            return {'error': str(e)}

    def cleanup_old_contexts(self, hours: int = 24):
        """Clean up old user contexts"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        contexts_to_remove = [
            user_id for user_id, context in self.active_contexts.items()
            if context.last_interaction < cutoff_time
        ]
        
        for user_id in contexts_to_remove:
            del self.active_contexts[user_id]
        
        logger.info(f"Cleaned up {len(contexts_to_remove)} old emo_ai contexts")
