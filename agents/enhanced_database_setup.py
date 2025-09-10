#!/usr/bin/env python3
"""
Enhanced Database Schema for Smart Agents
Comprehensive database setup with advanced analytics and memory support
"""

import sqlite3
import logging
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

class EnhancedDatabaseSetup:
    """Enhanced database setup for smart agent system"""
    
    def __init__(self, db_path: str = "agents.db"):
        self.db_path = db_path
    
    def create_all_tables(self):
        """Create all required tables for the smart agent system"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Core agent tables
            self._create_agent_tables(cursor)
            
            # Analytics tables
            self._create_analytics_tables(cursor)
            
            # Memory system tables
            self._create_memory_tables(cursor)
            
            # WebSocket and real-time tables
            self._create_realtime_tables(cursor)
            
            # Training and tuning tables
            self._create_training_tables(cursor)
            
            # User interaction tables
            self._create_user_tables(cursor)
            
            # System monitoring tables
            self._create_monitoring_tables(cursor)
            
            # Create indexes for performance
            self._create_indexes(cursor)
            
            # Insert default data
            self._insert_default_data(cursor)
            
            conn.commit()
            conn.close()
            
            logger.info("Enhanced database schema created successfully")
            
        except Exception as e:
            logger.error(f"Error creating database schema: {str(e)}")
            raise
    
    def _create_agent_tables(self, cursor):
        """Create core agent tables"""
        
        # Agents registry
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_type TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            model_name TEXT NOT NULL,
            specialization TEXT,
            capabilities TEXT, -- JSON array
            config TEXT, -- JSON configuration
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Agent sessions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            status TEXT DEFAULT 'active',
            context_data TEXT, -- JSON
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            total_interactions INTEGER DEFAULT 0,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Agent interactions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id TEXT UNIQUE NOT NULL,
            session_id TEXT NOT NULL,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            request_type TEXT,
            request_data TEXT, -- JSON
            response_data TEXT, -- JSON
            response_time REAL,
            success BOOLEAN,
            error_message TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES agent_sessions (session_id),
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
    
    def _create_analytics_tables(self, cursor):
        """Create analytics and metrics tables"""
        
        # Agent metrics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS agent_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            response_time REAL NOT NULL,
            user_satisfaction REAL,
            task_completion_rate REAL,
            engagement_score REAL,
            specialization_effectiveness REAL,
            error_rate REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Interaction analysis
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS interaction_analysis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            interaction_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            interaction_type TEXT,
            success_score REAL,
            complexity_level INTEGER,
            features_used TEXT, -- JSON array
            response_quality REAL,
            user_feedback REAL,
            contextual_relevance REAL,
            sentiment_score REAL,
            topic_classification TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (interaction_id) REFERENCES agent_interactions (interaction_id),
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Performance baselines
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_baselines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_type TEXT NOT NULL,
            metric_name TEXT NOT NULL,
            baseline_value REAL NOT NULL,
            confidence_interval REAL,
            sample_size INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(agent_type, metric_name),
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # System alerts
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_type TEXT NOT NULL,
            severity TEXT NOT NULL, -- critical, warning, info
            agent_type TEXT,
            user_id TEXT,
            title TEXT NOT NULL,
            description TEXT,
            alert_data TEXT, -- JSON
            status TEXT DEFAULT 'active', -- active, acknowledged, resolved
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            acknowledged_at TIMESTAMP,
            resolved_at TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
    
    def _create_memory_tables(self, cursor):
        """Create memory system tables"""
        
        # Universal memory items
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id TEXT UNIQUE NOT NULL,
            memory_type TEXT NOT NULL, -- episodic, semantic, procedural, emotional
            agent_type TEXT,
            user_id TEXT,
            content TEXT NOT NULL,
            metadata TEXT, -- JSON
            importance_score REAL DEFAULT 0.5,
            access_count INTEGER DEFAULT 0,
            last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            tags TEXT, -- JSON array
            embeddings BLOB, -- Vector embeddings
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Memory associations
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_associations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_item_id TEXT NOT NULL,
            target_item_id TEXT NOT NULL,
            association_type TEXT NOT NULL,
            strength REAL DEFAULT 0.5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (source_item_id) REFERENCES memory_items (item_id),
            FOREIGN KEY (target_item_id) REFERENCES memory_items (item_id)
        )
        """)
        
        # Context snapshots
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS context_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            snapshot_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            session_id TEXT,
            context_data TEXT NOT NULL, -- JSON
            memory_state TEXT, -- JSON
            trigger_event TEXT,
            importance_score REAL DEFAULT 0.5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type),
            FOREIGN KEY (session_id) REFERENCES agent_sessions (session_id)
        )
        """)
        
        # Memory consolidation log
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS memory_consolidation_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consolidation_id TEXT UNIQUE NOT NULL,
            agent_type TEXT,
            consolidation_type TEXT NOT NULL,
            items_processed INTEGER,
            items_consolidated INTEGER,
            items_archived INTEGER,
            performance_impact REAL,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            status TEXT DEFAULT 'running',
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
    
    def _create_realtime_tables(self, cursor):
        """Create WebSocket and real-time communication tables"""
        
        # WebSocket connections
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS websocket_connections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            connection_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            client_info TEXT, -- JSON
            connected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_ping TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'connected',
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Real-time events
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS realtime_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_id TEXT UNIQUE NOT NULL,
            connection_id TEXT NOT NULL,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            event_type TEXT NOT NULL,
            event_data TEXT, -- JSON
            processed BOOLEAN DEFAULT FALSE,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (connection_id) REFERENCES websocket_connections (connection_id),
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Message queue
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS message_queue (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            message_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            message_type TEXT NOT NULL,
            priority INTEGER DEFAULT 1,
            payload TEXT NOT NULL, -- JSON
            status TEXT DEFAULT 'pending',
            retry_count INTEGER DEFAULT 0,
            max_retries INTEGER DEFAULT 3,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            scheduled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processed_at TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
    
    def _create_training_tables(self, cursor):
        """Create training and tuning tables"""
        
        # Training sessions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            training_type TEXT NOT NULL,
            model_version TEXT,
            dataset_info TEXT, -- JSON
            hyperparameters TEXT, -- JSON
            training_config TEXT, -- JSON
            status TEXT DEFAULT 'pending',
            progress REAL DEFAULT 0.0,
            started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            results TEXT, -- JSON
            performance_metrics TEXT, -- JSON
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Model versions
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            version_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            version_name TEXT NOT NULL,
            model_path TEXT,
            config_path TEXT,
            performance_metrics TEXT, -- JSON
            is_active BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            deployed_at TIMESTAMP,
            deprecated_at TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Training feedback
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS training_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            user_id TEXT NOT NULL,
            interaction_id TEXT,
            feedback_type TEXT NOT NULL,
            feedback_data TEXT NOT NULL, -- JSON
            rating REAL,
            comments TEXT,
            processed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type),
            FOREIGN KEY (interaction_id) REFERENCES agent_interactions (interaction_id)
        )
        """)
    
    def _create_user_tables(self, cursor):
        """Create user-related tables"""
        
        # User profiles
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT UNIQUE NOT NULL,
            username TEXT,
            email TEXT,
            preferences TEXT, -- JSON
            interaction_patterns TEXT, -- JSON
            learning_profile TEXT, -- JSON
            privacy_settings TEXT, -- JSON
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # User agent preferences
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_agent_preferences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            agent_type TEXT NOT NULL,
            preferences TEXT NOT NULL, -- JSON
            satisfaction_history TEXT, -- JSON array
            usage_frequency REAL DEFAULT 0.0,
            last_used TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, agent_type),
            FOREIGN KEY (user_id) REFERENCES user_profiles (user_id),
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # User feedback
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            feedback_id TEXT UNIQUE NOT NULL,
            user_id TEXT NOT NULL,
            agent_type TEXT,
            interaction_id TEXT,
            feedback_type TEXT NOT NULL,
            rating REAL,
            feedback_text TEXT,
            categories TEXT, -- JSON array
            sentiment REAL,
            processed BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES user_profiles (user_id),
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type),
            FOREIGN KEY (interaction_id) REFERENCES agent_interactions (interaction_id)
        )
        """)
    
    def _create_monitoring_tables(self, cursor):
        """Create system monitoring tables"""
        
        # System health metrics
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_health (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            metric_name TEXT NOT NULL,
            metric_value REAL NOT NULL,
            metric_unit TEXT,
            agent_type TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Resource usage
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS resource_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resource_type TEXT NOT NULL, -- cpu, memory, disk, network
            agent_type TEXT,
            usage_value REAL NOT NULL,
            max_value REAL,
            usage_percent REAL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Error logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            error_id TEXT UNIQUE NOT NULL,
            agent_type TEXT,
            user_id TEXT,
            error_type TEXT NOT NULL,
            error_message TEXT NOT NULL,
            error_details TEXT, -- JSON
            stack_trace TEXT,
            severity TEXT DEFAULT 'error',
            resolved BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
        
        # Performance logs
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS performance_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            log_id TEXT UNIQUE NOT NULL,
            agent_type TEXT NOT NULL,
            operation_type TEXT NOT NULL,
            execution_time REAL NOT NULL,
            resource_usage TEXT, -- JSON
            success BOOLEAN DEFAULT TRUE,
            metadata TEXT, -- JSON
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (agent_type) REFERENCES agents (agent_type)
        )
        """)
    
    def _create_indexes(self, cursor):
        """Create performance indexes"""
        indexes = [
            # Agent tables indexes
            "CREATE INDEX IF NOT EXISTS idx_agents_type ON agents (agent_type)",
            "CREATE INDEX IF NOT EXISTS idx_sessions_agent_user ON agent_sessions (agent_type, user_id)",
            "CREATE INDEX IF NOT EXISTS idx_interactions_session ON agent_interactions (session_id)",
            "CREATE INDEX IF NOT EXISTS idx_interactions_timestamp ON agent_interactions (timestamp)",
            
            # Analytics indexes
            "CREATE INDEX IF NOT EXISTS idx_metrics_agent_time ON agent_metrics (agent_type, timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_metrics_user_time ON agent_metrics (user_id, timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_analysis_interaction ON interaction_analysis (interaction_id)",
            "CREATE INDEX IF NOT EXISTS idx_alerts_status ON system_alerts (status, created_at)",
            
            # Memory indexes
            "CREATE INDEX IF NOT EXISTS idx_memory_type_agent ON memory_items (memory_type, agent_type)",
            "CREATE INDEX IF NOT EXISTS idx_memory_user_time ON memory_items (user_id, created_at)",
            "CREATE INDEX IF NOT EXISTS idx_memory_importance ON memory_items (importance_score)",
            "CREATE INDEX IF NOT EXISTS idx_snapshots_agent_user ON context_snapshots (agent_type, user_id)",
            
            # Real-time indexes
            "CREATE INDEX IF NOT EXISTS idx_connections_agent ON websocket_connections (agent_type, status)",
            "CREATE INDEX IF NOT EXISTS idx_events_processed ON realtime_events (processed, timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_queue_status ON message_queue (status, priority)",
            
            # Training indexes
            "CREATE INDEX IF NOT EXISTS idx_training_agent_status ON training_sessions (agent_type, status)",
            "CREATE INDEX IF NOT EXISTS idx_versions_agent_active ON model_versions (agent_type, is_active)",
            "CREATE INDEX IF NOT EXISTS idx_feedback_processed ON training_feedback (processed, created_at)",
            
            # User indexes
            "CREATE INDEX IF NOT EXISTS idx_user_profiles_last_active ON user_profiles (last_active)",
            "CREATE INDEX IF NOT EXISTS idx_user_preferences_agent ON user_agent_preferences (user_id, agent_type)",
            "CREATE INDEX IF NOT EXISTS idx_feedback_user_time ON user_feedback (user_id, created_at)",
            
            # Monitoring indexes
            "CREATE INDEX IF NOT EXISTS idx_health_metric_time ON system_health (metric_name, timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_resource_agent_time ON resource_usage (agent_type, timestamp)",
            "CREATE INDEX IF NOT EXISTS idx_errors_resolved ON error_logs (resolved, severity)",
            "CREATE INDEX IF NOT EXISTS idx_performance_agent_op ON performance_logs (agent_type, operation_type)"
        ]
        
        for index in indexes:
            cursor.execute(index)
    
    def _insert_default_data(self, cursor):
        """Insert default data for system initialization"""
        
        # Default agents
        agents_data = [
            ('auto_chat', 'Auto Chat Agent', 'Automated conversation and chat assistance', 'phi3:14b', 'conversation_automation', '["natural_language", "context_awareness", "multi_turn_dialog"]'),
            ('chat_revive', 'Chat Revival Agent', 'Chat engagement and conversation revival', 'gemma2:2b', 'engagement_optimization', '["engagement_analysis", "conversation_revival", "user_retention"]'),
            ('cv_smash', 'CV Optimization Agent', 'Resume and CV optimization specialist', 'qwen2.5:7b', 'resume_optimization', '["resume_analysis", "skill_enhancement", "career_guidance"]'),
            ('emo_ai', 'Emotional Support Agent', 'Emotional intelligence and support', 'llama3.1:8b', 'emotional_support', '["emotion_recognition", "empathy", "mental_health_support"]'),
            ('pdf_mind', 'Document Analysis Agent', 'PDF and document analysis specialist', 'mistral:7b', 'document_analysis', '["pdf_processing", "content_extraction", "document_intelligence"]'),
            ('tok_boost', 'Social Media Agent', 'Social media optimization and management', 'deepseek-coder:6.7b', 'social_media_optimization', '["content_creation", "engagement_optimization", "trend_analysis"]'),
            ('you_gen', 'Content Generation Agent', 'Creative content generation specialist', 'llama3.2:3b', 'content_generation', '["creative_writing", "content_strategy", "multimedia_content"]'),
            ('agent_x', 'Adaptive Intelligence Agent', 'Advanced adaptive AI with learning capabilities', 'codellama:7b', 'adaptive_intelligence', '["machine_learning", "pattern_recognition", "adaptive_behavior"]')
        ]
        
        for agent_data in agents_data:
            cursor.execute("""
            INSERT OR IGNORE INTO agents (agent_type, name, description, model_name, specialization, capabilities)
            VALUES (?, ?, ?, ?, ?, ?)
            """, agent_data)
        
        # Default performance baselines
        baseline_data = [
            ('response_time', 2.0, 0.3),
            ('user_satisfaction', 0.8, 0.1),
            ('task_completion_rate', 0.85, 0.1),
            ('engagement_score', 0.7, 0.15),
            ('specialization_effectiveness', 0.75, 0.12)
        ]
        
        for agent_type in [row[0] for row in agents_data]:
            for metric_name, baseline_value, confidence_interval in baseline_data:
                cursor.execute("""
                INSERT OR IGNORE INTO performance_baselines (agent_type, metric_name, baseline_value, confidence_interval, sample_size)
                VALUES (?, ?, ?, ?, ?)
                """, (agent_type, metric_name, baseline_value, confidence_interval, 100))


def setup_enhanced_database(db_path: str = None) -> bool:
    """Setup the enhanced database schema"""
    try:
        if db_path is None:
            db_path = "/workspaces/Prophantom_Johnnet_AI2.0/core/agents.db"
        
        db_setup = EnhancedDatabaseSetup(db_path)
        db_setup.create_all_tables()
        
        print(f"✅ Enhanced database schema created successfully at: {db_path}")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up database: {str(e)}")
        return False

if __name__ == "__main__":
    setup_enhanced_database()