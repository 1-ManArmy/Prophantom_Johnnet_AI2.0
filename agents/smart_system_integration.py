#!/usr/bin/env python3
"""
Smart Agent System Integration
Complete integration of all smart agent components with advanced capabilities
"""

import asyncio
import logging
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys
import os

# Add project root to path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# Import core components
from core.database import get_db
from agents.universal_memory import UniversalMemorySystem
from agents.advanced_analytics import AdvancedAnalyticsSystem
from agents.enhanced_database_setup import setup_enhanced_database

# Import all agent logic modules
from agents.auto_chat.logic import AutoChatAgent
from agents.chat_revive.logic import ChatReviveAgent
from agents.cv_smash.logic import CVOptimizationAgent
from agents.emo_ai.logic import EmotionalSupportAgent
from agents.pdf_mind.logic import DocumentAnalysisAgent
from agents.tok_boost.logic import SocialMediaAgent
from agents.you_gen.logic import ContentGenerationAgent
from agents.agent_x.logic import AdaptiveIntelligenceAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SmartAgentSystem:
    """Complete smart agent system integration"""
    
    def __init__(self, config_path: str = None):
        self.config_path = config_path or str(project_root / "config" / "system_config.json")
        self.config = self._load_system_config()
        
        # Initialize core systems
        self.memory_system = UniversalMemorySystem()
        self.analytics_system = AdvancedAnalyticsSystem()
        
        # Initialize agents
        self.agents = {
            'auto_chat': AutoChatAgent(),
            'chat_revive': ChatReviveAgent(),
            'cv_smash': CVOptimizationAgent(),
            'emo_ai': EmotionalSupportAgent(),
            'pdf_mind': DocumentAnalysisAgent(),
            'tok_boost': SocialMediaAgent(),
            'you_gen': ContentGenerationAgent(),
            'agent_x': AdaptiveIntelligenceAgent()
        }
        
        # System state
        self.active_sessions = {}
        self.websocket_connections = {}
        self.message_queues = {}
        
        # Performance monitoring
        self.performance_monitor = PerformanceMonitor()
        
        logger.info("Smart Agent System initialized successfully")
    
    def _load_system_config(self) -> Dict[str, Any]:
        """Load system configuration"""
        default_config = {
            "system": {
                "name": "Prophantom Johnnet AI 2.0",
                "version": "2.0.0",
                "environment": "development",
                "max_concurrent_sessions": 100,
                "session_timeout": 3600,
                "memory_consolidation_interval": 21600,
                "analytics_update_interval": 300
            },
            "agents": {
                "auto_chat": {
                    "model": "phi3:14b",
                    "max_context_length": 4000,
                    "temperature": 0.7,
                    "specialization_weight": 0.8
                },
                "chat_revive": {
                    "model": "gemma2:2b",
                    "max_context_length": 3000,
                    "temperature": 0.6,
                    "specialization_weight": 0.9
                },
                "cv_smash": {
                    "model": "qwen2.5:7b",
                    "max_context_length": 5000,
                    "temperature": 0.4,
                    "specialization_weight": 0.95
                },
                "emo_ai": {
                    "model": "llama3.1:8b",
                    "max_context_length": 4500,
                    "temperature": 0.8,
                    "specialization_weight": 0.85
                },
                "pdf_mind": {
                    "model": "mistral:7b",
                    "max_context_length": 6000,
                    "temperature": 0.3,
                    "specialization_weight": 0.9
                },
                "tok_boost": {
                    "model": "deepseek-coder:6.7b",
                    "max_context_length": 4000,
                    "temperature": 0.7,
                    "specialization_weight": 0.8
                },
                "you_gen": {
                    "model": "llama3.2:3b",
                    "max_context_length": 3500,
                    "temperature": 0.9,
                    "specialization_weight": 0.75
                },
                "agent_x": {
                    "model": "codellama:7b",
                    "max_context_length": 5500,
                    "temperature": 0.5,
                    "specialization_weight": 0.9
                }
            },
            "memory": {
                "max_items_per_user": 10000,
                "consolidation_threshold": 0.3,
                "importance_decay": 0.99,
                "embedding_dimension": 384
            },
            "analytics": {
                "real_time_monitoring": True,
                "performance_tracking": True,
                "user_behavior_analysis": True,
                "predictive_insights": True
            },
            "websocket": {
                "port": 8765,
                "max_connections": 200,
                "ping_interval": 30,
                "ping_timeout": 10
            }
        }
        
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults
                return {**default_config, **loaded_config}
            else:
                # Create default config file
                os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
                with open(self.config_path, 'w') as f:
                    json.dump(default_config, f, indent=2)
                return default_config
        except Exception as e:
            logger.warning(f"Error loading config, using defaults: {str(e)}")
            return default_config
    
    async def initialize_system(self) -> bool:
        """Initialize the complete system"""
        try:
            logger.info("Initializing Smart Agent System...")
            
            # Setup enhanced database
            if not setup_enhanced_database():
                raise Exception("Failed to setup database")
            
            # Initialize memory system
            await self.memory_system.initialize()
            
            # Initialize analytics system
            await self.analytics_system.initialize()
            
            # Initialize all agents
            for agent_name, agent in self.agents.items():
                await agent.initialize()
                logger.info(f"✅ {agent_name} agent initialized")
            
            # Start background tasks
            await self._start_background_tasks()
            
            # Load existing sessions
            await self._load_existing_sessions()
            
            logger.info("🚀 Smart Agent System fully initialized!")
            return True
            
        except Exception as e:
            logger.error(f"❌ System initialization failed: {str(e)}")
            return False
    
    async def process_user_request(self, user_id: str, agent_type: str, 
                                 request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user request through the appropriate agent"""
        try:
            start_time = datetime.now()
            
            # Validate agent type
            if agent_type not in self.agents:
                return {
                    'success': False,
                    'error': f'Unknown agent type: {agent_type}',
                    'agent_type': agent_type
                }
            
            # Get or create session
            session_id = await self._get_or_create_session(user_id, agent_type)
            
            # Load user context and memory
            context = await self._load_user_context(user_id, agent_type, session_id)
            
            # Get agent
            agent = self.agents[agent_type]
            
            # Process request with enhanced context
            enhanced_request = {
                **request_data,
                'user_id': user_id,
                'session_id': session_id,
                'context': context,
                'system_config': self.config['agents'][agent_type]
            }
            
            # Process through agent
            response = await agent.process_enhanced_request(enhanced_request)
            
            # Calculate metrics
            processing_time = (datetime.now() - start_time).total_seconds()
            
            # Store interaction
            interaction_id = await self._store_interaction(
                user_id, agent_type, session_id, enhanced_request, response, processing_time
            )
            
            # Update memory
            await self._update_memory(user_id, agent_type, enhanced_request, response, interaction_id)
            
            # Record analytics
            await self._record_analytics(user_id, agent_type, enhanced_request, response, processing_time)
            
            # Update session
            await self._update_session(session_id, interaction_id)
            
            # Enhanced response
            enhanced_response = {
                **response,
                'interaction_id': interaction_id,
                'session_id': session_id,
                'processing_time': processing_time,
                'agent_type': agent_type,
                'timestamp': datetime.now().isoformat()
            }
            
            return enhanced_response
            
        except Exception as e:
            logger.error(f"Error processing request: {str(e)}")
            return {
                'success': False,
                'error': str(e),
                'agent_type': agent_type,
                'timestamp': datetime.now().isoformat()
            }
    
    async def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status"""
        try:
            # Get agent status
            agent_status = {}
            for agent_name, agent in self.agents.items():
                status = await agent.get_status()
                agent_status[agent_name] = status
            
            # Get analytics dashboard
            dashboard = await self.analytics_system.get_real_time_dashboard()
            
            # Get memory system status
            memory_status = await self.memory_system.get_system_status()
            
            # Get performance metrics
            performance = await self.performance_monitor.get_current_metrics()
            
            # System health
            health_report = await self.analytics_system.get_system_health_report()
            
            return {
                'system_info': {
                    'name': self.config['system']['name'],
                    'version': self.config['system']['version'],
                    'environment': self.config['system']['environment'],
                    'uptime': self._get_system_uptime(),
                    'active_sessions': len(self.active_sessions),
                    'websocket_connections': len(self.websocket_connections)
                },
                'agent_status': agent_status,
                'analytics_dashboard': dashboard,
                'memory_status': memory_status,
                'performance_metrics': performance,
                'health_report': health_report,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {str(e)}")
            return {'error': str(e)}
    
    async def optimize_system_performance(self) -> Dict[str, Any]:
        """Optimize system performance based on analytics"""
        try:
            logger.info("Starting system performance optimization...")
            
            optimization_results = {}
            
            # Memory optimization
            memory_optimization = await self.memory_system.optimize_memory()
            optimization_results['memory'] = memory_optimization
            
            # Agent performance optimization
            for agent_name, agent in self.agents.items():
                agent_optimization = await self._optimize_agent_performance(agent_name, agent)
                optimization_results[f'agent_{agent_name}'] = agent_optimization
            
            # Database optimization
            db_optimization = await self._optimize_database()
            optimization_results['database'] = db_optimization
            
            # WebSocket optimization
            ws_optimization = await self._optimize_websockets()
            optimization_results['websockets'] = ws_optimization
            
            # Update baselines
            await self._update_performance_baselines()
            
            logger.info("System performance optimization completed")
            
            return {
                'success': True,
                'optimization_results': optimization_results,
                'optimized_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error optimizing system: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def _get_or_create_session(self, user_id: str, agent_type: str) -> str:
        """Get existing session or create new one"""
        session_key = f"{user_id}_{agent_type}"
        
        if session_key in self.active_sessions:
            return self.active_sessions[session_key]['session_id']
        
        # Create new session
        session_id = f"session_{user_id}_{agent_type}_{datetime.now().timestamp()}"
        
        # Store in database
        db = get_db()
        db.execute("""
        INSERT INTO agent_sessions (session_id, agent_type, user_id, status, start_time)
        VALUES (?, ?, ?, 'active', ?)
        """, (session_id, agent_type, user_id, datetime.now().isoformat()))
        db.commit()
        
        # Cache session
        self.active_sessions[session_key] = {
            'session_id': session_id,
            'start_time': datetime.now(),
            'last_activity': datetime.now(),
            'interaction_count': 0
        }
        
        return session_id
    
    async def _load_user_context(self, user_id: str, agent_type: str, session_id: str) -> Dict[str, Any]:
        """Load comprehensive user context"""
        try:
            # Get user profile
            user_profile = await self._get_user_profile(user_id)
            
            # Get relevant memories
            memories = await self.memory_system.retrieve_memories(
                user_id=user_id,
                agent_type=agent_type,
                context={"type": "context_loading"},
                max_items=20
            )
            
            # Get session history
            session_history = await self._get_session_history(session_id)
            
            # Get user preferences for this agent
            agent_preferences = await self._get_user_agent_preferences(user_id, agent_type)
            
            return {
                'user_profile': user_profile,
                'memories': memories,
                'session_history': session_history,
                'agent_preferences': agent_preferences,
                'loaded_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error loading user context: {str(e)}")
            return {}
    
    async def _start_background_tasks(self):
        """Start background system tasks"""
        try:
            # Memory consolidation task
            asyncio.create_task(self._memory_consolidation_task())
            
            # Analytics update task
            asyncio.create_task(self._analytics_update_task())
            
            # Performance monitoring task
            asyncio.create_task(self._performance_monitoring_task())
            
            # Session cleanup task
            asyncio.create_task(self._session_cleanup_task())
            
            # Health check task
            asyncio.create_task(self._health_check_task())
            
            logger.info("Background tasks started successfully")
            
        except Exception as e:
            logger.error(f"Error starting background tasks: {str(e)}")
    
    async def _memory_consolidation_task(self):
        """Background memory consolidation"""
        while True:
            try:
                await asyncio.sleep(self.config['system']['memory_consolidation_interval'])
                await self.memory_system.consolidate_memories()
                logger.info("Memory consolidation completed")
            except Exception as e:
                logger.error(f"Memory consolidation error: {str(e)}")
    
    async def _analytics_update_task(self):
        """Background analytics updates"""
        while True:
            try:
                await asyncio.sleep(self.config['system']['analytics_update_interval'])
                # Update real-time analytics
                await self.analytics_system.update_real_time_metrics()
                logger.debug("Analytics updated")
            except Exception as e:
                logger.error(f"Analytics update error: {str(e)}")
    
    def _get_system_uptime(self) -> float:
        """Get system uptime in seconds"""
        if hasattr(self, 'start_time'):
            return (datetime.now() - self.start_time).total_seconds()
        return 0


class PerformanceMonitor:
    """System performance monitoring"""
    
    def __init__(self):
        self.metrics = {}
        self.start_time = datetime.now()
    
    async def get_current_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics"""
        try:
            import psutil
            
            return {
                'cpu_usage': psutil.cpu_percent(interval=1),
                'memory_usage': psutil.virtual_memory()._asdict(),
                'disk_usage': psutil.disk_usage('/')._asdict(),
                'network_io': psutil.net_io_counters()._asdict(),
                'process_count': len(psutil.pids()),
                'uptime': (datetime.now() - self.start_time).total_seconds()
            }
        except ImportError:
            return {
                'message': 'psutil not available for detailed metrics',
                'uptime': (datetime.now() - self.start_time).total_seconds()
            }


async def main():
    """Main system initialization and startup"""
    try:
        # Initialize system
        system = SmartAgentSystem()
        
        if await system.initialize_system():
            logger.info("🎉 Smart Agent System is ready!")
            
            # Get system status
            status = await system.get_system_status()
            print("\n" + "="*50)
            print("SMART AGENT SYSTEM STATUS")
            print("="*50)
            print(f"System: {status['system_info']['name']} v{status['system_info']['version']}")
            print(f"Environment: {status['system_info']['environment']}")
            print(f"Active Agents: {len(status['agent_status'])}")
            print(f"Active Sessions: {status['system_info']['active_sessions']}")
            print("="*50)
            
            # Keep system running
            while True:
                await asyncio.sleep(60)  # Run indefinitely
                
        else:
            logger.error("❌ Failed to initialize system")
            
    except KeyboardInterrupt:
        logger.info("System shutdown requested")
    except Exception as e:
        logger.error(f"System error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())