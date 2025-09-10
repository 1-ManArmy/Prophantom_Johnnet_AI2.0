#!/usr/bin/env python3
"""
Auto Chat WebSocket Handler
Real-time communication for auto chat agent
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from flask_socketio import emit, join_room, leave_room
from ..logic import AutoChatLogic
from ..engine.ollama_phi3 import AutoChatOllamaEngine
from ..engine.predict import AutoChatPredictor

logger = logging.getLogger(__name__)

class AutoChatSocketHandler:
    """WebSocket handler for auto chat real-time communication"""
    
    def __init__(self):
        self.logic = AutoChatLogic()
        self.engine = AutoChatOllamaEngine()
        self.predictor = AutoChatPredictor()
        self.active_sessions = {}
        self.typing_indicators = {}
    
    async def handle_connect(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """Handle user connection"""
        try:
            # Join user to their room
            join_room(f"auto_chat_{user_id}")
            
            # Initialize session
            self.active_sessions[session_id] = {
                'user_id': user_id,
                'connected_at': datetime.now(),
                'status': 'active',
                'message_count': 0
            }
            
            # Send welcome message
            welcome_context = await self.logic.get_conversation_insights(user_id)
            
            emit('connection_established', {
                'status': 'connected',
                'session_id': session_id,
                'welcome_message': 'Hello! I\'m your auto-chat assistant. How can I help you today?',
                'context': welcome_context
            })
            
            logger.info(f"Auto chat connection established for user {user_id}")
            return {'success': True, 'session_id': session_id}
            
        except Exception as e:
            logger.error(f"Error handling connection: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def handle_message(self, data: Dict[str, Any]) -> None:
        """Handle incoming message"""
        try:
            user_id = data.get('user_id')
            message = data.get('message', '')
            session_id = data.get('session_id')
            
            if not user_id or not message:
                emit('error', {'message': 'Missing required fields'})
                return
            
            # Update session
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['message_count'] += 1
            
            # Show typing indicator
            emit('typing_indicator', {'status': 'typing', 'agent': 'auto_chat'}, 
                 room=f"auto_chat_{user_id}")
            
            # Process message with logic engine
            response_data = await self.logic.process_auto_response(user_id, message)
            
            # Calculate optimal response timing
            timing_context = {
                'urgency': 3,  # Default urgency
                'patience_level': 'medium',
                'flow_speed': 'normal'
            }
            optimal_delay = await self.engine.optimize_response_timing(timing_context)
            
            # Add realistic typing delay
            await asyncio.sleep(min(optimal_delay, 3.0))
            
            # Stop typing indicator
            emit('typing_indicator', {'status': 'stopped'}, room=f"auto_chat_{user_id}")
            
            # Send response
            if response_data['success']:
                # Get conversation predictions
                conversation_history = []  # Would get from logic context
                predictions = await self.predictor.predict_user_response(
                    conversation_history, response_data['response']
                )
                
                emit('message', {
                    'type': 'auto_chat_response',
                    'message': response_data['response'],
                    'context': response_data.get('context', {}),
                    'predictions': predictions,
                    'timestamp': datetime.now().isoformat(),
                    'agent': 'auto_chat'
                }, room=f"auto_chat_{user_id}")
                
                # Send analytics data
                emit('analytics', {
                    'sentiment': response_data['context'].get('sentiment'),
                    'engagement_level': response_data['context'].get('engagement_level'),
                    'topic': response_data['context'].get('topic')
                }, room=f"auto_chat_{user_id}")
                
            else:
                emit('error', {
                    'message': 'Sorry, I encountered an error processing your message.',
                    'details': response_data.get('error', 'Unknown error')
                }, room=f"auto_chat_{user_id}")
            
        except Exception as e:
            logger.error(f"Error handling message: {str(e)}")
            emit('error', {'message': 'An unexpected error occurred'})
    
    async def handle_typing(self, data: Dict[str, Any]) -> None:
        """Handle typing indicator"""
        try:
            user_id = data.get('user_id')
            is_typing = data.get('is_typing', False)
            
            if not user_id:
                return
            
            # Store typing state
            self.typing_indicators[user_id] = {
                'is_typing': is_typing,
                'timestamp': datetime.now()
            }
            
            # If user is typing, prepare proactive suggestions
            if is_typing:
                # Get conversation context for suggestions
                context = await self.logic.get_conversation_insights(user_id)
                
                # Generate proactive message if appropriate
                if context.get('engagement_level', 1) >= 3:
                    proactive_msg = await self.engine.generate_proactive_message(context)
                    
                    # Send suggestion (but don't auto-send)
                    emit('suggestion', {
                        'type': 'proactive',
                        'message': proactive_msg,
                        'context': 'typing_detected'
                    }, room=f"auto_chat_{user_id}")
            
        except Exception as e:
            logger.error(f"Error handling typing: {str(e)}")
    
    async def handle_feedback(self, data: Dict[str, Any]) -> None:
        """Handle user feedback"""
        try:
            user_id = data.get('user_id')
            feedback_type = data.get('type', 'rating')  # rating, thumbs, comment
            feedback_value = data.get('value')
            message_id = data.get('message_id')
            
            if not user_id or feedback_value is None:
                emit('error', {'message': 'Invalid feedback data'})
                return
            
            # Process feedback through training system
            feedback_data = {
                'user_id': user_id,
                'feedback_type': feedback_type,
                'value': feedback_value,
                'message_id': message_id,
                'timestamp': datetime.now().isoformat()
            }
            
            # Store and learn from feedback
            # This would integrate with the training module
            
            emit('feedback_received', {
                'status': 'success',
                'message': 'Thank you for your feedback!'
            }, room=f"auto_chat_{user_id}")
            
        except Exception as e:
            logger.error(f"Error handling feedback: {str(e)}")
            emit('error', {'message': 'Error processing feedback'})
    
    async def handle_context_request(self, data: Dict[str, Any]) -> None:
        """Handle request for conversation context"""
        try:
            user_id = data.get('user_id')
            context_type = data.get('context_type', 'full')  # full, summary, insights
            
            if not user_id:
                emit('error', {'message': 'User ID required'})
                return
            
            if context_type == 'insights':
                insights = await self.logic.get_conversation_insights(user_id)
                emit('context_data', {
                    'type': 'insights',
                    'data': insights
                }, room=f"auto_chat_{user_id}")
                
            elif context_type == 'predictions':
                # Get conversation history and generate predictions
                conversation_history = []  # Would get from database
                predictions = await self.predictor.predict_conversation_direction(conversation_history)
                
                emit('context_data', {
                    'type': 'predictions',
                    'data': predictions
                }, room=f"auto_chat_{user_id}")
            
        except Exception as e:
            logger.error(f"Error handling context request: {str(e)}")
            emit('error', {'message': 'Error retrieving context'})
    
    async def handle_disconnect(self, user_id: str, session_id: str) -> None:
        """Handle user disconnection"""
        try:
            # Leave room
            leave_room(f"auto_chat_{user_id}")
            
            # Clean up session
            if session_id in self.active_sessions:
                session_data = self.active_sessions[session_id]
                session_data['status'] = 'disconnected'
                session_data['disconnected_at'] = datetime.now()
                
                # Calculate session metrics
                session_duration = session_data['disconnected_at'] - session_data['connected_at']
                session_metrics = {
                    'duration_minutes': session_duration.total_seconds() / 60,
                    'message_count': session_data['message_count'],
                    'user_id': user_id,
                    'session_id': session_id
                }
                
                # Store session analytics
                await self._store_session_analytics(session_metrics)
                
                # Clean up
                del self.active_sessions[session_id]
            
            # Clean up typing indicators
            if user_id in self.typing_indicators:
                del self.typing_indicators[user_id]
            
            logger.info(f"Auto chat session ended for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error handling disconnect: {str(e)}")
    
    async def send_proactive_message(self, user_id: str, context: Dict[str, Any]) -> None:
        """Send proactive message to user"""
        try:
            # Generate proactive message
            proactive_msg = await self.engine.generate_proactive_message(context)
            
            emit('proactive_message', {
                'message': proactive_msg,
                'context': context,
                'timestamp': datetime.now().isoformat(),
                'type': 'proactive'
            }, room=f"auto_chat_{user_id}")
            
        except Exception as e:
            logger.error(f"Error sending proactive message: {str(e)}")
    
    async def _store_session_analytics(self, metrics: Dict[str, Any]) -> None:
        """Store session analytics data"""
        try:
            # This would store analytics in database
            logger.info(f"Session analytics: {metrics}")
            
        except Exception as e:
            logger.error(f"Error storing session analytics: {str(e)}")
    
    def get_active_sessions(self) -> Dict[str, Any]:
        """Get information about active sessions"""
        return {
            'total_active': len(self.active_sessions),
            'sessions': {
                session_id: {
                    'user_id': session['user_id'],
                    'connected_duration': (datetime.now() - session['connected_at']).total_seconds(),
                    'message_count': session['message_count'],
                    'status': session['status']
                }
                for session_id, session in self.active_sessions.items()
                if session['status'] == 'active'
            }
        }

# Global socket handler instance
auto_chat_socket_handler = AutoChatSocketHandler()