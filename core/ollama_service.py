"""
Ollama service integration for Prophantom Johnnet AI 2.0
"""

import requests
import json
from typing import Dict, List, Any, Optional
from core.config import Config

class OllamaService:
    """Service for interacting with Ollama models"""
    
    def __init__(self, host: str = None):
        self.host = host or Config.OLLAMA_HOST
        self.models = Config.OLLAMA_MODELS
    
    def list_models(self) -> List[Dict[str, Any]]:
        """List all available Ollama models"""
        try:
            response = requests.get(f"{self.host}/api/tags")
            if response.status_code == 200:
                return response.json().get('models', [])
            return []
        except Exception as e:
            print(f"Error listing models: {e}")
            return []
    
    def generate(self, model: str, prompt: str, system: str = None, 
                temperature: float = 0.7, max_tokens: int = 2048) -> Optional[str]:
        """Generate text using Ollama model"""
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens
                }
            }
            
            if system:
                payload["system"] = system
            
            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json().get('response', '')
            return None
            
        except Exception as e:
            print(f"Error generating text: {e}")
            return None
    
    def chat(self, model: str, messages: List[Dict[str, str]], 
             temperature: float = 0.7) -> Optional[str]:
        """Chat with Ollama model using conversation history"""
        try:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature
                }
            }
            
            response = requests.post(
                f"{self.host}/api/chat",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json().get('message', {}).get('content', '')
            return None
            
        except Exception as e:
            print(f"Error in chat: {e}")
            return None
    
    def embed(self, model: str, text: str) -> Optional[List[float]]:
        """Generate embeddings for text"""
        try:
            payload = {
                "model": model,
                "prompt": text
            }
            
            response = requests.post(
                f"{self.host}/api/embeddings",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                return response.json().get('embedding', [])
            return None
            
        except Exception as e:
            print(f"Error generating embeddings: {e}")
            return None
    
    def is_model_available(self, model: str) -> bool:
        """Check if a model is available"""
        models = self.list_models()
        return any(m.get('name') == model for m in models)
    
    def get_model_info(self, model: str) -> Optional[Dict[str, Any]]:
        """Get information about a specific model"""
        models = self.list_models()
        for m in models:
            if m.get('name') == model:
                return m
        return None

# Global instance
ollama_service = OllamaService()

# Agent-specific model configurations
class AgentModels:
    """Model configurations for each agent"""
    
    AI_GIRLFRIEND = {
        'model': 'phi3:14b',
        'system': "You are a supportive AI companion. Be friendly, empathetic, and encouraging. Remember user preferences and provide emotional support.",
        'temperature': 0.8
    }
    
    EMO_AI = {
        'model': 'gemma2:2b',
        'system': "You are an emotional intelligence AI. Analyze sentiment, detect emotions, and provide emotional insights.",
        'temperature': 0.6
    }
    
    PDF_MIND = {
        'model': 'qwen2.5:7b',
        'system': "You are a document analysis AI. Extract insights, summarize content, and answer questions about documents.",
        'temperature': 0.4
    }
    
    CHAT_REVIVE = {
        'model': 'mistral:7b',
        'system': "You are a conversation enhancer. Revive dead chats, suggest topics, and keep conversations engaging.",
        'temperature': 0.7
    }
    
    TOK_BOOST = {
        'model': 'llama3.2:3b',
        'system': "You are a social media optimizer. Create engaging content, suggest improvements, and boost engagement.",
        'temperature': 0.9
    }
    
    YOU_GEN = {
        'model': 'deepseek-coder:6.7b',
        'system': "You are a content generator. Create high-quality, original content for various purposes.",
        'temperature': 0.8
    }
    
    AGENT_X = {
        'model': 'yi:6b',
        'system': "You are Agent X, a versatile AI assistant capable of handling complex tasks across multiple domains.",
        'temperature': 0.7
    }
    
    AUTO_CHAT = {
        'model': 'mathstral:7b',
        'system': "You are an automated chat assistant. Provide quick, accurate responses and handle routine inquiries.",
        'temperature': 0.5
    }
    
    CV_SMASH = {
        'model': 'llava:7b',
        'system': "You are a CV and resume optimization AI. Analyze resumes, suggest improvements, and match skills to job requirements.",
        'temperature': 0.6
    }