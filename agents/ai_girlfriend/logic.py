"""
AI Girlfriend Logic Layer
Handles personality, memory, and relationship building
"""

import json
from datetime import datetime, timedelta
from core.database import execute_query, fetch_one, fetch_all
from typing import Dict, List, Any

class AIGirlfriendLogic:
    """Logic for AI Girlfriend agent"""
    
    def __init__(self):
        self.personality_traits = {
            'supportive': 0.9,
            'empathetic': 0.8,
            'encouraging': 0.9,
            'playful': 0.6,
            'wise': 0.7,
            'caring': 0.9
        }
    
    def enhance_response(self, response: str, user_message: str, user_id: int) -> str:
        """Enhance response based on user history and personality"""
        try:
            # Get user preferences
            preferences = self.get_user_preferences(user_id)
            
            # Add personality touches
            if self._detect_sadness(user_message):
                response = self._add_comfort(response)
            elif self._detect_excitement(user_message):
                response = self._add_enthusiasm(response)
            elif self._detect_stress(user_message):
                response = self._add_calming_elements(response)
            
            # Add personal touches based on history
            response = self._add_personal_touches(response, user_id, preferences)
            
            return response
            
        except Exception as e:
            print(f"Error enhancing response: {e}")
            return response
    
    def get_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Get user preferences and history"""
        try:
            session_data = fetch_one(
                'SELECT session_data FROM user_sessions WHERE user_id = ? AND agent_type = ?',
                (user_id, 'ai_girlfriend')
            )
            
            if session_data and session_data['session_data']:
                return json.loads(session_data['session_data'])
            
            return {
                'communication_style': 'friendly',
                'interests': [],
                'mood_history': [],
                'preferred_topics': [],
                'celebration_style': 'enthusiastic'
            }
            
        except Exception as e:
            print(f"Error getting preferences: {e}")
            return {}
    
    def update_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> None:
        """Update user preferences"""
        try:
            current_prefs = self.get_user_preferences(user_id)
            current_prefs.update(preferences)
            
            execute_query(
                '''INSERT OR REPLACE INTO user_sessions (user_id, agent_type, session_data, updated_at) 
                   VALUES (?, ?, ?, CURRENT_TIMESTAMP)''',
                (user_id, 'ai_girlfriend', json.dumps(current_prefs))
            )
            
        except Exception as e:
            print(f"Error updating preferences: {e}")
    
    def get_memory_highlights(self, user_id: int) -> List[Dict[str, Any]]:
        """Get important memory highlights"""
        try:
            # Get achievements and celebrations
            celebrations = fetch_all(
                'SELECT message, response, timestamp FROM conversations WHERE user_id = ? AND agent_type = ? ORDER BY timestamp DESC LIMIT 5',
                (user_id, 'ai_girlfriend_celebration')
            )
            
            # Get meaningful conversations (longer exchanges)
            meaningful_chats = fetch_all(
                'SELECT message, response, timestamp FROM conversations WHERE user_id = ? AND agent_type = ? AND LENGTH(message) > 100 ORDER BY timestamp DESC LIMIT 5',
                (user_id, 'ai_girlfriend')
            )
            
            memories = []
            
            for conv in celebrations:
                memories.append({
                    'type': 'celebration',
                    'content': conv['message'],
                    'date': conv['timestamp'],
                    'importance': 'high'
                })
            
            for conv in meaningful_chats:
                memories.append({
                    'type': 'deep_conversation',
                    'content': conv['message'][:100] + '...',
                    'date': conv['timestamp'],
                    'importance': 'medium'
                })
            
            return memories
            
        except Exception as e:
            print(f"Error getting memory highlights: {e}")
            return []
    
    def calculate_relationship_level(self, user_id: int) -> Dict[str, Any]:
        """Calculate relationship level based on interactions"""
        try:
            # Count total interactions
            total_convs = fetch_one(
                'SELECT COUNT(*) as count FROM conversations WHERE user_id = ? AND agent_type LIKE ?',
                (user_id, 'ai_girlfriend%')
            )['count']
            
            # Get interaction span
            first_interaction = fetch_one(
                'SELECT MIN(timestamp) as first_date FROM conversations WHERE user_id = ? AND agent_type LIKE ?',
                (user_id, 'ai_girlfriend%')
            )
            
            # Calculate level
            if total_convs >= 100:
                level = 'Best Friend'
                level_num = 5
            elif total_convs >= 50:
                level = 'Close Friend'
                level_num = 4
            elif total_convs >= 20:
                level = 'Good Friend'
                level_num = 3
            elif total_convs >= 5:
                level = 'Friend'
                level_num = 2
            else:
                level = 'Getting to Know Each Other'
                level_num = 1
            
            return {
                'level': level,
                'level_number': level_num,
                'total_conversations': total_convs,
                'days_together': self._calculate_days_since(first_interaction['first_date']) if first_interaction else 0,
                'next_milestone': self._get_next_milestone(total_convs)
            }
            
        except Exception as e:
            print(f"Error calculating relationship level: {e}")
            return {'level': 'Unknown', 'level_number': 0}
    
    def _detect_sadness(self, message: str) -> bool:
        """Detect sadness in message"""
        sad_keywords = ['sad', 'depressed', 'down', 'upset', 'hurt', 'crying', 'lonely', 'awful', 'terrible']
        return any(keyword in message.lower() for keyword in sad_keywords)
    
    def _detect_excitement(self, message: str) -> bool:
        """Detect excitement in message"""
        excited_keywords = ['excited', 'amazing', 'awesome', 'great', 'fantastic', 'wonderful', 'achieved', 'success']
        return any(keyword in message.lower() for keyword in excited_keywords)
    
    def _detect_stress(self, message: str) -> bool:
        """Detect stress in message"""
        stress_keywords = ['stressed', 'overwhelmed', 'busy', 'tired', 'exhausted', 'pressure', 'deadline']
        return any(keyword in message.lower() for keyword in stress_keywords)
    
    def _add_comfort(self, response: str) -> str:
        """Add comforting elements to response"""
        comfort_additions = [
            " 🤗 I'm here for you.",
            " Remember, it's okay to feel this way sometimes.",
            " You're stronger than you think. 💙"
        ]
        import random
        return response + random.choice(comfort_additions)
    
    def _add_enthusiasm(self, response: str) -> str:
        """Add enthusiastic elements to response"""
        enthusiasm_additions = [
            " That's fantastic! 🎉",
            " I'm so proud of you! ✨",
            " You're amazing! 🌟"
        ]
        import random
        return response + random.choice(enthusiasm_additions)
    
    def _add_calming_elements(self, response: str) -> str:
        """Add calming elements for stress"""
        calming_additions = [
            " Take a deep breath. You've got this! 🌸",
            " Remember to take breaks when you need them.",
            " One step at a time. 🕯️"
        ]
        import random
        return response + random.choice(calming_additions)
    
    def _add_personal_touches(self, response: str, user_id: int, preferences: Dict) -> str:
        """Add personal touches based on user history"""
        # This could be enhanced with more sophisticated personalization
        communication_style = preferences.get('communication_style', 'friendly')
        
        if communication_style == 'casual':
            response = response.replace('Hello', 'Hey').replace('Greetings', 'Hi there')
        elif communication_style == 'formal':
            response = response.replace('Hey', 'Hello').replace('Hi', 'Good day')
        
        return response
    
    def _calculate_days_since(self, date_str: str) -> int:
        """Calculate days since a given date"""
        try:
            if not date_str:
                return 0
            date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
            return (datetime.now() - date).days
        except:
            return 0
    
    def _get_next_milestone(self, current_convs: int) -> Dict[str, Any]:
        """Get next relationship milestone"""
        milestones = [5, 20, 50, 100, 200]
        
        for milestone in milestones:
            if current_convs < milestone:
                return {
                    'conversations_needed': milestone - current_convs,
                    'milestone_conversations': milestone,
                    'reward': f"Unlock new features at {milestone} conversations!"
                }
        
        return {
            'conversations_needed': 0,
            'milestone_conversations': current_convs,
            'reward': "You've reached the highest level! 🏆"
        }