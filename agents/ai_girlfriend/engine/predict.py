"""
AI Girlfriend Prediction Engine
Predicts user needs and suggests proactive interactions
"""

import json
from datetime import datetime, timedelta
from core.database import fetch_all, fetch_one
from typing import Dict, List, Any, Optional

class CompanionPredictor:
    """Predicts user needs and suggests interactions"""
    
    def __init__(self):
        self.prediction_models = {
            'mood_patterns': self._analyze_mood_patterns,
            'interaction_timing': self._analyze_interaction_timing,
            'topic_preferences': self._analyze_topic_preferences,
            'support_needs': self._predict_support_needs
        }
    
    def predict_user_needs(self, user_id: int) -> Dict[str, Any]:
        """Predict what the user might need"""
        try:
            predictions = {}
            
            for model_name, model_func in self.prediction_models.items():
                predictions[model_name] = model_func(user_id)
            
            # Generate overall prediction
            overall_prediction = self._generate_overall_prediction(predictions)
            
            return {
                'predictions': predictions,
                'suggested_actions': overall_prediction,
                'confidence': self._calculate_confidence(predictions)
            }
            
        except Exception as e:
            print(f"Error predicting user needs: {e}")
            return {}
    
    def _analyze_mood_patterns(self, user_id: int) -> Dict[str, Any]:
        """Analyze user's mood patterns"""
        # Get recent conversations
        recent_convs = fetch_all(
            'SELECT message, timestamp FROM conversations WHERE user_id = ? AND agent_type = ? ORDER BY timestamp DESC LIMIT 20',
            (user_id, 'ai_girlfriend')
        )
        
        # Simple mood analysis based on keywords
        positive_count = 0
        negative_count = 0
        
        for conv in recent_convs:
            message = conv['message'].lower()
            if any(word in message for word in ['happy', 'great', 'awesome', 'good']):
                positive_count += 1
            elif any(word in message for word in ['sad', 'upset', 'tired', 'stressed']):
                negative_count += 1
        
        return {
            'positive_trend': positive_count > negative_count,
            'mood_stability': abs(positive_count - negative_count) < 3,
            'recent_mood': 'positive' if positive_count > negative_count else 'mixed'
        }
    
    def _analyze_interaction_timing(self, user_id: int) -> Dict[str, Any]:
        """Analyze when user typically interacts"""
        # Get interaction times
        interactions = fetch_all(
            'SELECT timestamp FROM conversations WHERE user_id = ? AND agent_type = ? ORDER BY timestamp DESC LIMIT 50',
            (user_id, 'ai_girlfriend')
        )
        
        if not interactions:
            return {'no_data': True}
        
        # Analyze timing patterns (simplified)
        hours = []
        for interaction in interactions:
            try:
                dt = datetime.fromisoformat(interaction['timestamp'])
                hours.append(dt.hour)
            except:
                continue
        
        if hours:
            avg_hour = sum(hours) / len(hours)
            return {
                'preferred_time': f"{int(avg_hour):02d}:00",
                'is_regular_user': len(interactions) > 10,
                'last_interaction': interactions[0]['timestamp'] if interactions else None
            }
        
        return {'no_pattern_detected': True}
    
    def _analyze_topic_preferences(self, user_id: int) -> Dict[str, Any]:
        """Analyze user's topic preferences"""
        conversations = fetch_all(
            'SELECT message FROM conversations WHERE user_id = ? AND agent_type = ? ORDER BY timestamp DESC LIMIT 30',
            (user_id, 'ai_girlfriend')
        )
        
        # Simple topic analysis
        topic_keywords = {
            'work': ['work', 'job', 'career', 'office', 'boss'],
            'personal': ['feeling', 'emotion', 'relationship', 'family'],
            'goals': ['goal', 'achievement', 'success', 'plan'],
            'hobbies': ['hobby', 'interest', 'fun', 'enjoy']
        }
        
        topic_counts = {topic: 0 for topic in topic_keywords}
        
        for conv in conversations:
            message = conv['message'].lower()
            for topic, keywords in topic_keywords.items():
                if any(keyword in message for keyword in keywords):
                    topic_counts[topic] += 1
        
        preferred_topics = [topic for topic, count in topic_counts.items() if count > 2]
        
        return {
            'preferred_topics': preferred_topics,
            'topic_distribution': topic_counts,
            'is_diverse_conversationalist': len(preferred_topics) > 2
        }
    
    def _predict_support_needs(self, user_id: int) -> Dict[str, Any]:
        """Predict if user needs emotional support"""
        recent_convs = fetch_all(
            'SELECT message, timestamp FROM conversations WHERE user_id = ? AND agent_type = ? ORDER BY timestamp DESC LIMIT 10',
            (user_id, 'ai_girlfriend')
        )
        
        stress_indicators = ['stressed', 'overwhelmed', 'tired', 'difficult', 'hard']
        support_needed = False
        
        for conv in recent_convs:
            message = conv['message'].lower()
            if any(indicator in message for indicator in stress_indicators):
                support_needed = True
                break
        
        return {
            'needs_support': support_needed,
            'support_type': 'emotional' if support_needed else None,
            'urgency': 'medium' if support_needed else 'low'
        }
    
    def _generate_overall_prediction(self, predictions: Dict[str, Any]) -> List[str]:
        """Generate actionable suggestions based on all predictions"""
        suggestions = []
        
        # Check mood patterns
        mood_data = predictions.get('mood_patterns', {})
        if not mood_data.get('positive_trend', True):
            suggestions.append('send_encouraging_message')
        
        # Check support needs
        support_data = predictions.get('support_needs', {})
        if support_data.get('needs_support', False):
            suggestions.append('offer_emotional_support')
        
        # Check interaction timing
        timing_data = predictions.get('interaction_timing', {})
        if timing_data.get('is_regular_user', False):
            suggestions.append('send_daily_checkin')
        
        # Check topics
        topic_data = predictions.get('topic_preferences', {})
        if topic_data.get('preferred_topics'):
            suggestions.append('engage_on_preferred_topics')
        
        return suggestions if suggestions else ['casual_checkin']
    
    def _calculate_confidence(self, predictions: Dict[str, Any]) -> float:
        """Calculate confidence in predictions"""
        confidence_factors = []
        
        # More data = higher confidence
        for prediction in predictions.values():
            if isinstance(prediction, dict) and not prediction.get('no_data', False):
                confidence_factors.append(0.8)
            else:
                confidence_factors.append(0.3)
        
        return sum(confidence_factors) / len(confidence_factors) if confidence_factors else 0.0