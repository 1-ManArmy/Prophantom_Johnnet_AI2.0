#!/usr/bin/env python3
"""
Auto Chat Training Module
Continuous learning and model improvement system
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import pickle
import os
from core.ollama_service import OllamaService
from core.database import get_db

logger = logging.getLogger(__name__)

@dataclass
class ConversationFeedback:
    """Represents user feedback on conversation quality"""
    conversation_id: str
    user_id: str
    rating: float  # 1-5 scale
    feedback_type: str  # 'explicit', 'implicit', 'behavioral'
    specific_feedback: Dict[str, Any]
    timestamp: datetime
    context: Dict[str, Any]

@dataclass
class LearningPattern:
    """Represents a learned conversation pattern"""
    pattern_id: str
    pattern_type: str  # 'response', 'intent', 'flow'
    context_conditions: Dict[str, Any]
    success_rate: float
    usage_count: int
    last_updated: datetime
    performance_metrics: Dict[str, float]

class AutoChatTrainer:
    """Training system for auto chat agent"""
    
    def __init__(self):
        self.ollama_service = OllamaService()
        self.training_model = "phi3:14b"
        self.analysis_model = "gemma2:2b"
        
        # Learning storage
        self.learned_patterns = {}
        self.feedback_history = []
        self.performance_metrics = {
            'response_quality': [],
            'user_satisfaction': [],
            'conversation_success': [],
            'engagement_scores': []
        }
        
        # Training configuration
        self.learning_rate = 0.1
        self.pattern_threshold = 0.7
        self.feedback_weight = {
            'explicit': 1.0,
            'implicit': 0.7,
            'behavioral': 0.5
        }
        
        # Load existing patterns
        self._load_learned_patterns()
    
    async def process_conversation_feedback(self, feedback: ConversationFeedback) -> Dict[str, Any]:
        """Process user feedback to improve future responses"""
        try:
            # Store feedback
            self.feedback_history.append(feedback)
            
            # Analyze feedback for patterns
            patterns = await self._extract_learning_patterns(feedback)
            
            # Update learned patterns
            updates = []
            for pattern in patterns:
                update_result = await self._update_pattern(pattern, feedback)
                updates.append(update_result)
            
            # Generate training insights
            insights = await self._generate_training_insights(feedback, patterns)
            
            # Store in database
            await self._store_feedback(feedback)
            
            return {
                'success': True,
                'patterns_updated': len(updates),
                'insights': insights,
                'learning_summary': {
                    'feedback_processed': True,
                    'patterns_learned': len([u for u in updates if u['action'] == 'created']),
                    'patterns_updated': len([u for u in updates if u['action'] == 'updated'])
                }
            }
            
        except Exception as e:
            logger.error(f"Error processing feedback: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def analyze_conversation_performance(self, conversation_id: str) -> Dict[str, Any]:
        """Analyze conversation performance for learning"""
        try:
            # Get conversation data
            conversation_data = await self._get_conversation_data(conversation_id)
            
            if not conversation_data:
                return {'error': 'Conversation not found'}
            
            # Analyze different aspects
            analysis_results = {}
            
            # Response quality analysis
            response_quality = await self._analyze_response_quality(conversation_data)
            analysis_results['response_quality'] = response_quality
            
            # Conversation flow analysis
            flow_analysis = await self._analyze_conversation_flow(conversation_data)
            analysis_results['flow_analysis'] = flow_analysis
            
            # User engagement analysis
            engagement_analysis = await self._analyze_user_engagement(conversation_data)
            analysis_results['engagement'] = engagement_analysis
            
            # Success metrics
            success_metrics = await self._calculate_success_metrics(conversation_data)
            analysis_results['success_metrics'] = success_metrics
            
            # Generate improvement recommendations
            recommendations = await self._generate_improvement_recommendations(analysis_results)
            analysis_results['recommendations'] = recommendations
            
            # Update performance metrics
            self._update_performance_metrics(analysis_results)
            
            return analysis_results
            
        except Exception as e:
            logger.error(f"Error analyzing conversation performance: {str(e)}")
            return {'error': str(e)}
    
    async def train_from_successful_patterns(self) -> Dict[str, Any]:
        """Train the system using successful conversation patterns"""
        try:
            # Get high-performing conversations
            successful_conversations = await self._get_successful_conversations()
            
            if not successful_conversations:
                return {'message': 'No successful conversations found for training'}
            
            # Extract successful patterns
            successful_patterns = []
            for conversation in successful_conversations:
                patterns = await self._extract_successful_patterns(conversation)
                successful_patterns.extend(patterns)
            
            # Analyze pattern commonalities
            pattern_analysis = await self._analyze_pattern_commonalities(successful_patterns)
            
            # Generate training recommendations
            training_recommendations = await self._generate_training_recommendations(pattern_analysis)
            
            # Update system knowledge
            knowledge_updates = await self._update_system_knowledge(training_recommendations)
            
            return {
                'success': True,
                'conversations_analyzed': len(successful_conversations),
                'patterns_extracted': len(successful_patterns),
                'knowledge_updates': knowledge_updates,
                'training_summary': pattern_analysis
            }
            
        except Exception as e:
            logger.error(f"Error in pattern training: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def adaptive_response_training(self, user_id: str, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Adapt responses based on user-specific patterns"""
        try:
            # Get user's conversation history
            user_conversations = await self._get_user_conversations(user_id)
            
            # Analyze user preferences
            user_preferences = await self._analyze_user_preferences(user_conversations)
            
            # Identify successful response patterns for this user
            successful_patterns = await self._identify_user_successful_patterns(user_conversations)
            
            # Generate personalized response strategies
            response_strategies = await self._generate_response_strategies(user_preferences, successful_patterns)
            
            # Create user-specific training data
            training_data = {
                'user_id': user_id,
                'preferences': user_preferences,
                'successful_patterns': successful_patterns,
                'response_strategies': response_strategies,
                'last_updated': datetime.now().isoformat()
            }
            
            # Store user-specific adaptations
            await self._store_user_adaptations(user_id, training_data)
            
            return {
                'success': True,
                'user_adaptations': training_data,
                'strategies_generated': len(response_strategies),
                'patterns_identified': len(successful_patterns)
            }
            
        except Exception as e:
            logger.error(f"Error in adaptive training: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def generate_training_data(self, feedback_threshold: float = 4.0) -> Dict[str, Any]:
        """Generate training data from high-quality conversations"""
        try:
            # Get high-quality conversations
            quality_conversations = await self._get_quality_conversations(feedback_threshold)
            
            training_examples = []
            
            for conversation in quality_conversations:
                # Extract training examples
                examples = await self._extract_training_examples(conversation)
                training_examples.extend(examples)
            
            # Process and format training data
            formatted_data = await self._format_training_data(training_examples)
            
            # Generate training prompts
            training_prompts = await self._generate_training_prompts(formatted_data)
            
            # Save training data
            training_file = await self._save_training_data(formatted_data, training_prompts)
            
            return {
                'success': True,
                'training_examples': len(training_examples),
                'conversations_processed': len(quality_conversations),
                'training_file': training_file,
                'data_summary': {
                    'total_examples': len(training_examples),
                    'quality_threshold': feedback_threshold,
                    'generated_prompts': len(training_prompts)
                }
            }
            
        except Exception as e:
            logger.error(f"Error generating training data: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def _extract_learning_patterns(self, feedback: ConversationFeedback) -> List[LearningPattern]:
        """Extract learning patterns from feedback"""
        patterns = []
        
        try:
            # Analyze the conversation context
            context = feedback.context
            specific_feedback = feedback.specific_feedback
            
            # Generate pattern analysis prompt
            pattern_prompt = f"""
            Analyze this conversation feedback to extract learning patterns:
            
            Rating: {feedback.rating}/5
            Feedback Type: {feedback.feedback_type}
            Specific Feedback: {specific_feedback}
            Context: {context}
            
            Extract patterns that can improve future conversations:
            1. Response patterns that worked well/poorly
            2. Context conditions that led to success/failure
            3. User interaction patterns
            4. Timing and flow patterns
            
            Format as JSON array of patterns:
            [
                {{
                    "pattern_type": "response",
                    "context_conditions": {{"user_intent": "question", "topic": "technical"}},
                    "success_indicator": true,
                    "pattern_description": "detailed technical explanations work well",
                    "confidence": 0.8
                }}
            ]
            """
            
            response = await self.ollama_service.generate(
                model=self.analysis_model,
                prompt=pattern_prompt,
                temperature=0.3
            )
            
            try:
                pattern_data = json.loads(response)
                for pattern_info in pattern_data:
                    pattern = LearningPattern(
                        pattern_id=f"pattern_{datetime.now().timestamp()}",
                        pattern_type=pattern_info.get('pattern_type', 'general'),
                        context_conditions=pattern_info.get('context_conditions', {}),
                        success_rate=0.8 if pattern_info.get('success_indicator') else 0.2,
                        usage_count=1,
                        last_updated=datetime.now(),
                        performance_metrics={'confidence': pattern_info.get('confidence', 0.5)}
                    )
                    patterns.append(pattern)
            except json.JSONDecodeError:
                logger.warning("Could not parse pattern extraction response")
                
        except Exception as e:
            logger.error(f"Error extracting patterns: {str(e)}")
        
        return patterns
    
    async def _update_pattern(self, pattern: LearningPattern, feedback: ConversationFeedback) -> Dict[str, Any]:
        """Update or create a learning pattern"""
        try:
            pattern_key = f"{pattern.pattern_type}_{hash(str(pattern.context_conditions))}"
            
            if pattern_key in self.learned_patterns:
                # Update existing pattern
                existing = self.learned_patterns[pattern_key]
                existing.usage_count += 1
                existing.success_rate = (existing.success_rate * (existing.usage_count - 1) + 
                                       (feedback.rating / 5.0)) / existing.usage_count
                existing.last_updated = datetime.now()
                
                return {'action': 'updated', 'pattern_key': pattern_key}
            else:
                # Create new pattern
                self.learned_patterns[pattern_key] = pattern
                return {'action': 'created', 'pattern_key': pattern_key}
                
        except Exception as e:
            logger.error(f"Error updating pattern: {str(e)}")
            return {'action': 'error', 'error': str(e)}
    
    def _load_learned_patterns(self):
        """Load previously learned patterns from storage"""
        try:
            patterns_file = '/tmp/auto_chat_patterns.pkl'
            if os.path.exists(patterns_file):
                with open(patterns_file, 'rb') as f:
                    self.learned_patterns = pickle.load(f)
                logger.info(f"Loaded {len(self.learned_patterns)} learned patterns")
        except Exception as e:
            logger.error(f"Error loading patterns: {str(e)}")
            self.learned_patterns = {}
    
    def _save_learned_patterns(self):
        """Save learned patterns to storage"""
        try:
            patterns_file = '/tmp/auto_chat_patterns.pkl'
            with open(patterns_file, 'wb') as f:
                pickle.dump(self.learned_patterns, f)
            logger.info(f"Saved {len(self.learned_patterns)} learned patterns")
        except Exception as e:
            logger.error(f"Error saving patterns: {str(e)}")
    
    async def _get_conversation_data(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation data from database"""
        try:
            db = get_db()
            query = """
            SELECT * FROM conversations 
            WHERE id = ? OR user_id = ?
            ORDER BY timestamp DESC
            """
            
            cursor = db.execute(query, (conversation_id, conversation_id))
            rows = cursor.fetchall()
            
            if rows:
                return {
                    'messages': [dict(row) for row in rows],
                    'conversation_id': conversation_id
                }
            return None
            
        except Exception as e:
            logger.error(f"Error getting conversation data: {str(e)}")
            return None
    
    def _update_performance_metrics(self, analysis_results: Dict[str, Any]):
        """Update performance metrics with analysis results"""
        try:
            if 'response_quality' in analysis_results:
                self.performance_metrics['response_quality'].append(
                    analysis_results['response_quality'].get('score', 0.5)
                )
            
            if 'engagement' in analysis_results:
                self.performance_metrics['engagement_scores'].append(
                    analysis_results['engagement'].get('score', 0.5)
                )
            
            # Keep only recent metrics (last 100)
            for metric_key in self.performance_metrics:
                if len(self.performance_metrics[metric_key]) > 100:
                    self.performance_metrics[metric_key] = self.performance_metrics[metric_key][-100:]
                    
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
    
    async def get_learning_summary(self) -> Dict[str, Any]:
        """Get summary of learning progress"""
        try:
            total_patterns = len(self.learned_patterns)
            total_feedback = len(self.feedback_history)
            
            # Calculate average performance
            avg_response_quality = 0
            if self.performance_metrics['response_quality']:
                avg_response_quality = sum(self.performance_metrics['response_quality']) / len(self.performance_metrics['response_quality'])
            
            avg_engagement = 0
            if self.performance_metrics['engagement_scores']:
                avg_engagement = sum(self.performance_metrics['engagement_scores']) / len(self.performance_metrics['engagement_scores'])
            
            # Get recent improvement trend
            recent_quality = self.performance_metrics['response_quality'][-10:] if self.performance_metrics['response_quality'] else []
            quality_trend = 'stable'
            if len(recent_quality) >= 5:
                first_half = sum(recent_quality[:len(recent_quality)//2]) / (len(recent_quality)//2)
                second_half = sum(recent_quality[len(recent_quality)//2:]) / (len(recent_quality) - len(recent_quality)//2)
                if second_half > first_half + 0.1:
                    quality_trend = 'improving'
                elif second_half < first_half - 0.1:
                    quality_trend = 'declining'
            
            return {
                'total_patterns_learned': total_patterns,
                'total_feedback_processed': total_feedback,
                'average_response_quality': round(avg_response_quality, 2),
                'average_engagement': round(avg_engagement, 2),
                'quality_trend': quality_trend,
                'learning_status': 'active' if total_patterns > 0 else 'initial',
                'most_successful_patterns': await self._get_top_patterns(5)
            }
            
        except Exception as e:
            logger.error(f"Error getting learning summary: {str(e)}")
            return {'error': str(e)}
    
    async def _get_top_patterns(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get top performing patterns"""
        try:
            # Sort patterns by success rate
            sorted_patterns = sorted(
                self.learned_patterns.items(),
                key=lambda x: x[1].success_rate,
                reverse=True
            )
            
            top_patterns = []
            for pattern_key, pattern in sorted_patterns[:limit]:
                top_patterns.append({
                    'pattern_type': pattern.pattern_type,
                    'success_rate': round(pattern.success_rate, 2),
                    'usage_count': pattern.usage_count,
                    'context': pattern.context_conditions
                })
            
            return top_patterns
            
        except Exception as e:
            logger.error(f"Error getting top patterns: {str(e)}")
            return []