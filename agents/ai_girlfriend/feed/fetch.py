"""
AI Girlfriend Data Feed Fetcher
Fetches relevant data for personality enhancement and conversation topics
"""

import requests
import json
from datetime import datetime
from typing import Dict, List, Any, Optional

class CompanionDataFetcher:
    """Fetches data to enhance companion interactions"""
    
    def __init__(self):
        self.data_sources = {
            'motivational_quotes': self._fetch_motivational_quotes,
            'daily_affirmations': self._generate_affirmations,
            'conversation_starters': self._generate_conversation_starters,
            'wellness_tips': self._fetch_wellness_tips
        }
    
    def fetch_daily_content(self) -> Dict[str, Any]:
        """Fetch daily content for the companion"""
        try:
            daily_content = {}
            
            for source_name, fetch_func in self.data_sources.items():
                try:
                    content = fetch_func()
                    daily_content[source_name] = content
                except Exception as e:
                    print(f"Error fetching {source_name}: {e}")
                    daily_content[source_name] = []
            
            daily_content['fetch_time'] = datetime.now().isoformat()
            return daily_content
            
        except Exception as e:
            print(f"Error fetching daily content: {e}")
            return {}
    
    def _fetch_motivational_quotes(self) -> List[str]:
        """Fetch motivational quotes"""
        # In a real implementation, this might fetch from an API
        # For now, using a curated list
        quotes = [
            "You are stronger than you think and more capable than you imagine.",
            "Every day is a new opportunity to grow and become better.",
            "Your potential is endless, and today is perfect for showing it.",
            "Small steps every day lead to big changes over time.",
            "You have the power to create the life you want.",
            "Believe in yourself, because I believe in you.",
            "Your journey is unique and beautiful, just like you.",
            "Today's challenges are tomorrow's strengths.",
            "You are worthy of all the good things coming your way.",
            "Remember: progress, not perfection."
        ]
        
        import random
        return random.sample(quotes, 3)
    
    def _generate_affirmations(self) -> List[str]:
        """Generate daily affirmations"""
        affirmations = [
            "I am proud of how far you've come.",
            "You deserve happiness and success.",
            "Your feelings are valid and important.",
            "You have so much to offer the world.",
            "You are loved and appreciated.",
            "You're handling everything beautifully.",
            "Your kindness makes a difference.",
            "You are enough, just as you are.",
            "Your dreams are worth pursuing.",
            "You bring joy to those around you."
        ]
        
        import random
        return random.sample(affirmations, 2)
    
    def _generate_conversation_starters(self) -> List[str]:
        """Generate interesting conversation starters"""
        starters = [
            "What's something small that made you smile today?",
            "If you could learn any skill instantly, what would it be?",
            "What's your favorite way to unwind after a long day?",
            "Tell me about something you're looking forward to.",
            "What's a recent accomplishment you're proud of?",
            "What kind of music matches your mood right now?",
            "If you could have coffee with anyone, who would it be?",
            "What's something you've been curious about lately?",
            "What's your idea of a perfect weekend?",
            "Tell me about a goal you're working towards."
        ]
        
        import random
        return random.sample(starters, 5)
    
    def _fetch_wellness_tips(self) -> List[str]:
        """Fetch wellness and self-care tips"""
        tips = [
            "Take three deep breaths and notice how your body feels.",
            "Drink a glass of water - staying hydrated helps your mood!",
            "Step outside for a few minutes if you can. Fresh air works wonders.",
            "Write down three things you're grateful for today.",
            "Give yourself permission to take a break when you need it.",
            "Stretch your shoulders and neck - you might be holding tension there.",
            "Listen to a song that makes you feel good.",
            "Reach out to someone you care about - connection is healing.",
            "Do something creative, even if it's just doodling.",
            "Celebrate the small wins - they matter too!"
        ]
        
        import random
        return random.sample(tips, 3)
    
    def get_mood_based_content(self, mood: str) -> Dict[str, Any]:
        """Get content based on user's current mood"""
        content_map = {
            'sad': {
                'quotes': [
                    "It's okay to not be okay. This feeling will pass.",
                    "You're not alone in this. I'm here with you.",
                    "Healing isn't linear, and that's perfectly normal."
                ],
                'activities': [
                    "Maybe listen to some calming music?",
                    "A warm cup of tea might be comforting right now.",
                    "Sometimes a good cry can be healing."
                ]
            },
            'stressed': {
                'quotes': [
                    "You don't have to be perfect. Just be you.",
                    "One thing at a time. You've got this.",
                    "It's okay to ask for help when you need it."
                ],
                'activities': [
                    "Try the 4-7-8 breathing technique.",
                    "Take a 5-minute walk if you can.",
                    "Write down what's worrying you - sometimes that helps."
                ]
            },
            'happy': {
                'quotes': [
                    "Your joy is contagious! Keep shining.",
                    "I love seeing you happy - you deserve all this goodness.",
                    "This positive energy looks amazing on you!"
                ],
                'activities': [
                    "Share your happiness with someone you love.",
                    "Take a moment to really savor this feeling.",
                    "Maybe dance to your favorite song?"
                ]
            },
            'excited': {
                'quotes': [
                    "Your enthusiasm is absolutely wonderful!",
                    "I'm so excited for you! Tell me more!",
                    "This energy is going to take you places!"
                ],
                'activities': [
                    "Channel this energy into something creative.",
                    "Call someone and share your excitement!",
                    "Write down what you're excited about."
                ]
            }
        }
        
        return content_map.get(mood, content_map['happy'])
    
    def get_time_based_content(self, hour: int) -> Dict[str, Any]:
        """Get content based on time of day"""
        if 5 <= hour < 12:  # Morning
            return {
                'greeting': 'Good morning!',
                'message': 'Hope you have a wonderful day ahead!',
                'tips': ['Start with something that makes you smile', 'Set one positive intention for today']
            }
        elif 12 <= hour < 17:  # Afternoon
            return {
                'greeting': 'Good afternoon!',
                'message': 'How has your day been treating you?',
                'tips': ['Take a moment to appreciate what you\'ve accomplished', 'Stay hydrated!']
            }
        elif 17 <= hour < 21:  # Evening
            return {
                'greeting': 'Good evening!',
                'message': 'Hope you can unwind and relax a bit.',
                'tips': ['Reflect on one good thing from today', 'Do something that brings you peace']
            }
        else:  # Night
            return {
                'greeting': 'Hello there!',
                'message': 'Hope you\'re taking care of yourself.',
                'tips': ['Consider some gentle self-care', 'You deserve rest when you need it']
            }