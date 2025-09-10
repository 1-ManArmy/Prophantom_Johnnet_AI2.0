import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'prophantom-johnnet-ai-2024-secret-key'
    
    # Database
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///prophantom_ai.db'
    
    # Ollama Configuration
    OLLAMA_HOST = os.environ.get('OLLAMA_HOST') or 'http://localhost:11434'
    OLLAMA_MODELS = {
        'yi:6b': 'a7f031bb846f',
        'mathstral:7b': '4ee7052be55a',
        'nomic-embed-text:latest': '0a109f422b47',
        'snowflake-arctic-embed:latest': '21ab8b9b0545',
        'phi3:14b': 'cf611a26b048',
        'qwen2.5:7b': '845dbda0ea48',
        'gemma2:2b': '8ccf136fdd52',
        'llava:7b': '8dd30f6b0cb1',
        'mistral:7b': '6577803aa9a0',
        'deepseek-coder:6.7b': 'ce298d984115',
        'llama3.2:3b': 'a80c4f17acd5'
    }
    
    # Session Configuration
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # File Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = 'uploads'
    
    # Agent-specific configurations
    AGENTS_CONFIG = {
        'ai_girlfriend': {
            'model': 'phi3:14b',
            'personality': 'supportive_companion',
            'memory_limit': 1000
        },
        'emo_ai': {
            'model': 'gemma2:2b',
            'sentiment_analysis': True,
            'emotion_detection': True
        },
        'pdf_mind': {
            'model': 'qwen2.5:7b',
            'embedding_model': 'nomic-embed-text:latest',
            'chunk_size': 1000
        },
        'chat_revive': {
            'model': 'mistral:7b',
            'context_window': 4096
        },
        'tok_boost': {
            'model': 'llama3.2:3b',
            'optimization_mode': 'speed'
        },
        'you_gen': {
            'model': 'deepseek-coder:6.7b',
            'generation_mode': 'creative'
        },
        'agent_x': {
            'model': 'yi:6b',
            'multi_modal': True
        },
        'auto_chat': {
            'model': 'mathstral:7b',
            'auto_response': True
        },
        'cv_smash': {
            'model': 'llava:7b',
            'vision_enabled': True
        }
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    DATABASE_URL = 'sqlite:///:memory:'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}