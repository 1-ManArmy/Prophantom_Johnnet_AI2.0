#!/usr/bin/env python3
"""
Auto Chat Feed Data Fetcher
Fetches and processes external data for conversation enhancement
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import aiohttp
import feedparser
from core.database import get_db

logger = logging.getLogger(__name__)

class AutoChatFeedFetcher:
    """Fetches external data to enhance conversations"""
    
    def __init__(self):
        self.data_sources = {
            'tech_news': 'https://feeds.feedburner.com/oreilly/radar/atom',
            'general_news': 'https://rss.cnn.com/rss/edition.rss',
            'science': 'https://www.sciencedaily.com/rss/all.xml',
            'ai_news': 'https://artificialintelligence-news.com/feed/',
            'programming': 'https://stackoverflow.blog/feed/'
        }
        
        self.trending_topics = []
        self.cached_content = {}
        self.last_fetch = {}
    
    async def fetch_trending_topics(self) -> List[Dict[str, Any]]:
        """Fetch current trending topics"""
        try:
            trending = []
            
            for source_name, url in self.data_sources.items():
                # Check if we need to refresh this source
                if self._should_refresh(source_name):
                    try:
                        feed_data = await self._fetch_feed_data(url)
                        processed_topics = self._process_feed_topics(feed_data, source_name)
                        trending.extend(processed_topics)
                        
                        self.last_fetch[source_name] = datetime.now()
                        
                    except Exception as e:
                        logger.error(f"Error fetching from {source_name}: {str(e)}")
                        continue
            
            # Sort by relevance and recency
            trending.sort(key=lambda x: (x['relevance_score'], x['timestamp']), reverse=True)
            
            # Cache top topics
            self.trending_topics = trending[:20]
            
            return self.trending_topics
            
        except Exception as e:
            logger.error(f"Error fetching trending topics: {str(e)}")
            return []
    
    async def get_conversation_context_data(self, topic: str, user_interests: List[str] = None) -> Dict[str, Any]:
        """Get contextual data for conversation topic"""
        try:
            # Search cached content first
            relevant_content = self._search_cached_content(topic, user_interests or [])
            
            if not relevant_content:
                # Fetch fresh content
                relevant_content = await self._fetch_topic_content(topic)
            
            # Prepare conversation context
            context_data = {
                'topic': topic,
                'relevant_articles': relevant_content[:5],  # Top 5 most relevant
                'trending_subtopics': self._extract_subtopics(relevant_content),
                'user_interest_match': self._calculate_interest_match(topic, user_interests or []),
                'freshness_score': self._calculate_freshness_score(relevant_content),
                'conversation_starters': self._generate_conversation_starters(relevant_content)
            }
            
            return context_data
            
        except Exception as e:
            logger.error(f"Error getting context data: {str(e)}")
            return {'topic': topic, 'error': str(e)}
    
    async def fetch_real_time_data(self, query: str) -> Dict[str, Any]:
        """Fetch real-time data for specific queries"""
        try:
            # This would integrate with real-time APIs
            # For now, we'll simulate with cached data
            
            search_results = []
            
            # Search through cached content
            for content in self.cached_content.values():
                if query.lower() in content.get('title', '').lower() or \
                   query.lower() in content.get('summary', '').lower():
                    search_results.append(content)
            
            # Sort by relevance
            search_results.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
            
            return {
                'query': query,
                'results': search_results[:10],
                'timestamp': datetime.now().isoformat(),
                'result_count': len(search_results)
            }
            
        except Exception as e:
            logger.error(f"Error fetching real-time data: {str(e)}")
            return {'query': query, 'error': str(e)}
    
    async def get_conversation_enhancers(self, conversation_history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get data to enhance ongoing conversation"""
        try:
            # Analyze conversation for key topics
            topics = self._extract_conversation_topics(conversation_history)
            
            # Get relevant external data
            enhancement_data = {}
            
            for topic in topics[:3]:  # Top 3 topics
                topic_data = await self.get_conversation_context_data(topic)
                enhancement_data[topic] = topic_data
            
            # Generate conversation suggestions
            suggestions = self._generate_conversation_suggestions(enhancement_data)
            
            return {
                'topics_identified': topics,
                'enhancement_data': enhancement_data,
                'conversation_suggestions': suggestions,
                'data_freshness': self._get_data_freshness_summary()
            }
            
        except Exception as e:
            logger.error(f"Error getting conversation enhancers: {str(e)}")
            return {'error': str(e)}
    
    async def _fetch_feed_data(self, url: str) -> Dict[str, Any]:
        """Fetch data from RSS/Atom feed"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, timeout=10) as response:
                    if response.status == 200:
                        content = await response.text()
                        feed = feedparser.parse(content)
                        return feed
                    else:
                        logger.warning(f"HTTP {response.status} when fetching {url}")
                        return {}
        except Exception as e:
            logger.error(f"Error fetching feed from {url}: {str(e)}")
            return {}
    
    def _process_feed_topics(self, feed_data: Dict[str, Any], source_name: str) -> List[Dict[str, Any]]:
        """Process feed data into topic format"""
        topics = []
        
        try:
            entries = feed_data.get('entries', [])
            
            for entry in entries[:10]:  # Top 10 entries per source
                topic = {
                    'title': entry.get('title', ''),
                    'summary': entry.get('summary', ''),
                    'link': entry.get('link', ''),
                    'published': entry.get('published', ''),
                    'source': source_name,
                    'timestamp': datetime.now().isoformat(),
                    'relevance_score': self._calculate_relevance_score(entry, source_name)
                }
                
                # Cache the content
                content_id = f"{source_name}_{hash(topic['title'])}"
                self.cached_content[content_id] = topic
                
                topics.append(topic)
                
        except Exception as e:
            logger.error(f"Error processing feed topics: {str(e)}")
        
        return topics
    
    def _should_refresh(self, source_name: str) -> bool:
        """Check if source data should be refreshed"""
        if source_name not in self.last_fetch:
            return True
        
        # Refresh every 30 minutes
        refresh_interval = timedelta(minutes=30)
        return datetime.now() - self.last_fetch[source_name] > refresh_interval
    
    def _search_cached_content(self, topic: str, user_interests: List[str]) -> List[Dict[str, Any]]:
        """Search cached content for relevant information"""
        relevant = []
        topic_lower = topic.lower()
        
        for content in self.cached_content.values():
            relevance = 0
            
            # Check title relevance
            if topic_lower in content.get('title', '').lower():
                relevance += 0.5
            
            # Check summary relevance
            if topic_lower in content.get('summary', '').lower():
                relevance += 0.3
            
            # Check user interest alignment
            for interest in user_interests:
                if interest.lower() in content.get('title', '').lower() or \
                   interest.lower() in content.get('summary', '').lower():
                    relevance += 0.2
            
            if relevance > 0:
                content_copy = content.copy()
                content_copy['relevance_score'] = relevance
                relevant.append(content_copy)
        
        # Sort by relevance
        relevant.sort(key=lambda x: x['relevance_score'], reverse=True)
        return relevant
    
    def _calculate_relevance_score(self, entry: Dict[str, Any], source_name: str) -> float:
        """Calculate relevance score for content"""
        score = 0.5  # Base score
        
        # Source reliability weight
        source_weights = {
            'tech_news': 0.9,
            'ai_news': 0.9,
            'programming': 0.8,
            'science': 0.8,
            'general_news': 0.6
        }
        
        score += source_weights.get(source_name, 0.5)
        
        # Recency bonus
        published_str = entry.get('published', '')
        if published_str:
            try:
                published_date = datetime.strptime(published_str[:19], '%Y-%m-%dT%H:%M:%S')
                hours_old = (datetime.now() - published_date).total_seconds() / 3600
                if hours_old < 24:
                    score += 0.3  # Recent content bonus
                elif hours_old < 72:
                    score += 0.1
            except:
                pass
        
        return min(1.0, score)
    
    def _extract_conversation_topics(self, conversation_history: List[Dict[str, Any]]) -> List[str]:
        """Extract key topics from conversation history"""
        topics = []
        
        # Simple keyword extraction (in production, would use NLP)
        keywords = set()
        
        for message in conversation_history[-10:]:  # Last 10 messages
            content = message.get('content', message.get('message', ''))
            words = content.lower().split()
            
            # Filter for meaningful words (length > 3)
            meaningful_words = [word for word in words if len(word) > 3]
            keywords.update(meaningful_words[:5])  # Top 5 words per message
        
        # Convert to topics (would use more sophisticated NLP in production)
        topics = list(keywords)[:10]  # Top 10 topics
        
        return topics
    
    def _generate_conversation_starters(self, content: List[Dict[str, Any]]) -> List[str]:
        """Generate conversation starters from content"""
        starters = []
        
        for item in content[:3]:
            title = item.get('title', '')
            if title:
                starters.append(f"Did you hear about {title}?")
                starters.append(f"What do you think about the recent news on {title}?")
        
        return starters[:5]
    
    def _calculate_interest_match(self, topic: str, user_interests: List[str]) -> float:
        """Calculate how well topic matches user interests"""
        if not user_interests:
            return 0.5
        
        topic_lower = topic.lower()
        matches = sum(1 for interest in user_interests if interest.lower() in topic_lower)
        
        return min(1.0, matches / len(user_interests))
    
    def _get_data_freshness_summary(self) -> Dict[str, Any]:
        """Get summary of data freshness"""
        freshness = {}
        
        for source, last_fetch_time in self.last_fetch.items():
            minutes_old = (datetime.now() - last_fetch_time).total_seconds() / 60
            freshness[source] = {
                'minutes_old': int(minutes_old),
                'status': 'fresh' if minutes_old < 30 else 'stale'
            }
        
        return freshness