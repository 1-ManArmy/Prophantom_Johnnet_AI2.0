"""
AI Girlfriend Agent Routes
Companion-grade module - supportive, intuitive, remembers rituals and celebrates wins
"""

from flask import Blueprint, request, jsonify, render_template, session
from core.auth import login_required
from core.database import execute_query, fetch_all, fetch_one
from core.ollama_service import ollama_service, AgentModels
from .logic import AIGirlfriendLogic
import json
from datetime import datetime

ai_girlfriend_bp = Blueprint('ai_girlfriend', __name__)
logic = AIGirlfriendLogic()

@ai_girlfriend_bp.route('/')
def index():
    """AI Girlfriend main interface"""
    return render_template('agents/ai_girlfriend.html')

@ai_girlfriend_bp.route('/chat', methods=['POST'])
@login_required
def chat():
    """Chat with AI Girlfriend"""
    try:
        data = request.get_json()
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Message cannot be empty'}), 400
        
        user_id = session.get('user_id')
        
        # Get user's conversation history for context
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
        
        # Save conversation
        execute_query(
            'INSERT INTO conversations (user_id, agent_type, message, response) VALUES (?, ?, ?, ?)',
            (user_id, 'ai_girlfriend', message, response)
        )
        
        # Process through logic layer for personality enhancement
        enhanced_response = logic.enhance_response(response, message, user_id)
        
        return jsonify({
            'response': enhanced_response,
            'timestamp': datetime.now().isoformat(),
            'agent': 'AI Girlfriend'
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat error: {str(e)}'}), 500

@ai_girlfriend_bp.route('/memory', methods=['GET'])
@login_required
def get_memory():
    """Get user's interaction memory"""
    try:
        user_id = session.get('user_id')
        
        # Get recent conversations
        conversations = fetch_all(
            'SELECT message, response, timestamp FROM conversations WHERE user_id = ? AND agent_type = ? ORDER BY timestamp DESC LIMIT 20',
            (user_id, 'ai_girlfriend')
        )
        
        # Get user preferences
        user_data = logic.get_user_preferences(user_id)
        
        return jsonify({
            'conversations': [dict(conv) for conv in conversations],
            'preferences': user_data,
            'memory_items': logic.get_memory_highlights(user_id)
        })
        
    except Exception as e:
        return jsonify({'error': f'Memory retrieval error: {str(e)}'}), 500

@ai_girlfriend_bp.route('/preferences', methods=['POST'])
@login_required
def update_preferences():
    """Update user preferences"""
    try:
        data = request.get_json()
        user_id = session.get('user_id')
        
        logic.update_user_preferences(user_id, data)
        
        return jsonify({'success': True, 'message': 'Preferences updated'})
        
    except Exception as e:
        return jsonify({'error': f'Preference update error: {str(e)}'}), 500

@ai_girlfriend_bp.route('/mood', methods=['POST'])
@login_required
def set_mood():
    """Set current mood/context"""
    try:
        data = request.get_json()
        mood = data.get('mood')
        context = data.get('context', '')
        
        user_id = session.get('user_id')
        
        # Store mood in session data
        execute_query(
            '''INSERT OR REPLACE INTO user_sessions (user_id, agent_type, session_data, updated_at) 
               VALUES (?, ?, ?, CURRENT_TIMESTAMP)''',
            (user_id, 'ai_girlfriend', json.dumps({'mood': mood, 'context': context}))
        )
        
        return jsonify({'success': True, 'message': f'Mood set to {mood}'})
        
    except Exception as e:
        return jsonify({'error': f'Mood setting error: {str(e)}'}), 500

@ai_girlfriend_bp.route('/celebrate', methods=['POST'])
@login_required
def celebrate_win():
    """Celebrate user's achievement"""
    try:
        data = request.get_json()
        achievement = data.get('achievement')
        
        if not achievement:
            return jsonify({'error': 'Achievement description required'}), 400
        
        user_id = session.get('user_id')
        
        # Generate celebration response
        celebration_prompt = f"Celebrate this achievement enthusiastically and personally: {achievement}"
        
        response = ollama_service.generate(
            model=AgentModels.AI_GIRLFRIEND['model'],
            prompt=celebration_prompt,
            system="You are celebrating a user's achievement. Be enthusiastic, personal, and encouraging. Make them feel proud and motivated.",
            temperature=0.9
        )
        
        # Store achievement
        execute_query(
            'INSERT INTO conversations (user_id, agent_type, message, response) VALUES (?, ?, ?, ?)',
            (user_id, 'ai_girlfriend_celebration', f"Achievement: {achievement}", response)
        )
        
        return jsonify({
            'celebration': response,
            'confetti': True,
            'achievement': achievement
        })
        
    except Exception as e:
        return jsonify({'error': f'Celebration error: {str(e)}'}), 500

@ai_girlfriend_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    """Get interaction statistics"""
    try:
        user_id = session.get('user_id')
        
        # Total conversations
        total_chats = fetch_one(
            'SELECT COUNT(*) as count FROM conversations WHERE user_id = ? AND agent_type = ?',
            (user_id, 'ai_girlfriend')
        )['count']
        
        # Days since first interaction
        first_interaction = fetch_one(
            'SELECT MIN(timestamp) as first_date FROM conversations WHERE user_id = ? AND agent_type = ?',
            (user_id, 'ai_girlfriend')
        )
        
        # Recent activity
        recent_activity = fetch_all(
            'SELECT DATE(timestamp) as date, COUNT(*) as count FROM conversations WHERE user_id = ? AND agent_type = ? GROUP BY DATE(timestamp) ORDER BY date DESC LIMIT 7',
            (user_id, 'ai_girlfriend')
        )
        
        return jsonify({
            'total_conversations': total_chats,
            'first_interaction': first_interaction['first_date'] if first_interaction else None,
            'recent_activity': [dict(activity) for activity in recent_activity],
            'relationship_level': logic.calculate_relationship_level(user_id)
        })
        
    except Exception as e:
        return jsonify({'error': f'Stats error: {str(e)}'}), 500