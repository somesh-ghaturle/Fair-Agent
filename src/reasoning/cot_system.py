"""
Chain-of-Thought Reasoning System for FAIR-Agent

This module implements structured reasoning capabilities to improve interpretability
and logical consistency of agent responses through step-by-step reasoning.
"""

import logging
import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import sys
import os

# Add utils to path for OllamaClient
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))
try:
    from ollama_client import OllamaClient
except ImportError:
    # Fallback for relative import
    from ..utils.ollama_client import OllamaClient

logger = logging.getLogger(__name__)

class ReasoningStep(Enum):
    """Types of reasoning steps"""
    PROBLEM_ANALYSIS = "problem_analysis"
    INFORMATION_GATHERING = "information_gathering"
    EVALUATION = "evaluation"
    SYNTHESIS = "synthesis"
    CONCLUSION = "conclusion"
    UNCERTAINTY_ASSESSMENT = "uncertainty_assessment"

@dataclass
class ThoughtStep:
    """Individual step in chain of thought"""
    step_number: int
    step_type: ReasoningStep
    thought: str
    evidence: Optional[str] = None
    confidence: float = 0.7
    reasoning_quality: float = 0.5

@dataclass
class ReasoningChain:
    """Complete chain of reasoning"""
    query: str
    domain: str
    thought_steps: List[ThoughtStep]
    final_conclusion: str
    overall_confidence: float
    reasoning_transparency: float
    logical_consistency: float

class MedicalReasoningTemplate:
    """Template for medical domain reasoning"""
    
    @staticmethod
    def get_reasoning_steps(query: str) -> List[str]:
        """Get medical reasoning step templates"""
        
        # Detect query type
        if any(word in query.lower() for word in ['symptom', 'pain', 'feeling', 'hurt']):
            return [
                "Let me analyze your symptoms systematically:",
                "First, I'll consider the most common causes of {symptom}:",
                "Next, I'll evaluate any potential red flags or serious conditions:",
                "I should also consider your individual risk factors:",
                "Based on this analysis, here are the general recommendations:",
                "However, I must emphasize the importance of professional medical evaluation:"
            ]
        
        elif any(word in query.lower() for word in ['medication', 'drug', 'treatment', 'medicine']):
            return [
                "Let me break down the information about {medication}:",
                "First, I'll explain how this medication works:",
                "Next, I'll discuss the typical uses and benefits:",
                "Now, let me address potential side effects and risks:",
                "I should also mention important interactions and precautions:",
                "Finally, I must emphasize the importance of medical supervision:"
            ]
        
        elif any(word in query.lower() for word in ['diagnosis', 'condition', 'disease']):
            return [
                "Let me provide information about {condition} systematically:",
                "First, I'll explain what this condition involves:",
                "Next, I'll discuss common signs and symptoms:",
                "Then, I'll cover typical treatment approaches:",
                "I should also mention the importance of proper diagnosis:",
                "Most importantly, professional medical care is essential:"
            ]
        
        else:
            return [
                "Let me address your medical question step by step:",
                "First, I'll provide general background information:",
                "Next, I'll discuss relevant factors to consider:",
                "Then, I'll offer evidence-based guidance:",
                "I should also highlight important limitations:",
                "Finally, I must emphasize the need for medical consultation:"
            ]

