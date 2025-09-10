"""
AI Girlfriend WebSocket Handler
Real-time communication for companion interactions
"""

from flask_socketio import emit, join_room, leave_room
from flask import session
import json
from datetime import datetime
from core.database import execute_query, fetch_all
from core.ollama_service import ollama_service, AgentModels
from .logic import AIGirlfriendLogic

logic = AIGirlfriendLogic()

class CompanionSocketHandler:
    """Handles WebSocket events for AI Girlfriend"""
    
    def __init__(self, socketio):
        self.socketio = socketio
        self.active_users = {}
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup WebSocket event handlers"""
        
        @self.socketio.on('join_companion')
        def handle_join_companion(data):
            """User joins companion room"""
            if 'user_id' not in session:
                emit('error', {'message': 'Authentication required'})
                return
            
            user_id = session['user_id']
            room = f"companion_{user_id}"
            join_room(room)
            
            # Track active user
            self.active_users[user_id] = {
                'room': room,
                'joined_at': datetime.now().isoformat(),
                'status': 'active'
            }
            
            # Send welcome message
            emit('companion_joined', {
                'message': 'Connected to your AI companion!',
                'room': room,
                'status': 'connected'
            })
            
            # Send daily check-in if appropriate
            self._maybe_send_daily_checkin(user_id)
        
        @self.socketio.on('leave_companion')
        def handle_leave_companion():
            """User leaves companion room"""
            if 'user_id' not in session:
                return
            
            user_id = session['user_id']
            if user_id in self.active_users:
                room = self.active_users[user_id]['room']
                leave_room(room)
                del self.active_users[user_id]
            
            emit('companion_left', {'message': 'Disconnected from companion'})
        
        @self.socketio.on('companion_message')
        def handle_companion_message(data):
            """Handle real-time companion messages"""
            if 'user_id' not in session:
                emit('error', {'message': 'Authentication required'})
                return
            
            user_id = session['user_id']
            message = data.get('message', '').strip()
            
            if not message:
                emit('error', {'message': 'Message cannot be empty'})
                return
            
            try:
                # Process message in real-time
                response = self._process_companion_message(user_id, message)
                
                # Emit response immediately
                emit('companion_response', {
                    'response': response,
                    'timestamp': datetime.now().isoformat(),
                    'message_id': data.get('message_id')
                })
                
                # Store conversation
                execute_query(
                    'INSERT INTO conversations (user_id, agent_type, message, response) VALUES (?, ?, ?, ?)',
                    (user_id, 'ai_girlfriend', message, response)
                )
                
            except Exception as e:
                emit('error', {'message': f'Failed to process message: {str(e)}'})
        
        @self.socketio.on('typing_companion')
        def handle_typing():
            """Handle typing indicators"""
            if 'user_id' not in session:
                return
            
            user_id = session['user_id']
            if user_id in self.active_users:
                room = self.active_users[user_id]['room']
                emit('companion_typing', {'typing': True}, room=room)
        
        @self.socketio.on('stop_typing_companion')
        def handle_stop_typing():
            """Handle stop typing"""
            if 'user_id' not in session:
                return
            
            user_id = session['user_id']
            if user_id in self.active_users:
                room = self.active_users[user_id]['room']
                emit('companion_typing', {'typing': False}, room=room)
        
        @self.socketio.on('mood_update')
        def handle_mood_update(data):
            """Handle mood updates"""
            if 'user_id' not in session:
                emit('error', {'message': 'Authentication required'})
                return
            
            user_id = session['user_id']
            mood = data.get('mood')
            context = data.get('context', '')
            
            if mood:
                # Store mood update
                execute_query(
                    '''INSERT OR REPLACE INTO user_sessions (user_id, agent_type, session_data, updated_at) 
                       VALUES (?, ?, ?, CURRENT_TIMESTAMP)''',
                    (user_id, 'ai_girlfriend', json.dumps({'mood': mood, 'context': context}))
                )
                
                # Send mood-appropriate response
                mood_response = self._generate_mood_response(mood, context)
                emit('mood_acknowledged', {
                    'mood': mood,
                    'response': mood_response,
                    'timestamp': datetime.now().isoformat()
                })
        
        @self.socketio.on('request_checkin')
        def handle_request_checkin():
            """Handle manual check-in requests"""
            if 'user_id' not in session:
                emit('error', {'message': 'Authentication required'})
                return
            
            user_id = session['user_id']
            checkin_message = self._generate_checkin_message(user_id)
            
            emit('companion_checkin', {
                'message': checkin_message,
                'type': 'daily_checkin',
                'timestamp': datetime.now().isoformat()
            })
    
    def _process_companion_message(self, user_id: int, message: str) -> str:
        """Process companion message and generate response"""
        # Get conversation history
        history = fetch_all(
            'SELECT message, response FROM conversations WHERE user_id = ? AND agent_type = ? ORDER BY timestamp DESC LIMIT 10',
            (user_id, 'ai_girlfriend')
        )
        
        # Build conversation context
        messages = []
        for conv in reversed(history):
            messages.extend([
                {"role": "user", "content": conv['message']},
                {"role": "assistant", "content": conv['response']}
            ])
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        # Get response from Ollama
        response = ollama_service.chat(
            model=AgentModels.AI_GIRLFRIEND['model'],
            messages=[{"role": "system", "content": AgentModels.AI_GIRLFRIEND['system']}] + messages,
            temperature=AgentModels.AI_GIRLFRIEND['temperature']
        )
        
        if not response:
            response = "I'm having trouble connecting right now. Please try again in a moment."
        
        # Enhance response through logic layer
        enhanced_response = logic.enhance_response(response, message, user_id)
        
        return enhanced_response
    
    def _maybe_send_daily_checkin(self, user_id: int):
        """Send daily check-in if appropriate"""
        # Check if user has been checked in today
        today = datetime.now().date().isoformat()
        
        last_checkin = fetch_all(
            'SELECT timestamp FROM conversations WHERE user_id = ? AND agent_type = ? AND DATE(timestamp) = ?',
            (user_id, 'ai_girlfriend_checkin', today)
        )
        
        if not last_checkin:
            checkin_message = self._generate_checkin_message(user_id)
            
            # Send check-in
            room = self.active_users[user_id]['room']
            self.socketio.emit('daily_checkin', {
                'message': checkin_message,
                'type': 'daily_checkin',
                'timestamp': datetime.now().isoformat()
            }, room=room)
            
            # Store checkin
            execute_query(
                'INSERT INTO conversations (user_id, agent_type, message, response) VALUES (?, ?, ?, ?)',
                (user_id, 'ai_girlfriend_checkin', 'Daily check-in', checkin_message)
            )
    
    def _generate_checkin_message(self, user_id: int) -> str:
        """Generate personalized check-in message"""
        # Get user context
        user_prefs = logic.get_user_preferences(user_id)
        
        # Generate check-in based on time and context
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            base_message = "Good morning! How are you starting your day?"
        elif 12 <= hour < 17:
            base_message = "Good afternoon! How's your day going so far?"
        elif 17 <= hour < 21:
            base_message = "Good evening! How are you winding down?"
        else:
            base_message = "Hello there! How are you doing?"
        
        # Personalize based on user history
        relationship_level = logic.calculate_relationship_level(user_id)
        if relationship_level['level_number'] >= 3:
            base_message += " I've been thinking about you and wanted to check in. 💙"
        
        return base_message
    
    def _generate_mood_response(self, mood: str, context: str) -> str:
        """Generate response based on mood"""
        mood_responses = {
            'happy': [
                "I love seeing you happy! Your joy is contagious! ✨",
                "That's wonderful! Tell me what's making you feel so good!",
                "Your happiness makes my day brighter! 🌟"
            ],
            'sad': [
                "I'm here for you. It's okay to feel sad sometimes. 💙",
                "I can see you're going through a tough time. Want to talk about it?",
                "Sending you comfort and support. You're not alone. 🤗"
            ],
            'excited': [
                "I can feel your excitement! That's amazing! 🎉",
                "Your energy is infectious! Tell me more!",
                "I'm so excited for you! This is wonderful! ✨"
            ],
            'stressed': [
                "Take a deep breath. You're stronger than you think. 🌸",
                "I'm here to support you through this stressful time.",
                "Remember to be gentle with yourself. You're doing your best. 💙"
            ],
            'tired': [
                "You deserve rest. Take care of yourself. 🕯️",
                "It sounds like you need some self-care time.",
                "Remember, it's okay to slow down when you need to."
            ]
        }
        
        import random
        responses = mood_responses.get(mood, mood_responses['happy'])
        base_response = random.choice(responses)
        
        if context:
            base_response += f" Thanks for sharing that context with me."
        
        return base_response
    
    def broadcast_to_user(self, user_id: int, event: str, data: Dict):
        """Broadcast message to specific user"""
        if user_id in self.active_users:
            room = self.active_users[user_id]['room']
            self.socketio.emit(event, data, room=room)
    
    def get_active_users(self) -> Dict:
        """Get list of active users"""
        return self.active_users