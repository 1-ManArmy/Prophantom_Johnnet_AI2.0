#!/usr/bin/env python3
"""
Advanced Agent Analytics System
Comprehensive analytics and performance monitoring for all agents
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import numpy as np
from core.database import get_db

logger = logging.getLogger(__name__)

@dataclass
class AgentMetrics:
    """Core metrics for agent performance"""
    agent_type: str
    user_id: str
    response_time: float
    user_satisfaction: float
    task_completion_rate: float
    engagement_score: float
    specialization_effectiveness: float
    error_rate: float
    timestamp: datetime

@dataclass
class InteractionAnalysis:
    """Analysis of user-agent interactions"""
    interaction_id: str
    agent_type: str
    user_id: str
    interaction_type: str
    success_score: float
    complexity_level: int
    features_used: List[str]
    response_quality: float
    user_feedback: Optional[float]
    contextual_relevance: float
    timestamp: datetime

class AdvancedAnalyticsSystem:
    """Advanced analytics for all agents"""
    
    def __init__(self):
        self.metrics_cache = {}
        self.analysis_cache = {}
        self.performance_baselines = {
            'response_time': 2.0,
            'user_satisfaction': 0.8,
            'task_completion': 0.85,
            'engagement': 0.7,
            'specialization_effectiveness': 0.75
        }
        
        # Analytics configuration
        self.analytics_config = {
            'cache_duration': 300,  # 5 minutes
            'baseline_update_interval': 86400,  # 24 hours
            'min_samples_for_analysis': 10,
            'performance_decay_factor': 0.95
        }
    
    async def record_interaction(self, agent_type: str, user_id: str, 
                               interaction_data: Dict[str, Any]) -> str:
        """Record and analyze an interaction"""
        try:
            interaction_id = f"{agent_type}_{user_id}_{datetime.now().timestamp()}"
            
            # Extract metrics from interaction
            metrics = self._extract_metrics(agent_type, user_id, interaction_data)
            
            # Analyze interaction quality
            analysis = self._analyze_interaction(interaction_id, agent_type, user_id, interaction_data)
            
            # Store metrics and analysis
            await self._store_metrics(metrics)
            await self._store_analysis(analysis)
            
            # Update real-time performance indicators
            await self._update_performance_indicators(agent_type, user_id, metrics, analysis)
            
            # Check for performance anomalies
            anomalies = await self._detect_anomalies(agent_type, metrics)
            
            return interaction_id
            
        except Exception as e:
            logger.error(f"Error recording interaction: {str(e)}")
            return ""
    
    async def get_agent_performance(self, agent_type: str, time_range: int = 24) -> Dict[str, Any]:
        """Get comprehensive performance analysis for an agent"""
        try:
            end_time = datetime.now()
            start_time = end_time - timedelta(hours=time_range)
            
            # Get metrics for time range
            metrics = await self._get_metrics_by_timerange(agent_type, start_time, end_time)
            
            if not metrics:
                return {'message': f'No metrics available for {agent_type}'}
            
            # Calculate performance statistics
            performance_stats = self._calculate_performance_stats(metrics)
            
            # Get trend analysis
            trend_analysis = self._analyze_performance_trends(metrics)
            
            # Get user satisfaction breakdown
            satisfaction_analysis = await self._analyze_user_satisfaction(agent_type, start_time, end_time)
            
            # Get feature usage statistics
            feature_usage = await self._analyze_feature_usage(agent_type, start_time, end_time)
            
            # Compare against baselines
            baseline_comparison = self._compare_against_baselines(performance_stats)
            
            # Generate insights and recommendations
            insights = self._generate_performance_insights(performance_stats, trend_analysis, baseline_comparison)
            
            return {
                'agent_type': agent_type,
                'time_range_hours': time_range,
                'total_interactions': len(metrics),
                'performance_stats': performance_stats,
                'trend_analysis': trend_analysis,
                'satisfaction_analysis': satisfaction_analysis,
                'feature_usage': feature_usage,
                'baseline_comparison': baseline_comparison,
                'insights': insights,
                'last_updated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error getting agent performance: {str(e)}")
            return {'error': str(e)}
    
    async def get_user_interaction_patterns(self, user_id: str, agent_type: str = None) -> Dict[str, Any]:
        """Analyze user interaction patterns"""
        try:
            # Get user's interaction history
            interactions = await self._get_user_interactions(user_id, agent_type)
            
            if not interactions:
                return {'message': 'No interaction history available'}
            
            # Analyze patterns
            usage_patterns = self._analyze_usage_patterns(interactions)
            preference_analysis = self._analyze_user_preferences(interactions)
            engagement_patterns = self._analyze_engagement_patterns(interactions)
            learning_progression = self._analyze_learning_progression(interactions)
            
            # Generate user profile insights
            user_profile = self._generate_user_profile(interactions, usage_patterns, preference_analysis)
            
            # Predict future needs
            future_needs = await self._predict_user_needs(user_id, interactions)
            
            return {
                'user_id': user_id,
                'total_interactions': len(interactions),
                'agents_used': list(set(i.agent_type for i in interactions)),
                'usage_patterns': usage_patterns,
                'preference_analysis': preference_analysis,
                'engagement_patterns': engagement_patterns,
                'learning_progression': learning_progression,
                'user_profile': user_profile,
                'predicted_needs': future_needs,
                'analysis_date': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error analyzing user patterns: {str(e)}")
            return {'error': str(e)}
    
    async def get_system_health_report(self) -> Dict[str, Any]:
        """Generate comprehensive system health report"""
        try:
            # Get all agent types
            agent_types = await self._get_all_agent_types()
            
            system_health = {}
            overall_health_score = 0
            
            for agent_type in agent_types:
                # Get recent performance
                performance = await self.get_agent_performance(agent_type, time_range=1)  # Last hour
                
                # Calculate health score for this agent
                health_score = self._calculate_agent_health_score(performance)
                
                system_health[agent_type] = {
                    'health_score': health_score,
                    'status': self._get_health_status(health_score),
                    'key_metrics': performance.get('performance_stats', {}),
                    'alerts': self._generate_health_alerts(performance)
                }
                
                overall_health_score += health_score
            
            # Calculate overall system health
            overall_health_score /= len(agent_types) if agent_types else 1
            
            # Get system-wide statistics
            system_stats = await self._get_system_statistics()
            
            # Generate recommendations
            recommendations = self._generate_system_recommendations(system_health, system_stats)
            
            return {
                'overall_health_score': round(overall_health_score, 2),
                'overall_status': self._get_health_status(overall_health_score),
                'agent_health': system_health,
                'system_statistics': system_stats,
                'recommendations': recommendations,
                'report_generated': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating health report: {str(e)}")
            return {'error': str(e)}
    
    async def get_predictive_insights(self, agent_type: str = None, user_id: str = None) -> Dict[str, Any]:
        """Generate predictive insights for optimization"""
        try:
            insights = {}
            
            if agent_type:
                # Predict agent performance trends
                agent_predictions = await self._predict_agent_performance(agent_type)
                insights['agent_predictions'] = agent_predictions
                
                # Predict optimal resource allocation
                resource_optimization = await self._predict_resource_needs(agent_type)
                insights['resource_optimization'] = resource_optimization
            
            if user_id:
                # Predict user behavior and needs
                user_predictions = await self._predict_user_behavior(user_id)
                insights['user_predictions'] = user_predictions
                
                # Predict optimal interaction strategies
                interaction_optimization = await self._predict_optimal_interactions(user_id)
                insights['interaction_optimization'] = interaction_optimization
            
            # System-wide predictions
            system_predictions = await self._predict_system_trends()
            insights['system_predictions'] = system_predictions
            
            return {
                'prediction_scope': {
                    'agent_type': agent_type,
                    'user_id': user_id,
                    'system_wide': True
                },
                'insights': insights,
                'confidence_scores': self._calculate_prediction_confidence(insights),
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating predictive insights: {str(e)}")
            return {'error': str(e)}
    
    def _extract_metrics(self, agent_type: str, user_id: str, interaction_data: Dict[str, Any]) -> AgentMetrics:
        """Extract metrics from interaction data"""
        return AgentMetrics(
            agent_type=agent_type,
            user_id=user_id,
            response_time=interaction_data.get('response_time', 0.0),
            user_satisfaction=interaction_data.get('user_satisfaction', 0.5),
            task_completion_rate=interaction_data.get('task_completion', 0.5),
            engagement_score=interaction_data.get('engagement_score', 0.5),
            specialization_effectiveness=interaction_data.get('specialization_effectiveness', 0.5),
            error_rate=interaction_data.get('error_rate', 0.0),
            timestamp=datetime.now()
        )
    
    def _analyze_interaction(self, interaction_id: str, agent_type: str, user_id: str, 
                           interaction_data: Dict[str, Any]) -> InteractionAnalysis:
        """Analyze interaction quality and characteristics"""
        return InteractionAnalysis(
            interaction_id=interaction_id,
            agent_type=agent_type,
            user_id=user_id,
            interaction_type=interaction_data.get('type', 'standard'),
            success_score=interaction_data.get('success_score', 0.5),
            complexity_level=interaction_data.get('complexity', 1),
            features_used=interaction_data.get('features_used', []),
            response_quality=interaction_data.get('response_quality', 0.5),
            user_feedback=interaction_data.get('user_feedback'),
            contextual_relevance=interaction_data.get('contextual_relevance', 0.5),
            timestamp=datetime.now()
        )
    
    def _calculate_performance_stats(self, metrics: List[AgentMetrics]) -> Dict[str, Any]:
        """Calculate comprehensive performance statistics"""
        if not metrics:
            return {}
        
        # Convert to arrays for statistical analysis
        response_times = [m.response_time for m in metrics]
        satisfaction_scores = [m.user_satisfaction for m in metrics]
        completion_rates = [m.task_completion_rate for m in metrics]
        engagement_scores = [m.engagement_score for m in metrics]
        effectiveness_scores = [m.specialization_effectiveness for m in metrics]
        error_rates = [m.error_rate for m in metrics]
        
        return {
            'response_time': {
                'avg': np.mean(response_times),
                'median': np.median(response_times),
                'p95': np.percentile(response_times, 95),
                'min': np.min(response_times),
                'max': np.max(response_times)
            },
            'user_satisfaction': {
                'avg': np.mean(satisfaction_scores),
                'median': np.median(satisfaction_scores),
                'distribution': self._calculate_distribution(satisfaction_scores)
            },
            'task_completion': {
                'avg': np.mean(completion_rates),
                'success_rate': len([r for r in completion_rates if r >= 0.8]) / len(completion_rates)
            },
            'engagement': {
                'avg': np.mean(engagement_scores),
                'trend': self._calculate_trend(engagement_scores)
            },
            'specialization_effectiveness': {
                'avg': np.mean(effectiveness_scores),
                'consistency': np.std(effectiveness_scores)
            },
            'error_metrics': {
                'avg_error_rate': np.mean(error_rates),
                'error_free_sessions': len([r for r in error_rates if r == 0]) / len(error_rates)
            }
        }
    
    def _analyze_performance_trends(self, metrics: List[AgentMetrics]) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        if len(metrics) < 5:
            return {'trend': 'insufficient_data'}
        
        # Sort by timestamp
        sorted_metrics = sorted(metrics, key=lambda m: m.timestamp)
        
        # Analyze trends for key metrics
        trends = {}
        
        # Response time trend
        response_times = [m.response_time for m in sorted_metrics]
        trends['response_time'] = self._calculate_trend(response_times)
        
        # Satisfaction trend
        satisfaction_scores = [m.user_satisfaction for m in sorted_metrics]
        trends['satisfaction'] = self._calculate_trend(satisfaction_scores)
        
        # Engagement trend
        engagement_scores = [m.engagement_score for m in sorted_metrics]
        trends['engagement'] = self._calculate_trend(engagement_scores)
        
        return {
            'trends': trends,
            'overall_direction': self._determine_overall_trend(trends),
            'volatility': self._calculate_volatility(sorted_metrics),
            'improvement_rate': self._calculate_improvement_rate(sorted_metrics)
        }
    
    def _calculate_trend(self, values: List[float]) -> str:
        """Calculate trend direction for a series of values"""
        if len(values) < 3:
            return 'stable'
        
        # Simple linear trend analysis
        recent_avg = np.mean(values[-3:])
        earlier_avg = np.mean(values[:3]) if len(values) >= 6 else np.mean(values[:-3])
        
        change_ratio = (recent_avg - earlier_avg) / earlier_avg if earlier_avg > 0 else 0
        
        if change_ratio > 0.1:
            return 'improving'
        elif change_ratio < -0.1:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_distribution(self, values: List[float]) -> Dict[str, float]:
        """Calculate distribution statistics"""
        total = len(values)
        if total == 0:
            return {}
        
        return {
            'excellent': len([v for v in values if v >= 0.9]) / total,
            'good': len([v for v in values if 0.7 <= v < 0.9]) / total,
            'average': len([v for v in values if 0.5 <= v < 0.7]) / total,
            'poor': len([v for v in values if v < 0.5]) / total
        }
    
    def _compare_against_baselines(self, performance_stats: Dict[str, Any]) -> Dict[str, Any]:
        """Compare performance against established baselines"""
        comparisons = {}
        
        for metric, baseline in self.performance_baselines.items():
            if metric in performance_stats:
                actual = performance_stats[metric].get('avg', 0)
                variance = ((actual - baseline) / baseline) * 100 if baseline > 0 else 0
                
                comparisons[metric] = {
                    'baseline': baseline,
                    'actual': actual,
                    'variance_percent': round(variance, 2),
                    'status': 'above' if variance > 5 else 'below' if variance < -5 else 'on_target'
                }
        
        return comparisons
    
    def _generate_performance_insights(self, stats: Dict[str, Any], trends: Dict[str, Any], 
                                     baselines: Dict[str, Any]) -> List[str]:
        """Generate actionable insights from performance data"""
        insights = []
        
        # Response time insights
        if 'response_time' in stats and stats['response_time']['avg'] > 3.0:
            insights.append("Response times are above optimal range. Consider performance optimization.")
        
        # Satisfaction insights
        if 'user_satisfaction' in stats and stats['user_satisfaction']['avg'] < 0.7:
            insights.append("User satisfaction is below target. Review response quality and relevance.")
        
        # Trend insights
        if trends.get('overall_direction') == 'declining':
            insights.append("Performance is trending downward. Investigate recent changes and user feedback.")
        elif trends.get('overall_direction') == 'improving':
            insights.append("Performance is improving. Continue current optimization strategies.")
        
        # Baseline comparison insights
        for metric, comparison in baselines.items():
            if comparison['status'] == 'below' and comparison['variance_percent'] < -10:
                insights.append(f"{metric.replace('_', ' ').title()} is significantly below baseline. Requires attention.")
        
        return insights
    
    def _calculate_agent_health_score(self, performance: Dict[str, Any]) -> float:
        """Calculate overall health score for an agent"""
        if 'performance_stats' not in performance:
            return 0.5
        
        stats = performance['performance_stats']
        
        # Weight different metrics
        weights = {
            'user_satisfaction': 0.3,
            'task_completion': 0.25,
            'engagement': 0.2,
            'specialization_effectiveness': 0.15,
            'response_time': 0.1  # Inverse weight
        }
        
        health_score = 0
        total_weight = 0
        
        for metric, weight in weights.items():
            if metric in stats:
                if metric == 'response_time':
                    # Lower response time is better
                    score = max(0, 1 - (stats[metric]['avg'] / 5.0))  # Normalize to 0-1
                else:
                    score = stats[metric].get('avg', 0.5)
                
                health_score += score * weight
                total_weight += weight
        
        return health_score / total_weight if total_weight > 0 else 0.5
    
    def _get_health_status(self, health_score: float) -> str:
        """Get health status based on score"""
        if health_score >= 0.9:
            return 'excellent'
        elif health_score >= 0.8:
            return 'good'
        elif health_score >= 0.6:
            return 'fair'
        elif health_score >= 0.4:
            return 'poor'
        else:
            return 'critical'
    
    async def _store_metrics(self, metrics: AgentMetrics):
        """Store metrics in database"""
        try:
            db = get_db()
            
            query = """
            INSERT INTO agent_metrics (agent_type, user_id, response_time, user_satisfaction,
                                     task_completion_rate, engagement_score, specialization_effectiveness,
                                     error_rate, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            
            params = (
                metrics.agent_type,
                metrics.user_id,
                metrics.response_time,
                metrics.user_satisfaction,
                metrics.task_completion_rate,
                metrics.engagement_score,
                metrics.specialization_effectiveness,
                metrics.error_rate,
                metrics.timestamp.isoformat()
            )
            
            db.execute(query, params)
            db.commit()
            
        except Exception as e:
            logger.error(f"Error storing metrics: {str(e)}")
    
    async def get_real_time_dashboard(self) -> Dict[str, Any]:
        """Get real-time dashboard data"""
        try:
            # Get current system status
            current_time = datetime.now()
            last_hour = current_time - timedelta(hours=1)
            
            # Active sessions count
            active_sessions = await self._get_active_sessions_count()
            
            # Recent performance metrics
            recent_metrics = await self._get_recent_metrics(last_hour)
            
            # System alerts
            alerts = await self._get_system_alerts()
            
            # Agent status
            agent_status = {}
            agent_types = await self._get_all_agent_types()
            
            for agent_type in agent_types:
                agent_metrics = [m for m in recent_metrics if m.agent_type == agent_type]
                agent_status[agent_type] = {
                    'active': len(agent_metrics) > 0,
                    'avg_response_time': np.mean([m.response_time for m in agent_metrics]) if agent_metrics else 0,
                    'avg_satisfaction': np.mean([m.user_satisfaction for m in agent_metrics]) if agent_metrics else 0,
                    'interaction_count': len(agent_metrics)
                }
            
            return {
                'timestamp': current_time.isoformat(),
                'active_sessions': active_sessions,
                'total_interactions_last_hour': len(recent_metrics),
                'agent_status': agent_status,
                'system_alerts': alerts,
                'overall_health': self._calculate_overall_system_health(recent_metrics),
                'performance_summary': self._calculate_performance_summary(recent_metrics)
            }
            
        except Exception as e:
            logger.error(f"Error getting dashboard data: {str(e)}")
            return {'error': str(e)}