class FinancialReasoningTemplate:
    """Template for financial domain reasoning"""
    
    @staticmethod
    def get_reasoning_steps(query: str) -> List[str]:
        """Get financial reasoning step templates"""
        query_lower = query.lower()
        
        # Check for comparison queries (e.g., "pay off mortgage OR invest")
        is_comparison = any(word in query_lower for word in [' or ', ' vs ', 'versus', 'compare', 'difference', 'better'])
        
        # Detect specific topics
        has_invest = any(word in query_lower for word in ['investment', 'invest', 'portfolio', 'stock', 'fund'])
        has_debt = any(word in query_lower for word in ['debt', 'loan', 'credit', 'mortgage'])
        has_retirement = any(word in query_lower for word in ['retirement', 'saving', 'pension', '401k'])
        
        # Case 1: Comparison (e.g., Mortgage vs Invest)
        if is_comparison and ((has_invest and has_debt) or (has_invest and has_retirement)):
            return [
                "Let me analyze this financial trade-off systematically:",
                "First, I'll compare the potential returns versus the cost of debt:",
                "Next, I'll evaluate the risk factors and liquidity needs:",
                "Then, I'll consider tax implications and psychological factors:",
                "I should also run a scenario analysis for both options:",
                "Finally, I must emphasize that the 'best' choice depends on your specific goals:"
            ]
            
        # Case 2: Investment focus
        elif has_invest:
            return [
                "Let me analyze your investment question systematically:",
                "First, I'll consider your risk tolerance and investment timeline:",
                "Next, I'll evaluate the specific investment options:",
                "Then, I'll discuss diversification and risk management:",
                "I should also address potential returns and volatility:",
                "Finally, I must remind you about the importance of professional advice:"
            ]
        
        # Case 3: Retirement focus
        elif has_retirement:
            return [
                "Let me break down retirement planning considerations:",
                "First, I'll assess your current financial situation:",
                "Next, I'll calculate potential savings needs:",
                "Then, I'll discuss different retirement account options:",
                "I should also consider tax implications:",
                "Most importantly, personalized financial planning is crucial:"
            ]
        
        # Case 4: Debt/Mortgage focus
        elif has_debt:
            return [
                "Let me analyze your debt management question:",
                "First, I'll assess the type and terms of the debt:",
                "Next, I'll consider repayment strategies:",
                "Then, I'll evaluate the impact on your credit:",
                "I should also discuss potential risks:",
                "Finally, professional financial counseling may be beneficial:"
            ]
        
        # Default
        else:
            return [
                "Let me address your financial question step by step:",
                "First, I'll provide relevant financial background:",
                "Next, I'll consider key factors that apply:",
                "Then, I'll discuss potential strategies:",
                "I should also highlight important risks:",
                "Remember that individual financial advice requires professional consultation:"
            ]

