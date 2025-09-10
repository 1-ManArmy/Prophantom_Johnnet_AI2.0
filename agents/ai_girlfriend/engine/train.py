"""
AI Girlfriend Training Engine
Continuous learning from user interactions
"""

import json
from datetime import datetime
from core.database import fetch_all, execute_query
from typing import Dict, List, Any, Optional

class CompanionTrainer:
    """Trains and improves the companion AI based on interactions"""
    
    def __init__(self):
        self.training_data = {
            'successful_responses': [],
            'user_preferences': {},
            'conversation_patterns': {},
            'emotional_responses': {}
        }
    
    def learn_from_interaction(self, user_id: int, user_message: str, 
                             ai_response: str, user_feedback: str = None) -> None:
        """Learn from a single interaction"""
        try:
            interaction_data = {
                'user_id': user_id,
                'user_message': user_message,
                'ai_response': ai_response,
                'timestamp': datetime.now().isoformat(),
                'feedback': user_feedback
            }
            
            # Analyze interaction quality
            quality_score = self._analyze_interaction_quality(user_message, ai_response)
            interaction_data['quality_score'] = quality_score
            
            # Extract learning patterns
            patterns = self._extract_patterns(user_message, ai_response)
            interaction_data['patterns'] = patterns
            
            # Store for future training
            self._store_training_data(interaction_data)
            
        except Exception as e:
            print(f"Error learning from interaction: {e}")
    
    def _analyze_interaction_quality(self, user_message: str, ai_response: str) -> float:
        """Analyze the quality of an interaction"""
        quality_factors = {
            'response_length': self._score_response_length(ai_response),
            'emotional_appropriateness': self._score_emotional_match(user_message, ai_response),
            'engagement_level': self._score_engagement(ai_response),
            'personalization': self._score_personalization(ai_response)
        }
        
        # Weighted average
        weights = {
            'response_length': 0.2,
            'emotional_appropriateness': 0.4,
            'engagement_level': 0.3,
            'personalization': 0.1
        }
        
        total_score = sum(score * weights[factor] for factor, score in quality_factors.items())
        return min(max(total_score, 0.0), 1.0)  # Clamp between 0 and 1
    
    def _score_response_length(self, response: str) -> float:
        """Score response length appropriateness"""
        length = len(response.split())
        
        if 10 <= length <= 50:  # Ideal range
            return 1.0
        elif 5 <= length < 10 or 50 < length <= 80:
            return 0.7
        elif length < 5:
            return 0.3
        else:
            return 0.5
    
    def _score_emotional_match(self, user_message: str, ai_response: str) -> float:
        """Score emotional appropriateness"""
        # Simple emotion detection
        user_emotion = self._detect_emotion(user_message)
        response_tone = self._detect_tone(ai_response)
        
        # Matching logic
        if user_emotion == 'sad' and response_tone in ['supportive', 'comforting']:
            return 1.0
        elif user_emotion == 'happy' and response_tone in ['celebratory', 'enthusiastic']:
            return 1.0
        elif user_emotion == 'neutral' and response_tone in ['friendly', 'casual']:
            return 0.8
        else:
            return 0.5
    
    def _score_engagement(self, response: str) -> float:
        """Score how engaging the response is"""
        engagement_indicators = [
            '?' in response,  # Questions encourage engagement
            '!' in response,  # Excitement/emphasis
            any(emoji in response for emoji in ['😊', '🎉', '💙', '🌟', '✨']),  # Emojis
            any(word in response.lower() for word in ['you', 'your', 'tell me', 'how', 'what'])
        ]
        
        score = sum(engagement_indicators) / len(engagement_indicators)
        return score
    
    def _score_personalization(self, response: str) -> float:
        """Score personalization level"""
        # This would be enhanced with actual user data
        personal_indicators = [
            'remember' in response.lower(),
            'you mentioned' in response.lower(),
            'last time' in response.lower()
        ]
        
        return sum(personal_indicators) / 3.0 if personal_indicators else 0.0
    
    def _detect_emotion(self, message: str) -> str:
        """Simple emotion detection"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['sad', 'upset', 'down', 'hurt']):
            return 'sad'
        elif any(word in message_lower for word in ['happy', 'excited', 'great', 'awesome']):
            return 'happy'
        elif any(word in message_lower for word in ['angry', 'frustrated', 'mad']):
            return 'angry'
        elif any(word in message_lower for word in ['stressed', 'overwhelmed', 'tired']):
            return 'stressed'
        else:
            return 'neutral'
    
    def _detect_tone(self, response: str) -> str:
        """Detect tone of AI response"""
        response_lower = response.lower()
        
        if any(word in response_lower for word in ['sorry', 'understand', 'here for you']):
            return 'supportive'
        elif any(word in response_lower for word in ['amazing', 'fantastic', 'congratulations']):
            return 'celebratory'
        elif '!' in response and any(word in response_lower for word in ['great', 'awesome']):
            return 'enthusiastic'
        else:
            return 'friendly'
    
    def _extract_patterns(self, user_message: str, ai_response: str) -> Dict[str, Any]:
        """Extract patterns from interaction"""
        patterns = {
            'user_message_length': len(user_message.split()),
            'user_emotion': self._detect_emotion(user_message),
            'response_tone': self._detect_tone(ai_response),
            'topics': self._extract_topics(user_message),
            'time_of_day': datetime.now().hour
        }
        
        return patterns
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from message"""
        topic_keywords = {
            'work': ['work', 'job', 'career', 'office'],
            'relationships': ['friend', 'family', 'partner', 'relationship'],
            'health': ['tired', 'sick', 'exercise', 'health'],
            'hobbies': ['hobby', 'fun', 'game', 'music', 'movie']
        }
        
        detected_topics = []
        message_lower = message.lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_topics.append(topic)
        
        return detected_topics
    
    def _store_training_data(self, interaction_data: Dict[str, Any]) -> None:
        """Store training data for future use"""
        try:
            # Store in database for now (could be enhanced with vector storage)
            execute_query(
                '''INSERT INTO conversations (user_id, agent_type, message, response, timestamp) 
                   VALUES (?, ?, ?, ?, ?)''',
                (interaction_data['user_id'], 'ai_girlfriend_training', 
                 json.dumps(interaction_data), '', interaction_data['timestamp'])
            )
            
        except Exception as e:
            print(f"Error storing training data: {e}")
    
    def get_learning_insights(self, user_id: int) -> Dict[str, Any]:
        """Get insights from learning data"""
        try:
            # Get training interactions
            training_data = fetch_all(
                'SELECT message FROM conversations WHERE user_id = ? AND agent_type = ?',
                (user_id, 'ai_girlfriend_training')
            )
            
            insights = {
                'total_interactions': len(training_data),
                'learning_progress': 'active' if training_data else 'none',
                'improvement_areas': self._identify_improvement_areas(training_data)
            }
            
            return insights
            
        except Exception as e:
            print(f"Error getting learning insights: {e}")
            return {}
    
    def _identify_improvement_areas(self, training_data: List) -> List[str]:
        """Identify areas for improvement"""
        # Placeholder for more sophisticated analysis
        areas = []
        
        if len(training_data) < 10:
            areas.append('need_more_interaction_data')
        
        return areas