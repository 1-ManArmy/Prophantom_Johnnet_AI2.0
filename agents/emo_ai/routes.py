"""
EmoAI Agent Routes
Sentiment decoder - reads the vibe, tunes the tone, ensures emotional resonance
"""

from flask import Blueprint, request, jsonify, render_template, session
from core.auth import login_required
from core.database import execute_query, fetch_all, fetch_one
from core.ollama_service import ollama_service, AgentModels
import json
from datetime import datetime

emo_ai_bp = Blueprint('emo_ai', __name__)

@emo_ai_bp.route('/')
def index():
    """EmoAI main interface"""
    return render_template('agents/emo_ai.html')

@emo_ai_bp.route('/analyze', methods=['POST'])
@login_required
def analyze_emotion():
    """Analyze emotional content of text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        user_id = session.get('user_id')
        
        # Analyze emotion using Gemma2 2B
        emotion_prompt = f"""
        Analyze the emotional content of this text: "{text}"
        
        Provide analysis in JSON format:
        {{
            "primary_emotion": "emotion name",
            "intensity": 0.0-1.0,
            "sentiment": "positive/negative/neutral", 
            "confidence": 0.0-1.0,
            "emotions_detected": ["emotion1", "emotion2"],
            "mood_indicators": ["indicator1", "indicator2"],
            "emotional_tone": "description",
            "suggestions": ["suggestion1", "suggestion2"]
        }}
        """
        
        response = ollama_service.generate(
            model=AgentModels.EMO_AI['model'],
            prompt=emotion_prompt,
            system=AgentModels.EMO_AI['system'],
            temperature=AgentModels.EMO_AI['temperature']
        )
        
        if not response:
            return jsonify({'error': 'Analysis failed'}), 500
        
        # Try to parse JSON response
        try:
            emotion_data = json.loads(response)
        except:
            # Fallback simple analysis
            emotion_data = {
                "primary_emotion": "neutral",
                "intensity": 0.5,
                "sentiment": "neutral",
                "confidence": 0.6,
                "emotions_detected": ["neutral"],
                "mood_indicators": [],
                "emotional_tone": "The text appears neutral",
                "suggestions": ["Consider adding more emotional expression"]
            }
        
        # Store analysis
        execute_query(
            'INSERT INTO conversations (user_id, agent_type, message, response) VALUES (?, ?, ?, ?)',
            (user_id, 'emo_ai', text, json.dumps(emotion_data))
        )
        
        return jsonify({
            'analysis': emotion_data,
            'timestamp': datetime.now().isoformat(),
            'agent': 'EmoAI'
        })
        
    except Exception as e:
        return jsonify({'error': f'Analysis error: {str(e)}'}), 500

@emo_ai_bp.route('/tune-tone', methods=['POST'])
@login_required  
def tune_tone():
    """Tune the emotional tone of text"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        desired_tone = data.get('tone', 'neutral')
        
        if not text:
            return jsonify({'error': 'Text cannot be empty'}), 400
        
        user_id = session.get('user_id')
        
        # Tune tone using EmoAI
        tune_prompt = f"""
        Rewrite this text to have a {desired_tone} emotional tone: "{text}"
        
        Requirements:
        - Maintain the core message
        - Adjust emotional language appropriately
        - Make it sound natural and authentic
        - Match the desired tone: {desired_tone}
        
        Return only the rewritten text.
        """
        
        response = ollama_service.generate(
            model=AgentModels.EMO_AI['model'],
            prompt=tune_prompt,
            system="You are an expert at adjusting emotional tone while preserving meaning.",
            temperature=0.7
        )
        
        if not response:
            response = text  # Fallback to original
        
        # Store tuning
        execute_query(
            'INSERT INTO conversations (user_id, agent_type, message, response) VALUES (?, ?, ?, ?)',
            (user_id, 'emo_ai_tune', f"{desired_tone}: {text}", response)
        )
        
        return jsonify({
            'original_text': text,
            'tuned_text': response,
            'target_tone': desired_tone,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Tone tuning error: {str(e)}'}), 500

@emo_ai_bp.route('/history', methods=['GET'])
@login_required
def get_analysis_history():
    """Get user's emotion analysis history"""
    try:
        user_id = session.get('user_id')
        
        # Get analysis history
        analyses = fetch_all(
            'SELECT message, response, timestamp FROM conversations WHERE user_id = ? AND agent_type = ? ORDER BY timestamp DESC LIMIT 20',
            (user_id, 'emo_ai')
        )
        
        history = []
        for analysis in analyses:
            try:
                emotion_data = json.loads(analysis['response'])
                history.append({
                    'text': analysis['message'],
                    'analysis': emotion_data,
                    'timestamp': analysis['timestamp']
                })
            except:
                continue
        
        return jsonify({
            'history': history,
            'total_analyses': len(history)
        })
        
    except Exception as e:
        return jsonify({'error': f'History retrieval error: {str(e)}'}), 500