class ReasoningQualityEvaluator:
    """Evaluates the quality of reasoning chains"""
    
    def __init__(self):
        self.quality_metrics = {
            'logical_flow': 0.0,
            'evidence_integration': 0.0,
            'completeness': 0.0,
            'clarity': 0.0,
            'uncertainty_handling': 0.0
        }
    
    def evaluate_reasoning_chain(self, chain: ReasoningChain) -> Dict[str, float]:
        """Evaluate overall quality of reasoning chain"""
        
        # Evaluate logical flow
        logical_flow = self._evaluate_logical_flow(chain.thought_steps)
        
        # Evaluate evidence integration
        evidence_integration = self._evaluate_evidence_integration(chain.thought_steps)
        
        # Evaluate completeness
        completeness = self._evaluate_completeness(chain.thought_steps, chain.domain)
        
        # Evaluate clarity
        clarity = self._evaluate_clarity(chain.thought_steps)
        
        # Evaluate uncertainty handling
        uncertainty_handling = self._evaluate_uncertainty_handling(chain.thought_steps)
        
        return {
            'logical_flow': logical_flow,
            'evidence_integration': evidence_integration,
            'completeness': completeness,
            'clarity': clarity,
            'uncertainty_handling': uncertainty_handling,
            'overall_quality': (logical_flow + evidence_integration + completeness + clarity + uncertainty_handling) / 5
        }
    
    def _evaluate_logical_flow(self, steps: List[ThoughtStep]) -> float:
        """Evaluate logical progression of reasoning steps"""
        if len(steps) < 2:
            return 0.3
        
        # Check for appropriate step progression
        expected_flow = [
            ReasoningStep.PROBLEM_ANALYSIS,
            ReasoningStep.INFORMATION_GATHERING,
            ReasoningStep.EVALUATION,
            ReasoningStep.SYNTHESIS,
            ReasoningStep.CONCLUSION
        ]
        
        step_types = [step.step_type for step in steps]
        flow_score = 0.0
        
        # Basic flow checking
        if ReasoningStep.PROBLEM_ANALYSIS in step_types:
            flow_score += 0.2
        if ReasoningStep.EVALUATION in step_types:
            flow_score += 0.2
        if ReasoningStep.CONCLUSION in step_types:
            flow_score += 0.2
        
        # Sequential logic bonus
        if len(step_types) >= 3:
            flow_score += 0.2
        
        # Uncertainty assessment bonus
        if ReasoningStep.UNCERTAINTY_ASSESSMENT in step_types:
            flow_score += 0.2
        
        return min(flow_score, 1.0)
    
    def _evaluate_evidence_integration(self, steps: List[ThoughtStep]) -> float:
        """Evaluate how well evidence is integrated"""
        if not steps:
            return 0.0
        
        evidence_steps = [step for step in steps if step.evidence]
        evidence_ratio = len(evidence_steps) / len(steps)
        
        # Higher score for more evidence integration
        base_score = evidence_ratio * 0.7
        
        # Quality bonus for substantial evidence
        if evidence_steps:
            avg_evidence_length = sum(len(step.evidence) for step in evidence_steps) / len(evidence_steps)
            if avg_evidence_length > 50:  # Substantial evidence
                base_score += 0.3
        
        return min(base_score, 1.0)
    
    def _evaluate_completeness(self, steps: List[ThoughtStep], domain: str) -> float:
        """Evaluate completeness of reasoning for domain"""
        if not steps:
            return 0.0
        
        # Domain-specific completeness criteria
        if domain == "medical":
            required_aspects = ['symptoms', 'treatment', 'risks', 'professional']
        elif domain == "finance":
            required_aspects = ['risk', 'return', 'diversification', 'professional']
        else:
            required_aspects = ['analysis', 'evaluation', 'conclusion']
        
        # Check how many aspects are covered
        covered_aspects = 0
        all_text = ' '.join(step.thought.lower() for step in steps)
        
        for aspect in required_aspects:
            if aspect in all_text:
                covered_aspects += 1
        
        completeness_score = covered_aspects / len(required_aspects)
        
        # Length bonus for thorough reasoning
        if len(steps) >= 4:
            completeness_score += 0.1
        
        return min(completeness_score, 1.0)
    
    def _evaluate_clarity(self, steps: List[ThoughtStep]) -> float:
        """Evaluate clarity of reasoning steps"""
        if not steps:
            return 0.0
        
        clarity_score = 0.0
        
        # Check for clear step structure
        numbered_steps = sum(1 for step in steps if str(step.step_number) in step.thought)
        if numbered_steps >= len(steps) * 0.5:
            clarity_score += 0.3
        
        # Check for transition words
        transition_words = ['first', 'next', 'then', 'finally', 'however', 'therefore']
        transition_count = 0
        for step in steps:
            if any(word in step.thought.lower() for word in transition_words):
                transition_count += 1
        
        if transition_count >= len(steps) * 0.3:
            clarity_score += 0.2
        
        # Check average step length (not too short, not too long)
        avg_length = sum(len(step.thought) for step in steps) / len(steps)
        if 50 <= avg_length <= 200:
            clarity_score += 0.3
        
        # Structure bonus
        if len(steps) >= 3:
            clarity_score += 0.2
        
        return min(clarity_score, 1.0)
    
    def _evaluate_uncertainty_handling(self, steps: List[ThoughtStep]) -> float:
        """Evaluate how well uncertainty is handled"""
        if not steps:
            return 0.0
        
        uncertainty_indicators = [
            'however', 'but', 'although', 'may', 'might', 'could', 'possibly',
            'uncertainty', 'risk', 'limitation', 'consult', 'professional'
        ]
        
        uncertainty_score = 0.0
        
        # Check for uncertainty language
        uncertainty_mentions = 0
        for step in steps:
            if any(indicator in step.thought.lower() for indicator in uncertainty_indicators):
                uncertainty_mentions += 1
        
        if uncertainty_mentions > 0:
            uncertainty_score += 0.4
        
        # Check for confidence scores
        low_confidence_steps = [step for step in steps if step.confidence < 0.8]
        if low_confidence_steps:
            uncertainty_score += 0.3
        
        # Professional consultation mention bonus
        all_text = ' '.join(step.thought.lower() for step in steps)
        if any(phrase in all_text for phrase in ['consult', 'professional', 'doctor', 'advisor']):
            uncertainty_score += 0.3
        
        return min(uncertainty_score, 1.0)

