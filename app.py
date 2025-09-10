#!/usr/bin/env python3
"""
Prophantom Johnnet AI 2.0 - The Sovereign Gateway
Main Flask application entry point
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import os
import logging
from datetime import datetime

# Import all agent blueprints
from agents.ai_girlfriend.routes import ai_girlfriend_bp
from agents.emo_ai.routes import emo_ai_bp
from agents.pdf_mind.routes import pdf_mind_bp
from agents.chat_revive.routes import chat_revive_bp
from agents.tok_boost.routes import tok_boost_bp
from agents.you_gen.routes import you_gen_bp
from agents.agent_x.routes import agent_x_bp
from agents.auto_chat.routes import auto_chat_bp
from agents.cv_smash.routes import cv_smash_bp

# Core services
from core.database import init_db
from core.auth import auth_bp
from core.config import Config

def create_app():
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    socketio = SocketIO(app, cors_allowed_origins="*")
    init_db(app)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(ai_girlfriend_bp, url_prefix='/agents/ai-girlfriend')
    app.register_blueprint(emo_ai_bp, url_prefix='/agents/emo-ai')
    app.register_blueprint(pdf_mind_bp, url_prefix='/agents/pdf-mind')
    app.register_blueprint(chat_revive_bp, url_prefix='/agents/chat-revive')
    app.register_blueprint(tok_boost_bp, url_prefix='/agents/tok-boost')
    app.register_blueprint(you_gen_bp, url_prefix='/agents/you-gen')
    app.register_blueprint(agent_x_bp, url_prefix='/agents/agent-x')
    app.register_blueprint(auto_chat_bp, url_prefix='/agents/auto-chat')
    app.register_blueprint(cv_smash_bp, url_prefix='/agents/cv-smash')
    
    # Main routes
    @app.route('/')
    def index():
        """Homepage - Beautiful modern landing page"""
        return render_template('homepage.html')

    @app.route('/agents-dashboard')
    def agents_dashboard():
        """Agent dashboard"""
        return render_template('index.html')
    
    @app.route('/platform')
    def platform():
        """Platform overview and services"""
        return render_template('platform.html')
    
    @app.route('/use-cases')
    def use_cases():
        """Industries and use cases"""
        return render_template('use_cases.html')
    
    @app.route('/pricing')
    def pricing():
        """Pricing plans"""
        return render_template('pricing.html')
    
    @app.route('/docs')
    def docs():
        """API Documentation"""
        return render_template('docs.html')
    
    @app.route('/blog')
    def blog():
        """Blog and news"""
        return render_template('blog.html')
    
    @app.route('/about')
    def about():
        """About us page"""
        return render_template('about.html')
    
    @app.route('/contact')
    def contact():
        """Contact and support"""
        return render_template('contact.html')
    
    @app.route('/dashboard')
    def user_dashboard():
        """User dashboard"""
        return render_template('dashboard.html')
    
    # API Routes
    @app.route('/api/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'agents_available': 9
        })
    
    @app.route('/api/agents')
    def list_agents():
        """List all available agents"""
        agents = [
            {'name': 'AI Girlfriend', 'endpoint': '/agents/ai-girlfriend', 'status': 'active'},
            {'name': 'EmoAI', 'endpoint': '/agents/emo-ai', 'status': 'active'},
            {'name': 'PDFMind', 'endpoint': '/agents/pdf-mind', 'status': 'active'},
            {'name': 'ChatRevive', 'endpoint': '/agents/chat-revive', 'status': 'active'},
            {'name': 'TokBoost', 'endpoint': '/agents/tok-boost', 'status': 'active'},
            {'name': 'YouGen', 'endpoint': '/agents/you-gen', 'status': 'active'},
            {'name': 'AgentX', 'endpoint': '/agents/agent-x', 'status': 'active'},
            {'name': 'AutoChat', 'endpoint': '/agents/auto-chat', 'status': 'active'},
            {'name': 'CVSmash', 'endpoint': '/agents/cv-smash', 'status': 'active'}
        ]
        return jsonify({'agents': agents})
    
    # WebSocket events
    @socketio.on('connect')
    def handle_connect():
        emit('status', {'msg': 'Connected to Prophantom Johnnet AI 2.0'})
    
    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')
    
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)