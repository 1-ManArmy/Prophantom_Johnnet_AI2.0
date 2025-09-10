#!/usr/bin/env python3
"""
Pdf Analysis And Document Intelligence Agent WebSocket Handler
Real-time communication for pdf_mind agent
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from flask_socketio import emit, join_room, leave_room
from ..logic import PdfMindLogic
from ..engine.ollama_deepseek-coder_6_7b import PdfMindOllamaEngine

logger = logging.getLogger(__name__)

class PdfMindSocketHandler:
    """WebSocket handler for pdf_mind real-time communication"""
    
    def __init__(self):
        self.logic = PdfMindLogic()
        self.engine = PdfMindOllamaEngine()
        self.active_sessions = {}
        self.specialization = "document_analysis"
        self.features = ['pdf_parsing', 'content_extraction', 'document_summarization']
    
    async def handle_connect(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """Handle user connection to pdf_mind agent"""
        try:
            # Join user to their specialized room
            join_room(f"pdf_mind_{user_id}")
            
            # Initialize session with specialization context
            self.active_sessions[session_id] = {
                'user_id': user_id,
                'agent_type': 'pdf_mind',
                'specialization': self.specialization,
                'connected_at': datetime.now(),
                'status': 'active',
                'interaction_count': 0,
                'features_available': self.features
            }
            
            # Get user insights for personalized welcome
            user_insights = await self.logic.get_user_insights(user_id)
            
            # Send specialized welcome message
            welcome_message = f"Hello! I'm your {self.specialization} specialist. I can help you with {', '.join(self.features)}. How can I assist you today?"
            
            emit('connection_established', {
                'status': 'connected',
                'agent_type': 'pdf_mind',
                'specialization': self.specialization,
                'session_id': session_id,
                'welcome_message': welcome_message,
                'available_features': self.features,
                'user_insights': user_insights
            })
            
            logger.info(f"pdf_mind connection established for user {user_id}")
            return {'success': True, 'session_id': session_id, 'specialization': self.specialization}
            
        except Exception as e:
            logger.error(f"Error handling pdf_mind connection: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    async def handle_specialized_request(self, data: Dict[str, Any]) -> None:
        """Handle specialized requests for document_analysis"""
        try:
            user_id = data.get('user_id')
            request = data.get('request', '')
            request_type = data.get('type', 'default')  # default, analysis, creative, technical
            session_id = data.get('session_id')
            
            if not user_id or not request:
                emit('error', {'message': 'Missing required fields for pdf_mind request'})
                return
            
            # Update session
            if session_id in self.active_sessions:
                self.active_sessions[session_id]['interaction_count'] += 1
            
            # Show specialized typing indicator
            emit('typing_indicator', {
                'status': 'processing', 
                'agent': 'pdf_mind',
                'specialization': self.specialization,
                'processing_type': request_type
            }, room=f"pdf_mind_{user_id}")
            
            # Process with specialized logic
            response_data = await self.logic.process_request(user_id, request, {
                'request_type': request_type,
                'specialization_focus': self.specialization
            })
            
            # Generate additional specialized insights if successful
            if response_data['success']:
                # Get specialized analysis
                analysis_result = await self.engine.analyze_with_specialization(
                    request, 
                    analysis_type='comprehensive'
                )
                
                # Stop typing indicator
                emit('typing_indicator', {'status': 'completed'}, room=f"pdf_mind_{user_id}")
                
                # Send specialized response
                emit('specialized_response', {
                    'type': 'pdf_mind_response',
                    'specialization': self.specialization,
                    'response': response_data['response'],
                    'analysis': response_data['analysis'],
                    'specialized_insights': analysis_result,
                    'features_used': response_data.get('features_used', []),
                    'confidence_score': analysis_result.get('confidence_score', 0.8),
                    'timestamp': datetime.now().isoformat(),
                    'agent': 'pdf_mind'
                }, room=f"pdf_mind_{user_id}")
                
                # Send specialized metrics
                emit('agent_metrics', {
                    'agent_type': 'pdf_mind',
                    'specialization_effectiveness': response_data['context_updates'],
                    'features_utilized': self.features,
                    'interaction_quality': analysis_result.get('confidence_score', 0.8)
                }, room=f"pdf_mind_{user_id}")
                
            else:
                emit('error', {
                    'message': f'Error in {self.specialization} processing',
                    'details': response_data.get('error', 'Unknown error'),
                    'agent': 'pdf_mind'
                }, room=f"pdf_mind_{user_id}")
            
        except Exception as e:
            logger.error(f"Error handling pdf_mind request: {str(e)}")
            emit('error', {'message': f'An unexpected error occurred in {self.specialization} processing'})
    
    async def handle_creative_request(self, data: Dict[str, Any]) -> None:
        """Handle creative/innovative requests"""
        try:
            user_id = data.get('user_id')
            problem = data.get('problem', '')
            constraints = data.get('constraints', {})
            
            if not user_id or not problem:
                emit('error', {'message': 'Missing problem description'})
                return
            
            # Show creative processing indicator
            emit('creative_processing', {
                'status': 'generating_solutions',
                'specialization': self.specialization
            }, room=f"pdf_mind_{user_id}")
            
            # Generate creative solutions
            creative_result = await self.engine.generate_creative_solution(problem, constraints)
            
            emit('creative_solution', {
                'type': 'creative_response',
                'agent': 'pdf_mind',
                'specialization': self.specialization,
                'problem': problem,
                'solutions': creative_result,
                'innovation_score': creative_result.get('innovation_score', 0.7),
                'timestamp': datetime.now().isoformat()
            }, room=f"pdf_mind_{user_id}")
            
        except Exception as e:
            logger.error(f"Error handling creative request: {str(e)}")
            emit('error', {'message': 'Error generating creative solutions'})
    
    async def handle_analysis_request(self, data: Dict[str, Any]) -> None:
        """Handle analysis requests with specialization"""
        try:
            user_id = data.get('user_id')
            analysis_data = data.get('data', '')
            analysis_type = data.get('analysis_type', 'comprehensive')
            
            if not user_id or not analysis_data:
                emit('error', {'message': 'Missing data for analysis'})
                return
            
            # Show analysis indicator
            emit('analysis_processing', {
                'status': 'analyzing',
                'specialization': self.specialization,
                'analysis_type': analysis_type
            }, room=f"pdf_mind_{user_id}")
            
            # Perform specialized analysis
            analysis_result = await self.engine.analyze_with_specialization(
                analysis_data, 
                analysis_type
            )
            
            # Validate the analysis output
            validation_result = await self.engine.validate_specialized_output(
                json.dumps(analysis_result), 
                'json'
            )
            
            emit('analysis_complete', {
                'type': 'analysis_response',
                'agent': 'pdf_mind',
                'specialization': self.specialization,
                'analysis_result': analysis_result,
                'validation': validation_result,
                'confidence_score': analysis_result.get('confidence_score', 0.8),
                'timestamp': datetime.now().isoformat()
            }, room=f"pdf_mind_{user_id}")
            
        except Exception as e:
            logger.error(f"Error handling analysis request: {str(e)}")
            emit('error', {'message': 'Error performing specialized analysis'})
    
    async def handle_feature_request(self, data: Dict[str, Any]) -> None:
        """Handle requests for specific agent features"""
        try:
            user_id = data.get('user_id')
            feature_name = data.get('feature')
            feature_data = data.get('feature_data', {})
            
            if not user_id or not feature_name:
                emit('error', {'message': 'Missing feature specification'})
                return
            
            if feature_name not in self.features:
                emit('error', {'message': f'Feature {feature_name} not available in {self.specialization}'})
                return
            
            # Process feature-specific request
            # This would be expanded based on specific feature implementations
            emit('feature_response', {
                'feature': feature_name,
                'agent': 'pdf_mind',
                'specialization': self.specialization,
                'result': f'Processing {feature_name} with {self.specialization} expertise',
                'available_features': self.features,
                'timestamp': datetime.now().isoformat()
            }, room=f"pdf_mind_{user_id}")
            
        except Exception as e:
            logger.error(f"Error handling feature request: {str(e)}")
            emit('error', {'message': 'Error processing feature request'})
    
    async def handle_disconnect(self, user_id: str, session_id: str) -> None:
        """Handle user disconnection from pdf_mind"""
        try:
            # Leave specialized room
            leave_room(f"pdf_mind_{user_id}")
            
            # Process session data
            if session_id in self.active_sessions:
                session_data = self.active_sessions[session_id]
                session_data['status'] = 'disconnected'
                session_data['disconnected_at'] = datetime.now()
                
                # Calculate specialized session metrics
                session_duration = session_data['disconnected_at'] - session_data['connected_at']
                specialized_metrics = {
                    'agent_type': 'pdf_mind',
                    'specialization': self.specialization,
                    'duration_minutes': session_duration.total_seconds() / 60,
                    'interaction_count': session_data['interaction_count'],
                    'features_available': len(self.features),
                    'specialization_effectiveness': 'calculated_from_interactions'
                }
                
                # Store specialized analytics
                await self._store_specialized_analytics(user_id, specialized_metrics)
                
                # Cleanup
                del self.active_sessions[session_id]
            
            logger.info(f"pdf_mind session ended for user {user_id}")
            
        except Exception as e:
            logger.error(f"Error handling pdf_mind disconnect: {str(e)}")
    
    async def _store_specialized_analytics(self, user_id: str, metrics: Dict[str, Any]):
        """Store analytics specific to document_analysis"""
        try:
            logger.info(f"pdf_mind analytics: {metrics}")
            # Implementation would store in specialized analytics database
            
        except Exception as e:
            logger.error(f"Error storing pdf_mind analytics: {str(e)}")
    
    def get_specialization_status(self) -> Dict[str, Any]:
        """Get status of pdf_mind specialization"""
        return {
            'agent_type': 'pdf_mind',
            'specialization': self.specialization,
            'features': self.features,
            'active_sessions': len(self.active_sessions),
            'total_interactions': sum(
                session['interaction_count'] 
                for session in self.active_sessions.values()
            ),
            'description': "PDF analysis and document intelligence agent"
        }

# Global socket handler instance
pdf_mind_socket_handler = PdfMindSocketHandler()