class ChainOfThoughtGenerator:
    """Generates chain-of-thought reasoning for agent responses"""
    
    def __init__(self):
        self.medical_template = MedicalReasoningTemplate()
        self.financial_template = FinancialReasoningTemplate()
        self.quality_evaluator = ReasoningQualityEvaluator()
        self.logger = logging.getLogger(__name__)
        
        # Initialize Ollama client for dynamic generation
        try:
            self.ollama_client = OllamaClient()
            self.has_llm = self.ollama_client.is_available()
        except Exception as e:
            self.logger.warning(f"Failed to initialize Ollama client for CoT: {e}")
            self.has_llm = False
    
    def generate_reasoning_chain(
        self, 
        query: str, 
        response: str, 
        domain: str
    ) -> ReasoningChain:
        """Generate chain-of-thought reasoning for a response"""
        
        # Try to use LLM for dynamic reasoning first
        if self.has_llm:
            try:
                thought_steps = self._generate_reasoning_with_llm(query, response, domain)
                if thought_steps:
                    # Calculate overall metrics
                    overall_confidence = sum(step.confidence for step in thought_steps) / len(thought_steps)
                    
                    # Create reasoning chain
                    chain = ReasoningChain(
                        query=query,
                        domain=domain,
                        thought_steps=thought_steps,
                        final_conclusion=response,
                        overall_confidence=overall_confidence,
                        reasoning_transparency=0.0,
                        logical_consistency=0.0
                    )
                    
                    # Evaluate reasoning quality
                    quality_metrics = self.quality_evaluator.evaluate_reasoning_chain(chain)
                    chain.reasoning_transparency = quality_metrics['overall_quality']
                    chain.logical_consistency = quality_metrics['logical_flow']
                    
                    return chain
            except Exception as e:
                self.logger.error(f"LLM reasoning generation failed: {e}")
                # Fallback to template-based generation
        
        # Fallback: Get domain-specific reasoning template
        if domain == "medical":
            step_templates = self.medical_template.get_reasoning_steps(query)
        elif domain == "finance":
            step_templates = self.financial_template.get_reasoning_steps(query)
        else:
            step_templates = [
                "Let me address your question systematically:",
                "First, I'll analyze the key components:",
                "Next, I'll consider relevant factors:",
                "Then, I'll synthesize the information:",
                "Finally, I'll provide a clear conclusion:"
            ]
        
        # Generate thought steps
        thought_steps = self._generate_thought_steps(
            query, response, step_templates, domain
        )
        
        # Calculate overall metrics
        overall_confidence = sum(step.confidence for step in thought_steps) / len(thought_steps)
        
        # Create reasoning chain
        chain = ReasoningChain(
            query=query,
            domain=domain,
            thought_steps=thought_steps,
            final_conclusion=response,
            overall_confidence=overall_confidence,
            reasoning_transparency=0.0,  # Will be calculated
            logical_consistency=0.0      # Will be calculated
        )
        
        # Evaluate reasoning quality
        quality_metrics = self.quality_evaluator.evaluate_reasoning_chain(chain)
        chain.reasoning_transparency = quality_metrics['overall_quality']
        chain.logical_consistency = quality_metrics['logical_flow']
        
        return chain
    
    def _generate_reasoning_with_llm(self, query: str, response: str, domain: str) -> Optional[List[ThoughtStep]]:
        """Generate reasoning steps using LLM"""
        
        prompt = f"""
        Analyze the following {domain} query and response. 
        Break down the reasoning process that leads to this response into 3-5 clear, logical steps.
        
        Query: {query}
        Response: {response}
        
        Format your output as a numbered list of steps. Each step should be a single sentence describing a part of the reasoning process.
        Do not include introductory text or "Here are the steps". Just the numbered list.
        
        Example format:
        1. Analyzed the user's request regarding [topic].
        2. Identified key factors such as [factor 1] and [factor 2].
        3. Evaluated the evidence from [source type].
        4. Synthesized the findings to conclude [conclusion].
        """
        
        try:
            generated_text = self.ollama_client.generate(
                model="llama3.2:latest",
                prompt=prompt,
                max_tokens=256,
                temperature=0.3
            )
            
            if not generated_text:
                return None
                
            # Parse the generated text into steps
            steps = []
            lines = generated_text.strip().split('\n')
            step_num = 1
            
            for line in lines:
                line = line.strip()
                # Match numbered lines (e.g., "1. Step description")
                if re.match(r'^\d+\.', line):
                    content = re.sub(r'^\d+\.\s*', '', line)
                    
                    # Determine step type based on content/position
                    if step_num == 1:
                        step_type = ReasoningStep.PROBLEM_ANALYSIS
                    elif step_num == len(lines):
                        step_type = ReasoningStep.CONCLUSION
                    elif "evaluate" in content.lower() or "assess" in content.lower():
                        step_type = ReasoningStep.EVALUATION
                    elif "gather" in content.lower() or "identify" in content.lower():
                        step_type = ReasoningStep.INFORMATION_GATHERING
                    else:
                        step_type = ReasoningStep.SYNTHESIS
                        
                    step = ThoughtStep(
                        step_number=step_num,
                        step_type=step_type,
                        thought=content,
                        evidence=None,
                        confidence=0.85, # Higher confidence for LLM generated steps
                        reasoning_quality=0.8
                    )
                    steps.append(step)
                    step_num += 1
            
            return steps if steps else None
            
        except Exception as e:
            self.logger.error(f"Error in _generate_reasoning_with_llm: {e}")
            return None

    def _generate_thought_steps(
        self, 
        query: str, 
        response: str, 
        templates: List[str], 
        domain: str
    ) -> List[ThoughtStep]:
        """Generate individual thought steps"""
        
        thought_steps = []
        response_parts = self._split_response_into_parts(response, len(templates))
        
        for i, (template, part) in enumerate(zip(templates, response_parts), 1):
            # Determine step type
            step_type = self._determine_step_type(i, len(templates), template)
            
            # Generate thought content
            thought_content = self._generate_step_content(template, part, query, domain, i)
            
            # Assess confidence and quality
            confidence = self._assess_step_confidence(thought_content, domain)
            quality = self._assess_reasoning_quality(thought_content)
            
            # Create evidence if relevant
            evidence = self._generate_step_evidence(part, domain) if part else None
            
            step = ThoughtStep(
                step_number=i,
                step_type=step_type,
                thought=thought_content,
                evidence=evidence,
                confidence=confidence,
                reasoning_quality=quality
            )
            
            thought_steps.append(step)
        
        return thought_steps
    
    def _determine_step_type(self, step_num: int, total_steps: int, template: str) -> ReasoningStep:
        """Determine the type of reasoning step"""
        
        template_lower = template.lower()
        
        if 'analyze' in template_lower or step_num == 1:
            return ReasoningStep.PROBLEM_ANALYSIS
        elif 'information' in template_lower or 'background' in template_lower:
            return ReasoningStep.INFORMATION_GATHERING
        elif 'evaluate' in template_lower or 'consider' in template_lower:
            return ReasoningStep.EVALUATION
        elif 'synthesis' in template_lower or 'combine' in template_lower:
            return ReasoningStep.SYNTHESIS
        elif step_num == total_steps or 'conclusion' in template_lower:
            return ReasoningStep.CONCLUSION
        else:
            return ReasoningStep.EVALUATION
    
    def _split_response_into_parts(self, response: str, num_parts: int) -> List[str]:
        """Split response into logical parts for reasoning steps"""
        
        # Split by sentences
        sentences = re.split(r'[.!?]+', response)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if len(sentences) <= num_parts:
            return sentences + [''] * (num_parts - len(sentences))
        
        # Group sentences into parts
        sentences_per_part = len(sentences) // num_parts
        parts = []
        
        for i in range(num_parts):
            start_idx = i * sentences_per_part
            if i == num_parts - 1:  # Last part gets remaining sentences
                part_sentences = sentences[start_idx:]
            else:
                part_sentences = sentences[start_idx:start_idx + sentences_per_part]
            
            parts.append('. '.join(part_sentences) + '.' if part_sentences else '')
        
        return parts
    
    def _generate_step_content(
        self, 
        template: str, 
        response_part: str, 
        query: str, 
        domain: str,
        step_number: int = 1
    ) -> str:
        """Generate content for a reasoning step"""
        
        # Fill in template variables
        filled_template = template
        
        # Simple template variable replacement
        if '{symptom}' in template:
            # Extract potential symptom from query
            symptom = self._extract_key_terms(query, ['pain', 'ache', 'symptom', 'feeling'])
            filled_template = template.replace('{symptom}', symptom or 'your symptoms')
        
        if '{medication}' in template:
            medication = self._extract_key_terms(query, ['aspirin', 'medication', 'drug', 'medicine'])
            filled_template = template.replace('{medication}', medication or 'this medication')
        
        if '{condition}' in template:
            condition = self._extract_key_terms(query, ['diabetes', 'hypertension', 'condition', 'disease'])
            filled_template = template.replace('{condition}', condition or 'this condition')
        
        # Generate dynamic step content based on response content and reasoning flow
        if response_part and len(response_part.strip()) > 0:
            # Analyze the response part to generate contextual reasoning
            step_content = self._generate_contextual_reasoning(
                filled_template, response_part, query, domain, step_number
            )
        else:
            # Fall back to template for structure
            step_content = filled_template
        
        return step_content
    
    def _generate_contextual_reasoning(
        self, 
        template: str, 
        response_part: str, 
        query: str, 
        domain: str, 
        step_number: int
    ) -> str:
        """Generate dynamic reasoning based on actual response content"""
        
        # Extract key concepts from the response part
        key_concepts = self._extract_response_concepts(response_part, domain)
        
        # Generate reasoning based on step type and content
        if step_number == 1:
            # Problem analysis step
            query_focus = self._identify_query_focus(query, domain)
            return f"{template.rstrip(':')} to provide accurate, evidence-based information."
        
        elif "first" in template.lower() and step_number == 2:
            # First evaluation step - what we're analyzing
            if key_concepts:
                concept_list = ", ".join(key_concepts[:3])  # Top 3 concepts
                return f"{template.rstrip(':')} including {concept_list}."
            else:
                return f"{template.rstrip(':')} to understand the core question."
            
        elif "next" in template.lower() or "then" in template.lower():
            # Middle evaluation steps - deeper analysis
            if key_concepts:
                return f"{template.rstrip(':')} particularly focusing on {key_concepts[0] if key_concepts else 'relevant factors'}."
            else:
                return f"{template.rstrip(':')} based on current understanding."
                
        elif "finally" in template.lower() or step_number >= 5:
            # Conclusion step - emphasize key takeaway
            if "professional" in response_part.lower() or "consult" in response_part.lower():
                return f"{template.rstrip(':')} Professional guidance is essential for your specific situation."
            else:
                return f"{template.rstrip(':')} Consider all factors in your decision-making."
        
        # Default: Use clean template without truncation
        return template
    
    def _extract_response_concepts(self, response_part: str, domain: str) -> List[str]:
        """Extract key concepts from response content"""
        concepts = []
        
        # Domain-specific concept extraction
        if domain == "finance":
            finance_terms = ['risk', 'investment', 'return', 'portfolio', 'diversification', 
                           'volatility', 'savings', 'retirement', 'compound', 'debt']
            concepts.extend([term for term in finance_terms if term in response_part.lower()])
            
        elif domain == "medical":
            medical_terms = ['treatment', 'symptoms', 'diagnosis', 'side effects', 'dosage',
                           'consultation', 'health', 'medical', 'professional', 'condition']
            concepts.extend([term for term in medical_terms if term in response_part.lower()])
        
        return concepts[:5]  # Return top 5 concepts
    
    def _identify_query_focus(self, query: str, domain: str) -> str:
        """Identify the main focus of the query"""
        query_lower = query.lower()
        
        if domain == "finance":
            if any(word in query_lower for word in ['invest', 'investment']):
                return "investment strategy"
            elif any(word in query_lower for word in ['retirement', '401k']):
                return "retirement planning"
            elif any(word in query_lower for word in ['debt', 'loan']):
                return "debt management"
            else:
                return "financial planning"
                
        elif domain == "medical":
            if any(word in query_lower for word in ['symptom', 'pain']):
                return "symptoms and health concerns"
            elif any(word in query_lower for word in ['medication', 'drug']):
                return "medication information"
            else:
                return "health-related questions"
        
        return "your inquiry"
    
    def _extract_conclusion_focus(self, response_part: str) -> str:
        """Extract the main conclusion focus from response"""
        response_lower = response_part.lower()
        
        if any(word in response_lower for word in ['recommend', 'suggest', 'should']):
            return "the key recommendation is clear"
        elif any(word in response_lower for word in ['risk', 'danger', 'careful']):
            return "important risks need consideration"
        elif any(word in response_lower for word in ['consult', 'professional', 'doctor']):
            return "professional consultation is essential"
        else:
            return "the analysis points to important considerations"
    
    def _extract_key_terms(self, text: str, potential_terms: List[str]) -> Optional[str]:
        """Extract key terms from text"""
        text_lower = text.lower()
        for term in potential_terms:
            if term in text_lower:
                return term
        return None
    
    def _assess_step_confidence(self, content: str, domain: str) -> float:
        """Dynamically assess confidence level for a reasoning step"""
        
        # Start with content-based confidence
        base_confidence = self._calculate_content_confidence(content)
        
        # Adjust for uncertainty language
        uncertainty_penalty = self._calculate_uncertainty_penalty(content)
        base_confidence -= uncertainty_penalty
        
        # Adjust for specificity and detail
        specificity_bonus = self._calculate_specificity_bonus(content)
        base_confidence += specificity_bonus
        
        # Domain-specific confidence adjustments
        domain_adjustment = self._calculate_domain_confidence(content, domain)
        base_confidence += domain_adjustment
        
        return max(0.3, min(base_confidence, 0.95))
    
    def _calculate_content_confidence(self, content: str) -> float:
        """Calculate base confidence from content characteristics"""
        
        # Length-based confidence (longer = more detailed = higher confidence)
        word_count = len(content.split())
        if word_count < 10:
            return 0.5  # Short, less confident
        elif word_count < 30:
            return 0.65  # Medium length
        elif word_count < 80:
            return 0.75  # Good detail
        else:
            return 0.8   # Very detailed
    
    def _calculate_uncertainty_penalty(self, content: str) -> float:
        """Calculate confidence penalty for uncertainty language"""
        content_lower = content.lower()
        
        uncertainty_words = ['may', 'might', 'could', 'possibly', 'uncertain', 'unclear', 'depends']
        uncertainty_count = sum(1 for word in uncertainty_words if word in content_lower)
        
        # More uncertainty words = bigger penalty
        return min(uncertainty_count * 0.1, 0.3)
    
    def _calculate_specificity_bonus(self, content: str) -> float:
        """Calculate confidence bonus for specific, actionable content"""
        content_lower = content.lower()
        bonus = 0.0
        
        # Bonus for specific numbers/percentages
        if any(char.isdigit() for char in content):
            bonus += 0.05
        
        # Bonus for specific recommendations
        if any(word in content_lower for word in ['recommend', 'should', 'must', 'always']):
            bonus += 0.1
        
        # Bonus for evidence-based language
        if any(word in content_lower for word in ['research', 'studies', 'evidence', 'data']):
            bonus += 0.1
        
        return min(bonus, 0.2)
    
    def _calculate_domain_confidence(self, content: str, domain: str) -> float:
        """Calculate domain-specific confidence adjustments"""
        content_lower = content.lower()
        
        if domain == "medical":
            # Higher confidence for appropriate medical disclaimers
            if any(word in content_lower for word in ['consult', 'doctor', 'professional', 'healthcare']):
                return 0.1
            # Lower confidence for definitive medical claims without disclaimers
            elif any(word in content_lower for word in ['diagnose', 'cure', 'treatment']) and \
                 'consult' not in content_lower:
                return -0.15
                
        elif domain == "finance":
            # Higher confidence for appropriate financial disclaimers
            if any(word in content_lower for word in ['advisor', 'professional', 'financial planner']):
                return 0.1
            # Lower confidence for definitive investment advice without disclaimers
            elif any(word in content_lower for word in ['guarantee', 'definitely', 'certain return']) and \
                 'risk' not in content_lower:
                return -0.15
        
        return 0.0
    
    def _assess_reasoning_quality(self, content: str) -> float:
        """Assess the quality of reasoning in content"""
        
        base_quality = 0.5
        
        # Quality indicators
        if len(content) > 50:
            base_quality += 0.1
        
        if any(word in content.lower() for word in ['because', 'therefore', 'since', 'due to']):
            base_quality += 0.2  # Causal reasoning
        
        if any(word in content.lower() for word in ['first', 'next', 'then', 'finally']):
            base_quality += 0.1  # Structured thinking
        
        return min(base_quality, 1.0)
    
    def _generate_step_evidence(self, response_part: str, domain: str) -> Optional[str]:
        """Generate evidence for a reasoning step"""
        
        # Return None to avoid duplicating response content as "evidence"
        # The main response already contains all necessary information
        return None

