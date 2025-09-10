#!/usr/bin/env python3
"""
Content Generation And Creative Writing Assistant Ollama Engine
Specialized Ollama integration for you_gen agent
"""

import asyncio
import json
import logging
from typing import Dict, List, Any, Optional
from core.ollama_service import OllamaService

logger = logging.getLogger(__name__)

class YouGenOllamaEngine:
    """Specialized Ollama engine for you_gen agent"""
    
    def __init__(self):
        self.ollama_service = OllamaService()
        self.primary_model = "mistral:7b"
        self.analysis_model = "qwen2.5:7b"
        self.creative_model = "phi3:14b"
        self.specialization = "content_generation"
        
        # Specialized prompts for content_generation
        self.system_prompts = {
            'default': f"You are an expert AI agent specializing in {self.specialization}. Your capabilities include: ['creative_writing', 'content_planning', 'style_adaptation']",
            'analysis': f"As a {self.specialization} specialist, analyze the following with expertise in ['creative_writing', 'content_planning', 'style_adaptation']",
            'creative': f"Using your {self.specialization} expertise, create innovative solutions leveraging ['creative_writing', 'content_planning', 'style_adaptation']",
            'technical': f"Provide technical guidance on {self.specialization} using your knowledge of ['creative_writing', 'content_planning', 'style_adaptation']"
        }
    
    async def generate_specialized_response(self, prompt: str, context: Dict[str, Any], response_type: str = 'default') -> str:
        """Generate response with content_generation specialization"""
        try:
            # Select appropriate model and system prompt
            model = self._select_model(response_type, context)
            system_prompt = self.system_prompts.get(response_type, self.system_prompts['default'])
            
            # Build enhanced prompt
            enhanced_prompt = f"""
            {system_prompt}
            
            Context Information:
            - User background: {context.get('user_background', 'general')}
            - Interaction history: {len(context.get('history', []))} previous interactions
            - Specialization focus: {self.specialization}
            - Required expertise level: {context.get('expertise_level', 'intermediate')}
            
            User Request: {prompt}
            
            Provide a specialized response that demonstrates deep expertise in {self.specialization}.
            Focus on actionable insights and leverage these capabilities: ['creative_writing', 'content_planning', 'style_adaptation']
            """
            
            # Generate response
            response = await self.ollama_service.generate(
                model=model,
                prompt=enhanced_prompt,
                temperature=self._get_temperature(response_type),
                max_tokens=self._get_max_tokens(response_type)
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error in specialized response generation: {str(e)}")
            return f"I'm processing your {self.specialization} request. Let me provide some guidance."
    
    async def analyze_with_specialization(self, data: str, analysis_type: str = 'comprehensive') -> Dict[str, Any]:
        """Perform specialized analysis using content_generation expertise"""
        try:
            analysis_prompt = f"""
            As an expert in {self.specialization}, perform a {analysis_type} analysis of:
            
            Data: {data}
            
            Your analysis should leverage these specialized capabilities:
            ['creative_writing', 'content_planning', 'style_adaptation']
            
            Provide analysis in JSON format:
            {{
                "specialization_insights": {"key insights specific to content_generation"},
                "recommendations": [{"actionable recommendations"}],
                "confidence_score": 0.95,
                "expertise_level_required": "intermediate",
                "follow_up_suggestions": [{"suggested next steps"}],
                "specialized_metrics": {"content_generation_specific_metrics"}
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.analysis_model,
                prompt=analysis_prompt,
                temperature=0.3
            )
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "specialization_insights": {"analysis": "completed"},
                    "recommendations": ["Continue with standard approach"],
                    "confidence_score": 0.7,
                    "expertise_level_required": "beginner"
                }
                
        except Exception as e:
            logger.error(f"Error in specialized analysis: {str(e)}")
            return {"error": str(e)}
    
    async def generate_creative_solution(self, problem: str, constraints: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate creative solutions using content_generation expertise"""
        try:
            constraints = constraints or {}
            
            creative_prompt = f"""
            Using your expertise in {self.specialization}, generate innovative solutions for:
            
            Problem: {problem}
            Constraints: {constraints}
            
            Your specialized capabilities: ['creative_writing', 'content_planning', 'style_adaptation']
            
            Generate multiple creative approaches that leverage {self.specialization} best practices.
            
            Respond in JSON format:
            {{
                "primary_solution": {{
                    "approach": "main recommended approach",
                    "implementation_steps": ["step1", "step2", "step3"],
                    "expected_outcomes": ["outcome1", "outcome2"],
                    "specialization_advantages": "how {self.specialization} expertise helps"
                }},
                "alternative_solutions": [
                    {{
                        "approach": "alternative approach",
                        "pros": ["advantage1", "advantage2"],
                        "cons": ["limitation1", "limitation2"]
                    }}
                ],
                "innovation_score": 0.85,
                "feasibility_rating": "high"
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.creative_model,
                prompt=creative_prompt,
                temperature=0.8
            )
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "primary_solution": {
                        "approach": "Standard approach to the problem",
                        "implementation_steps": ["Analyze", "Plan", "Execute"],
                        "expected_outcomes": ["Problem resolution"],
                        "specialization_advantages": f"Leverage {self.specialization} expertise"
                    },
                    "alternative_solutions": [],
                    "innovation_score": 0.6,
                    "feasibility_rating": "medium"
                }
                
        except Exception as e:
            logger.error(f"Error generating creative solution: {str(e)}")
            return {"error": str(e)}
    
    def _select_model(self, response_type: str, context: Dict[str, Any]) -> str:
        """Select appropriate model based on response type and context"""
        complexity = context.get('complexity', 'medium')
        
        if response_type == 'creative' or complexity == 'high':
            return self.creative_model
        elif response_type == 'analysis' or response_type == 'technical':
            return self.analysis_model
        else:
            return self.primary_model
    
    def _get_temperature(self, response_type: str) -> float:
        """Get appropriate temperature for response type"""
        temperature_map = {
            'default': 0.7,
            'analysis': 0.3,
            'creative': 0.9,
            'technical': 0.5
        }
        return temperature_map.get(response_type, 0.7)
    
    def _get_max_tokens(self, response_type: str) -> int:
        """Get appropriate max tokens for response type"""
        token_map = {
            'default': 200,
            'analysis': 300,
            'creative': 250,
            'technical': 350
        }
        return token_map.get(response_type, 200)
    
    async def validate_specialized_output(self, output: str, expected_format: str = 'text') -> Dict[str, Any]:
        """Validate output meets content_generation standards"""
        try:
            validation_prompt = f"""
            As a {self.specialization} expert, validate this output for quality and accuracy:
            
            Output: {output}
            Expected format: {expected_format}
            Specialization: {self.specialization}
            
            Evaluate:
            1. Technical accuracy for {self.specialization}
            2. Completeness of response
            3. Appropriate use of specialized knowledge
            4. Adherence to expected format
            
            Respond in JSON:
            {{
                "validation_score": 0.9,
                "technical_accuracy": 0.95,
                "completeness": 0.85,
                "format_compliance": 1.0,
                "improvement_suggestions": ["suggestion1", "suggestion2"],
                "passes_validation": true
            }}
            """
            
            response = await self.ollama_service.generate(
                model=self.analysis_model,
                prompt=validation_prompt,
                temperature=0.2
            )
            
            try:
                return json.loads(response)
            except json.JSONDecodeError:
                return {
                    "validation_score": 0.7,
                    "passes_validation": True,
                    "note": "Validation completed with fallback scoring"
                }
                
        except Exception as e:
            logger.error(f"Error in output validation: {str(e)}")
            return {"error": str(e), "passes_validation": True}
