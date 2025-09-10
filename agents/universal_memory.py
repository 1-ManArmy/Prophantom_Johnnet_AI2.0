#!/usr/bin/env python3
"""
Universal Agent Memory System
Advanced memory and context management for all agents
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import sqlite3
from core.database import get_db

logger = logging.getLogger(__name__)

@dataclass
class MemoryItem:
    """Represents a single memory item"""
    memory_id: str
    agent_type: str
    user_id: str
    content: Dict[str, Any]
    memory_type: str  # episodic, semantic, procedural, emotional
    importance_score: float
    access_count: int
    created_at: datetime
    last_accessed: datetime
    decay_factor: float

@dataclass
class ContextSnapshot:
    """Represents a context snapshot at a point in time"""
    snapshot_id: str
    user_id: str
    agent_type: str
    context_data: Dict[str, Any]
    interaction_count: int
    emotional_state: Dict[str, float]
    preferences: Dict[str, Any]
    timestamp: datetime

class UniversalMemorySystem:
    """Advanced memory system for all agents"""
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.short_term_memory = {}  # Session-based memory
        self.working_memory = {}     # Active processing memory
        self.memory_consolidation_threshold = 0.7
        self.max_short_term_items = 50
        
        # Memory type weights
        self.memory_weights = {
            'episodic': 1.0,    # Events and experiences
            'semantic': 0.9,    # Facts and knowledge
            'procedural': 0.8,  # Skills and procedures
            'emotional': 1.1    # Emotional associations
        }
    
    async def store_memory(self, user_id: str, content: Dict[str, Any], 
                          memory_type: str = 'episodic', importance: float = 0.5) -> str:
        """Store a new memory item"""
        try:
            memory_id = f"{self.agent_type}_{user_id}_{datetime.now().timestamp()}"
            
            memory_item = MemoryItem(
                memory_id=memory_id,
                agent_type=self.agent_type,
                user_id=user_id,
                content=content,
                memory_type=memory_type,
                importance_score=importance,
                access_count=0,
                created_at=datetime.now(),
                last_accessed=datetime.now(),
                decay_factor=1.0
            )
            
            # Store in short-term memory first
            if user_id not in self.short_term_memory:
                self.short_term_memory[user_id] = []
            
            self.short_term_memory[user_id].append(memory_item)
            
            # Manage short-term memory size
            if len(self.short_term_memory[user_id]) > self.max_short_term_items:
                await self._consolidate_memories(user_id)
            
            # Store in database for persistence
            await self._store_memory_persistent(memory_item)
            
            logger.info(f"Stored {memory_type} memory for user {user_id}")
            return memory_id
            
        except Exception as e:
            logger.error(f"Error storing memory: {str(e)}")
            return ""
    
    async def retrieve_memories(self, user_id: str, query: str = None, 
                               memory_type: str = None, limit: int = 10) -> List[MemoryItem]:
        """Retrieve relevant memories"""
        try:
            memories = []
            
            # Get from short-term memory
            if user_id in self.short_term_memory:
                memories.extend(self.short_term_memory[user_id])
            
            # Get from persistent storage
            persistent_memories = await self._retrieve_persistent_memories(
                user_id, query, memory_type, limit * 2
            )
            memories.extend(persistent_memories)
            
            # Filter and rank memories
            if query:
                memories = self._filter_memories_by_relevance(memories, query)
            
            if memory_type:
                memories = [m for m in memories if m.memory_type == memory_type]
            
            # Sort by importance and recency
            memories.sort(key=lambda m: (
                m.importance_score * self.memory_weights.get(m.memory_type, 1.0),
                m.last_accessed.timestamp()
            ), reverse=True)
            
            # Update access information
            for memory in memories[:limit]:
                memory.access_count += 1
                memory.last_accessed = datetime.now()
                await self._update_memory_access(memory)
            
            return memories[:limit]
            
        except Exception as e:
            logger.error(f"Error retrieving memories: {str(e)}")
            return []
    
    async def update_context(self, user_id: str, context_data: Dict[str, Any]) -> str:
        """Update user context with new information"""
        try:
            snapshot_id = f"context_{user_id}_{datetime.now().timestamp()}"
            
            # Get current context or create new
            current_context = await self._get_current_context(user_id)
            
            # Merge with new data
            if current_context:
                merged_context = {**current_context.context_data, **context_data}
                interaction_count = current_context.interaction_count + 1
                emotional_state = self._update_emotional_state(
                    current_context.emotional_state, 
                    context_data.get('emotional_indicators', {})
                )
            else:
                merged_context = context_data
                interaction_count = 1
                emotional_state = context_data.get('emotional_indicators', {})
            
            # Create new context snapshot
            snapshot = ContextSnapshot(
                snapshot_id=snapshot_id,
                user_id=user_id,
                agent_type=self.agent_type,
                context_data=merged_context,
                interaction_count=interaction_count,
                emotional_state=emotional_state,
                preferences=context_data.get('preferences', {}),
                timestamp=datetime.now()
            )
            
            # Store context snapshot
            await self._store_context_snapshot(snapshot)
            
            # Update working memory
            self.working_memory[user_id] = snapshot
            
            return snapshot_id
            
        except Exception as e:
            logger.error(f"Error updating context: {str(e)}")
            return ""
    
    async def get_contextual_memories(self, user_id: str, current_topic: str = None) -> Dict[str, Any]:
        """Get memories relevant to current context"""
        try:
            # Get current context
            current_context = self.working_memory.get(user_id) or await self._get_current_context(user_id)
            
            if not current_context:
                return {'memories': [], 'context': {}}
            
            # Retrieve relevant memories
            query = current_topic or "general interaction"
            relevant_memories = await self.retrieve_memories(user_id, query, limit=5)
            
            # Get emotional context
            emotional_memories = await self.retrieve_memories(
                user_id, memory_type='emotional', limit=3
            )
            
            # Get procedural memories (how to handle similar situations)
            procedural_memories = await self.retrieve_memories(
                user_id, memory_type='procedural', limit=2
            )
            
            return {
                'current_context': asdict(current_context),
                'relevant_memories': [asdict(m) for m in relevant_memories],
                'emotional_memories': [asdict(m) for m in emotional_memories],
                'procedural_memories': [asdict(m) for m in procedural_memories],
                'total_interactions': current_context.interaction_count,
                'emotional_state': current_context.emotional_state
            }
            
        except Exception as e:
            logger.error(f"Error getting contextual memories: {str(e)}")
            return {'error': str(e)}
    
    async def consolidate_learning(self, user_id: str) -> Dict[str, Any]:
        """Consolidate memories and extract learning patterns"""
        try:
            # Get all memories for user
            all_memories = await self.retrieve_memories(user_id, limit=100)
            
            if not all_memories:
                return {'message': 'No memories to consolidate'}
            
            # Analyze patterns
            patterns = self._analyze_memory_patterns(all_memories)
            
            # Extract user preferences
            preferences = self._extract_user_preferences(all_memories)
            
            # Identify successful interaction patterns
            successful_patterns = self._identify_successful_patterns(all_memories)
            
            # Create consolidated learning memory
            learning_content = {
                'patterns': patterns,
                'preferences': preferences,
                'successful_patterns': successful_patterns,
                'consolidation_date': datetime.now().isoformat(),
                'memory_count': len(all_memories)
            }
            
            # Store as semantic memory
            learning_memory_id = await self.store_memory(
                user_id, learning_content, 'semantic', importance=0.9
            )
            
            return {
                'success': True,
                'learning_memory_id': learning_memory_id,
                'patterns_found': len(patterns),
                'preferences_extracted': len(preferences),
                'consolidation_summary': learning_content
            }
            
        except Exception as e:
            logger.error(f"Error consolidating learning: {str(e)}")
            return {'error': str(e)}
    
    def _filter_memories_by_relevance(self, memories: List[MemoryItem], query: str) -> List[MemoryItem]:
        """Filter memories by relevance to query"""
        query_lower = query.lower()
        relevant = []
        
        for memory in memories:
            relevance_score = 0
            content_str = json.dumps(memory.content).lower()
            
            # Simple keyword matching (in production, would use semantic similarity)
            if query_lower in content_str:
                relevance_score += 0.5
            
            query_words = query_lower.split()
            for word in query_words:
                if word in content_str:
                    relevance_score += 0.1
            
            # Factor in memory importance and type
            total_score = relevance_score * memory.importance_score * \
                         self.memory_weights.get(memory.memory_type, 1.0)
            
            if total_score > 0.1:  # Threshold for relevance
                memory.relevance_score = total_score
                relevant.append(memory)
        
        return relevant
    
    def _update_emotional_state(self, current_state: Dict[str, float], 
                               new_indicators: Dict[str, float]) -> Dict[str, float]:
        """Update emotional state with new indicators"""
        updated_state = current_state.copy()
        
        for emotion, value in new_indicators.items():
            if emotion in updated_state:
                # Weighted average with decay
                updated_state[emotion] = (updated_state[emotion] * 0.7) + (value * 0.3)
            else:
                updated_state[emotion] = value
        
        return updated_state
    
    def _analyze_memory_patterns(self, memories: List[MemoryItem]) -> List[Dict[str, Any]]:
        """Analyze patterns in memory data"""
        patterns = []
        
        # Group by memory type
        type_groups = {}
        for memory in memories:
            if memory.memory_type not in type_groups:
                type_groups[memory.memory_type] = []
            type_groups[memory.memory_type].append(memory)
        
        # Analyze each type
        for mem_type, mem_list in type_groups.items():
            if len(mem_list) >= 3:  # Need minimum memories to find patterns
                pattern = {
                    'type': mem_type,
                    'frequency': len(mem_list),
                    'avg_importance': sum(m.importance_score for m in mem_list) / len(mem_list),
                    'common_themes': self._extract_common_themes(mem_list)
                }
                patterns.append(pattern)
        
        return patterns
    
    def _extract_common_themes(self, memories: List[MemoryItem]) -> List[str]:
        """Extract common themes from memories"""
        # Simple implementation - in production would use NLP
        themes = []
        
        all_content = []
        for memory in memories:
            content_str = json.dumps(memory.content)
            all_content.append(content_str)
        
        # Find common words/phrases
        combined_content = " ".join(all_content).lower()
        words = combined_content.split()
        
        # Get most frequent meaningful words
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Filter short words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top themes
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        themes = [word for word, freq in sorted_words[:5] if freq >= 2]
        
        return themes
    
    async def _store_memory_persistent(self, memory: MemoryItem):
        """Store memory in persistent database"""
        try:
            db = get_db()
            
            query = """
            INSERT INTO agent_memories (memory_id, agent_type, user_id, content, 
                                      memory_type, importance_score, access_count, 
                                      created_at, last_accessed, decay_factor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                memory.memory_id,
                memory.agent_type,
                memory.user_id,
                json.dumps(memory.content),
                memory.memory_type,
                memory.importance_score,
                memory.access_count,
                memory.created_at.isoformat(),
                memory.last_accessed.isoformat(),
                memory.decay_factor
            )
            
            db.execute(query, params)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing persistent memory: {str(e)}")
    
    async def get_memory_analytics(self, user_id: str) -> Dict[str, Any]:
        """Get analytics about user's memory patterns"""
        try:
            memories = await self.retrieve_memories(user_id, limit=50)
            
            if not memories:
                return {'message': 'No memory data available'}
            
            # Calculate analytics
            total_memories = len(memories)
            memory_types = {}
            avg_importance = 0
            
            for memory in memories:
                memory_types[memory.memory_type] = memory_types.get(memory.memory_type, 0) + 1
                avg_importance += memory.importance_score
            
            avg_importance /= total_memories if total_memories > 0 else 1
            
            # Memory age distribution
            now = datetime.now()
            age_distribution = {
                'recent': 0,    # < 1 day
                'short_term': 0,  # 1-7 days
                'medium_term': 0, # 1-4 weeks
                'long_term': 0    # > 4 weeks
            }
            
            for memory in memories:
                age = now - memory.created_at
                if age < timedelta(days=1):
                    age_distribution['recent'] += 1
                elif age < timedelta(days=7):
                    age_distribution['short_term'] += 1
                elif age < timedelta(weeks=4):
                    age_distribution['medium_term'] += 1
                else:
                    age_distribution['long_term'] += 1
            
            return {
                'agent_type': self.agent_type,
                'total_memories': total_memories,
                'memory_types': memory_types,
                'average_importance': round(avg_importance, 2),
                'age_distribution': age_distribution,
                'most_accessed': max(memories, key=lambda m: m.access_count).memory_id if memories else None,
                'memory_efficiency': self._calculate_memory_efficiency(memories)
            }
            
        except Exception as e:
            logger.error(f"Error getting memory analytics: {str(e)}")
            return {'error': str(e)}
    
    def _calculate_memory_efficiency(self, memories: List[MemoryItem]) -> float:
        """Calculate memory system efficiency"""
        if not memories:
            return 0.0
        
        # Efficiency based on access patterns and importance alignment
        total_score = 0
        for memory in memories:
            # Higher importance memories should be accessed more
            expected_access = memory.importance_score * 10
            actual_access = memory.access_count
            
            if expected_access > 0:
                efficiency = min(1.0, actual_access / expected_access)
                total_score += efficiency
        
        return total_score / len(memories)