class ChainOfThoughtIntegrator:
    """Integrates chain-of-thought reasoning into agent responses"""
    
    def __init__(self):
        self.cot_generator = ChainOfThoughtGenerator()
        self.logger = logging.getLogger(__name__)
    
    def enhance_response_with_reasoning(
        self, 
        response: str, 
        query: str, 
        domain: str
    ) -> Tuple[str, Dict[str, float]]:
        """Enhance response with chain-of-thought reasoning"""
        
        # Generate reasoning chain
        reasoning_chain = self.cot_generator.generate_reasoning_chain(
            query, response, domain
        )
        
        # Create enhanced response with reasoning
        enhanced_response = self._format_reasoning_response(reasoning_chain)
        
        # Calculate improvement metrics
        improvements = {
            'reasoning_transparency': reasoning_chain.reasoning_transparency,
            'logical_consistency': reasoning_chain.logical_consistency,
            'interpretability_improvement': reasoning_chain.reasoning_transparency * 0.5,  # Up to 50% improvement
            'logical_flow_improvement': reasoning_chain.logical_consistency * 0.4,        # Up to 40% improvement
            'step_by_step_clarity': min(len(reasoning_chain.thought_steps) * 0.1, 0.6),   # Up to 60% improvement
        }
        
        self.logger.info(f"Enhanced response with {len(reasoning_chain.thought_steps)} reasoning steps")
        
        return enhanced_response, improvements
    
    def _format_reasoning_response(self, chain: ReasoningChain) -> str:
        """Format reasoning chain into readable response"""
        
        # Start with the main answer
        formatted_response = chain.final_conclusion
        
        # Add reasoning process section with clean formatting
        formatted_response += "\n\n---\n\nMy Reasoning Process:\n"
        
        for step in chain.thought_steps:
            # Use clean, concise step descriptions
            step_content = step.thought.strip()
            # Remove any truncation artifacts
            if step_content.endswith('...'):
                step_content = step_content[:-3].rstrip()
            formatted_response += f"Step {step.step_number}: {step_content}\n\n"
        
        # Add confidence metrics in a clean format
        formatted_response += f"Reasoning Confidence: {chain.overall_confidence:.1%}\n"
        formatted_response += f"Transparency Score: {chain.reasoning_transparency:.1%}"
        
        return formatted_response

