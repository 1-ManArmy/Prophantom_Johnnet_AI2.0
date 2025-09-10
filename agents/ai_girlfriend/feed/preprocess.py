"""
AI Girlfriend Data Preprocessor
Processes and enhances data for better companion interactions
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple

class CompanionDataProcessor:
    """Processes data to enhance companion AI responses"""
    
    def __init__(self):
        self.emotion_keywords = {
            'joy': ['happy', 'excited', 'thrilled', 'delighted', 'cheerful', 'elated'],
            'sadness': ['sad', 'upset', 'depressed', 'down', 'melancholy', 'heartbroken'],
            'anger': ['angry', 'frustrated', 'annoyed', 'irritated', 'furious', 'mad'],
            'fear': ['scared', 'afraid', 'anxious', 'worried', 'nervous', 'terrified'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'stunned'],
            'love': ['love', 'adore', 'cherish', 'affection', 'care', 'devoted'],
            'stress': ['stressed', 'overwhelmed', 'pressured', 'tense', 'burned out']
        }
        
        self.topic_extractors = {
            'work': r'\b(work|job|career|office|boss|colleague|meeting|project|deadline)\b',
            'relationships': r'\b(friend|family|partner|relationship|date|marriage|love)\b',
            'health': r'\b(health|doctor|exercise|gym|diet|sleep|tired|sick)\b',
            'hobbies': r'\b(hobby|music|movie|book|game|sport|art|cooking|travel)\b',
            'goals': r'\b(goal|dream|plan|future|ambition|hope|wish|want)\b',
            'education': r'\b(school|study|learn|course|degree|exam|class)\b'
        }
    
    def process_user_message(self, message: str, user_context: Dict = None) -> Dict[str, Any]:
        """Process user message to extract insights"""
        processed = {
            'original_message': message,
            'emotions': self._extract_emotions(message),
            'topics': self._extract_topics(message),
            'sentiment': self._analyze_sentiment(message),
            'urgency': self._assess_urgency(message),
            'support_needed': self._detect_support_need(message),
            'personal_references': self._extract_personal_references(message),
            'questions': self._extract_questions(message),
            'achievements': self._detect_achievements(message),
            'processed_at': datetime.now().isoformat()
        }
        
        # Add context-aware processing
        if user_context:
            processed['contextual_insights'] = self._analyze_with_context(processed, user_context)
        
        return processed
    
    def _extract_emotions(self, message: str) -> Dict[str, float]:
        """Extract emotional content from message"""
        message_lower = message.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0.0
            for keyword in keywords:
                if keyword in message_lower:
                    # Weight by keyword strength and frequency
                    occurrences = message_lower.count(keyword)
                    score += occurrences * self._get_keyword_weight(keyword)
            
            # Normalize score
            emotion_scores[emotion] = min(score, 1.0)
        
        # Find dominant emotion
        dominant_emotion = max(emotion_scores.items(), key=lambda x: x[1])
        
        return {
            'scores': emotion_scores,
            'dominant': dominant_emotion[0] if dominant_emotion[1] > 0.1 else 'neutral',
            'intensity': dominant_emotion[1]
        }
    
    def _extract_topics(self, message: str) -> List[str]:
        """Extract topics from message using regex patterns"""
        detected_topics = []
        message_lower = message.lower()
        
        for topic, pattern in self.topic_extractors.items():
            if re.search(pattern, message_lower, re.IGNORECASE):
                detected_topics.append(topic)
        
        return detected_topics
    
    def _analyze_sentiment(self, message: str) -> Dict[str, Any]:
        """Analyze overall sentiment of message"""
        positive_words = ['good', 'great', 'awesome', 'amazing', 'wonderful', 'fantastic', 'excellent', 'perfect', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'dislike', 'worst', 'failed', 'wrong', 'problem']
        
        message_words = message.lower().split()
        
        positive_count = sum(1 for word in message_words if word in positive_words)
        negative_count = sum(1 for word in message_words if word in negative_words)
        
        if positive_count > negative_count:
            polarity = 'positive'
            confidence = (positive_count - negative_count) / len(message_words)
        elif negative_count > positive_count:
            polarity = 'negative'  
            confidence = (negative_count - positive_count) / len(message_words)
        else:
            polarity = 'neutral'
            confidence = 0.5
        
        return {
            'polarity': polarity,
            'confidence': min(confidence * 2, 1.0),  # Scale up confidence
            'positive_words': positive_count,
            'negative_words': negative_count
        }
    
    def _assess_urgency(self, message: str) -> str:
        """Assess urgency level of message"""
        high_urgency_indicators = ['urgent', 'emergency', 'help', 'crisis', 'immediately', 'asap', 'now']
        medium_urgency_indicators = ['soon', 'quickly', 'important', 'need to', 'should']
        
        message_lower = message.lower()
        
        if any(indicator in message_lower for indicator in high_urgency_indicators):
            return 'high'
        elif any(indicator in message_lower for indicator in medium_urgency_indicators):
            return 'medium'
        else:
            return 'low'
    
    def _detect_support_need(self, message: str) -> Dict[str, Any]:
        """Detect if user needs emotional support"""
        support_indicators = {
            'emotional': ['sad', 'depressed', 'upset', 'crying', 'hurt', 'lonely', 'heartbroken'],
            'practical': ['help', 'advice', 'suggestion', 'what should i', 'how do i'],
            'validation': ['am i', 'do you think', 'is it normal', 'should i feel'],
            'comfort': ['scared', 'worried', 'anxious', 'nervous', 'overwhelmed']
        }
        
        message_lower = message.lower()
        support_types = []
        
        for support_type, indicators in support_indicators.items():
            if any(indicator in message_lower for indicator in indicators):
                support_types.append(support_type)
        
        return {
            'needed': len(support_types) > 0,
            'types': support_types,
            'priority': 'high' if 'emotional' in support_types else 'medium' if support_types else 'low'
        }
    
    def _extract_personal_references(self, message: str) -> List[str]:
        """Extract personal references and names"""
        # Simple extraction of potential names and personal references
        personal_patterns = [
            r'\bmy ([a-zA-Z]+)\b',  # my friend, my mom, etc.
            r'\b([A-Z][a-z]+) (said|told|asked)\b',  # Names followed by verbs
            r'\bwith ([A-Z][a-z]+)\b'  # with Name
        ]
        
        references = []
        for pattern in personal_patterns:
            matches = re.findall(pattern, message)
            references.extend(matches)
        
        return list(set(references))  # Remove duplicates
    
    def _extract_questions(self, message: str) -> List[str]:
        """Extract questions from message"""
        # Split by sentence and filter questions
        sentences = re.split(r'[.!?]+', message)
        questions = [s.strip() + '?' for s in sentences if '?' in s or s.strip().lower().startswith(('what', 'how', 'why', 'when', 'where', 'who', 'can', 'should', 'would', 'do you'))]
        
        return questions
    
    def _detect_achievements(self, message: str) -> Dict[str, Any]:
        """Detect achievements or accomplishments mentioned"""
        achievement_indicators = [
            'accomplished', 'achieved', 'completed', 'finished', 'succeeded', 'won', 
            'got promoted', 'graduated', 'passed', 'earned', 'received', 'got the job'
        ]
        
        message_lower = message.lower()
        detected_achievements = []
        
        for indicator in achievement_indicators:
            if indicator in message_lower:
                detected_achievements.append(indicator)
        
        return {
            'has_achievement': len(detected_achievements) > 0,
            'indicators': detected_achievements,
            'celebration_worthy': len(detected_achievements) > 0
        }
    
    def _get_keyword_weight(self, keyword: str) -> float:
        """Get weight for emotional keywords"""
        # Strong emotional words get higher weights
        strong_words = ['thrilled', 'devastated', 'furious', 'terrified', 'elated', 'heartbroken']
        medium_words = ['happy', 'sad', 'angry', 'scared', 'excited']
        
        if keyword in strong_words:
            return 1.0
        elif keyword in medium_words:
            return 0.7
        else:
            return 0.5
    
    def _analyze_with_context(self, processed_message: Dict, user_context: Dict) -> Dict[str, Any]:
        """Analyze message with user context for better insights"""
        insights = {}
        
        # Compare with user's typical emotional patterns
        if 'mood_history' in user_context:
            current_emotion = processed_message['emotions']['dominant']
            insights['emotion_change'] = self._compare_with_history(current_emotion, user_context['mood_history'])
        
        # Check against user preferences
        if 'interests' in user_context:
            topic_match = any(topic in user_context['interests'] for topic in processed_message['topics'])
            insights['topic_relevance'] = 'high' if topic_match else 'medium'
        
        # Relationship building opportunities
        if processed_message['personal_references']:
            insights['relationship_building'] = 'high'  # Remember these references
        
        return insights
    
    def _compare_with_history(self, current_emotion: str, mood_history: List) -> str:
        """Compare current emotion with historical patterns"""
        if not mood_history:
            return 'no_history'
        
        recent_moods = mood_history[-5:]  # Last 5 moods
        
        if current_emotion == 'sadness' and all(mood != 'sadness' for mood in recent_moods):
            return 'mood_drop'
        elif current_emotion == 'joy' and all(mood != 'joy' for mood in recent_moods):
            return 'mood_lift'
        else:
            return 'consistent'
    
    def enhance_response_context(self, ai_response: str, processed_input: Dict) -> str:
        """Enhance AI response based on processed input"""
        enhanced_response = ai_response
        
        # Add emotional acknowledgment if strong emotion detected
        if processed_input['emotions']['intensity'] > 0.7:
            emotion = processed_input['emotions']['dominant']
            if emotion == 'sadness':
                enhanced_response = f"I can sense you're going through a tough time. {enhanced_response}"
            elif emotion == 'joy':
                enhanced_response = f"I can feel your happiness! {enhanced_response}"
        
        # Add celebration if achievement detected
        if processed_input['achievements']['has_achievement']:
            enhanced_response += " 🎉 Congratulations on your accomplishment!"
        
        return enhanced_response