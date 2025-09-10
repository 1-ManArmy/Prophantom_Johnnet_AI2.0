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

    # Product Pages
    @app.route('/products')
    def products():
        """Products overview"""
        return render_template('products/index.html')
    
    @app.route('/products/chatbot')
    def products_chatbot():
        """AI Chatbots"""
        return render_template('products/chatbot.html')
    
    @app.route('/products/nlp')
    def products_nlp():
        """Natural Language Processing"""
        return render_template('products/nlp.html')
    
    @app.route('/products/computer-vision')
    def products_computer_vision():
        """Computer Vision"""
        return render_template('products/computer_vision.html')
    
    @app.route('/products/speech')
    def products_speech():
        """Speech AI"""
        return render_template('products/speech.html')
    
    @app.route('/products/translation')
    def products_translation():
        """Translation Services"""
        return render_template('products/translation.html')
    
    @app.route('/products/generative-ai')
    def products_generative_ai():
        """Generative AI"""
        return render_template('products/generative_ai.html')

    # Solutions Pages
    @app.route('/solutions')
    def solutions():
        """Solutions overview"""
        return render_template('solutions/index.html')
    
    @app.route('/solutions/healthcare')
    def solutions_healthcare():
        """Healthcare solutions"""
        return render_template('solutions/healthcare.html')
    
    @app.route('/solutions/finance')
    def solutions_finance():
        """Finance solutions"""
        return render_template('solutions/finance.html')
    
    @app.route('/solutions/education')
    def solutions_education():
        """Education solutions"""
        return render_template('solutions/education.html')
    
    @app.route('/solutions/retail')
    def solutions_retail():
        """Retail solutions"""
        return render_template('solutions/retail.html')
    
    @app.route('/solutions/customer-support')
    def solutions_customer_support():
        """Customer Support solutions"""
        return render_template('solutions/customer_support.html')
    
    @app.route('/solutions/marketing')
    def solutions_marketing():
        """Marketing solutions"""
        return render_template('solutions/marketing.html')

    # Pricing
    @app.route('/pricing')
    def pricing():
        """Pricing plans"""
        return render_template('pricing.html')

    # Documentation
    @app.route('/docs')
    def docs():
        """Documentation overview"""
        return render_template('docs/index.html')
    
    @app.route('/docs/api')
    def docs_api():
        """API Reference"""
        return render_template('docs/api.html')
    
    @app.route('/docs/sdks')
    def docs_sdks():
        """SDKs and Libraries"""
        return render_template('docs/sdks.html')
    
    @app.route('/docs/tutorials')
    def docs_tutorials():
        """Tutorials and Guides"""
        return render_template('docs/tutorials.html')

    # Authentication & Account
    @app.route('/signup')
    def signup():
        """Sign up page"""
        return render_template('auth/signup.html')
    
    @app.route('/signin')
    def signin():
        """Sign in page"""
        return render_template('auth/signin.html')
    
    @app.route('/dashboard')
    def dashboard():
        """User dashboard"""
        return render_template('account/dashboard.html')
    
    @app.route('/account/profile')
    def account_profile():
        """User profile"""
        return render_template('account/profile.html')
    
    @app.route('/account/billing')
    def account_billing():
        """Billing and payments"""
        return render_template('account/billing.html')
    
    @app.route('/account/api-keys')
    def account_api_keys():
        """API keys management"""
        return render_template('account/api_keys.html')

    # Legal Pages
    @app.route('/legal/terms')
    def legal_terms():
        """Terms of Service"""
        return render_template('legal/terms.html')
    
    @app.route('/legal/privacy')
    def legal_privacy():
        """Privacy Policy"""
        return render_template('legal/privacy.html')
    
    @app.route('/legal/cookies')
    def legal_cookies():
        """Cookie Policy"""
        return render_template('legal/cookies.html')
    
    @app.route('/legal/security')
    def legal_security():
        """Security Policy"""
        return render_template('legal/security.html')
    
    @app.route('/legal/compliance')
    def legal_compliance():
        """Compliance Information"""
        return render_template('legal/compliance.html')

    # Company Pages
    @app.route('/about')
    def about():
        """About us page"""
        return render_template('company/about.html')
    
    @app.route('/careers')
    def careers():
        """Careers page"""
        return render_template('company/careers.html')
    
    @app.route('/blog')
    def blog():
        """Blog and insights"""
        return render_template('company/blog.html')
    
    @app.route('/news')
    def news():
        """News and press releases"""
        return render_template('company/news.html')
    
    @app.route('/partners')
    def partners():
        """Partner program"""
        return render_template('company/partners.html')

    # Support Pages
    @app.route('/support')
    def support():
        """Support center"""
        return render_template('support/index.html')
    
    @app.route('/support/contact')
    def support_contact():
        """Contact support"""
        return render_template('support/contact.html')
    
    @app.route('/support/billing')
    def support_billing():
        """Billing support"""
        return render_template('support/billing.html')
    
    @app.route('/support/technical')
    def support_technical():
        """Technical support"""
        return render_template('support/technical.html')
    
    @app.route('/support/training')
    def support_training():
        """Training and education"""
        return render_template('support/training.html')

    # Community & Status
    @app.route('/community')
    def community():
        """Developer community"""
        return render_template('community.html')
    
    @app.route('/status')
    def status():
        """System status"""
        return render_template('status.html')

    # Contact
    @app.route('/contact')
    def contact():
        """Contact us"""
        return render_template('contact.html')

    # Agent Dashboard (existing)
    @app.route('/agents-dashboard')
    def agents_dashboard():
        """Agent dashboard"""
        return render_template('index.html')
    
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