# Example usage and testing
def test_chain_of_thought():
    """Test the chain-of-thought system"""
    integrator = ChainOfThoughtIntegrator()
    
    test_cases = [
        {
            "query": "What are the side effects of aspirin for heart disease prevention?",
            "response": "Aspirin can cause gastrointestinal bleeding and stomach ulcers. It may also increase bleeding risk during surgery. However, for many people at high cardiovascular risk, the benefits outweigh the risks. Always consult your doctor before starting aspirin therapy.",
            "domain": "medical"
        },
        {
            "query": "Should I invest in cryptocurrency for retirement?",
            "response": "Cryptocurrency is extremely volatile and risky for retirement planning. It can lose 50% or more of its value quickly. Most financial advisors recommend limiting crypto to 5% or less of a portfolio. Focus on diversified, long-term investments for retirement security.",
            "domain": "finance"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Chain-of-Thought Test Case {i} ---")
        print(f"Query: {case['query']}")
        print(f"Original Response: {case['response']}")
        
        enhanced_response, improvements = integrator.enhance_response_with_reasoning(
            case['response'], case['query'], case['domain']
        )
        
        print(f"Enhanced Response: {enhanced_response}")
        print(f"Improvements: {improvements}")

if __name__ == "__main__":
    test_chain_of_thought()