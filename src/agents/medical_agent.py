"""
Medical Agent Module for FAIR-Agent System

This module implements a specialized LLM agent for medical domain queries,
focusing on biomedical reasoning with emphasis on faithfulness, adaptability,
interpretability, and risk-awareness in healthcare contexts.
"""

import logging
from typing import Dict, List, Optional, Union
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from dataclasses import dataclass
import sys
import os

# Add enhancement modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'safety'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'evidence'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'reasoning'))
from disclaimer_system import ResponseEnhancer
from rag_system import RAGSystem
from cot_system import ChainOfThoughtIntegrator 

@dataclass
class MedicalResponse:
    """Response structure for medical agent queries"""
    answer: str
    confidence_score: float
    reasoning_steps: List[str]
    safety_assessment: str
    medical_evidence: List[str]
    uncertainty_indicators: List[str]

class MedicalAgent:
    """
    Medical Agent specializing in biomedical reasoning tasks
    
    Handles queries related to:
    - Clinical decision support
    - Biomedical literature analysis
    - Drug interaction analysis
    - Symptom assessment and diagnosis support
    """
    
    def __init__(
        self, 
        model_name: str = "microsoft/BioGPT-Large",
        device: str = "auto",
        max_length: int = 512
    ):
        """
        Initialize the Medical Agent
        
        Args:
            model_name: HuggingFace model identifier for medical reasoning
            device: Device to run the model on ('cpu', 'cuda', or 'auto')
            max_length: Maximum token length for generation
        """
        self.model_name = model_name
        self.device = device
        self.max_length = max_length
        self.logger = logging.getLogger(__name__)
        
        # Initialize all enhancement systems
        self.response_enhancer = ResponseEnhancer()
        self.rag_system = RAGSystem()
        self.cot_integrator = ChainOfThoughtIntegrator()
        
        # Initialize tokenizer and model
        self._load_model()
        
    def _load_model(self):
        """Load the tokenizer and model for medical reasoning"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            
            # Handle models without pad token
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                device_map=self.device if self.device != "auto" else None
            )
            
            # Set up text generation pipeline
            self.pipeline = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device_map=self.device if self.device != "auto" else None
            )
            
            self.logger.info(f"Medical Agent loaded with model: {self.model_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load medical model: {e}")
            raise
    
    def query(
        self, 
        question: str, 
        context: Optional[Dict] = None,
        safety_check: bool = True
    ) -> MedicalResponse:
        """
        Process a medical query and return a structured response
        
        Args:
            question: The medical question to answer
            context: Additional context (patient data, medical history, etc.)
            safety_check: Whether to perform safety assessment
            
        Returns:
            MedicalResponse with answer, confidence, reasoning, and safety assessment
        """
        try:
            # Safety check for harmful queries
            if safety_check and self._is_harmful_query(question):
                return self._safe_response("Query requires professional medical consultation")
            
            # Construct prompt for medical reasoning
            prompt = self._construct_medical_prompt(question, context)
            
            # Generate response
            response = self.pipeline(
                prompt,
                max_length=self.max_length,
                temperature=0.3,  # Lower temperature for medical accuracy
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
            
            generated_text = response[0]['generated_text'][len(prompt):]
            
            # Parse and structure the response
            structured_response = self._parse_medical_response(
                generated_text, 
                question,
                safety_check
            )
            
            return structured_response
            
        except Exception as e:
            self.logger.error(f"Error processing medical query: {e}")
            return self._safe_response("Error processing medical query")
    
    def _construct_medical_prompt(self, question: str, context: Optional[Dict] = None) -> str:
        """Construct a specialized prompt for medical reasoning"""
        prompt_template = """You are a medical AI assistant. Provide evidence-based medical information with appropriate disclaimers.

IMPORTANT: Always include appropriate medical disclaimers and recommend consulting healthcare professionals for medical decisions.

Question: {question}

{context_section}

Please provide:
1. Evidence-based medical information
2. Step-by-step reasoning
3. Relevant medical evidence
4. Uncertainty indicators
5. Appropriate disclaimers

Response:"""
        
        context_section = ""
        if context:
            context_section = f"Context: {context}\n"
        
        return prompt_template.format(
            question=question,
            context_section=context_section
        )
    
    def _parse_medical_response(
        self, 
        generated_text: str, 
        question: str,
        safety_check: bool = True
    ) -> MedicalResponse:
        """Parse the generated response into structured format"""
        # Clean up the generated text
        text = generated_text.strip()
        
        # If text is empty, provide a medical disclaimer
        if not text:
            text = "I apologize, but I couldn't generate a complete response. Please consult with a healthcare professional for medical advice."
        
        # Split into lines and filter out empty ones
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Use the first non-empty line as the primary answer, or the full text if short
        if len(text) <= 200:
            answer = text
        else:
            answer = lines[0] if lines else text[:200] + "..."
        
        reasoning_steps = lines[:5] if len(lines) > 1 else [answer]
        
        # Extract medical evidence and uncertainty indicators
        medical_evidence = self._extract_medical_evidence(generated_text)
        uncertainty_indicators = self._extract_uncertainty_indicators(generated_text)
        
        # Compute confidence score with medical context
        confidence_score = self._compute_medical_confidence(generated_text)
        
        # Safety assessment
        safety_assessment = self._assess_medical_safety(generated_text) if safety_check else "Safety check skipped"
        
        # Apply all enhancement systems
        
        # Step 1: Enhance with disclaimers
        enhanced_answer, safety_improvements = self.response_enhancer.enhance_response(
            answer, question, "medical"
        )
        
        # Step 2: Enhance with evidence citations
        evidence_enhanced_answer, evidence_improvements = self.rag_system.enhance_agent_response(
            enhanced_answer, question, "medical"
        )
        
        # Step 3: Enhance with chain-of-thought reasoning
        final_enhanced_answer, reasoning_improvements = self.cot_integrator.enhance_response_with_reasoning(
            evidence_enhanced_answer, question, "medical"
        )
        
        # Calculate combined confidence score
        base_confidence = confidence_score
        safety_boost = safety_improvements.get('overall_safety_improvement', 0.0)
        evidence_boost = evidence_improvements.get('faithfulness_improvement', 0.0)
        reasoning_boost = reasoning_improvements.get('interpretability_improvement', 0.0)
        
        enhanced_confidence = min(base_confidence + safety_boost + evidence_boost + reasoning_boost, 1.0)
        
        self.logger.info(f"Medical response enhanced with all systems: safety (+{safety_boost:.2f}), evidence (+{evidence_boost:.2f}), reasoning (+{reasoning_boost:.2f})")
        
        return MedicalResponse(
            answer=final_enhanced_answer,
            confidence_score=enhanced_confidence,
            reasoning_steps=reasoning_steps[:5],
            safety_assessment=safety_assessment,
            medical_evidence=medical_evidence,
            uncertainty_indicators=uncertainty_indicators
        )
    
    def _is_harmful_query(self, question: str) -> bool:
        """Check if query might be harmful or inappropriate"""
        harmful_indicators = [
            'self-harm', 'suicide', 'illegal drugs', 'prescription without doctor',
            'dangerous procedures', 'unproven treatments'
        ]
        
        question_lower = question.lower()
        return any(indicator in question_lower for indicator in harmful_indicators)
    
    def _safe_response(self, message: str) -> MedicalResponse:
        """Return a safe default response for problematic queries"""
        return MedicalResponse(
            answer=message,
            confidence_score=0.0,
            reasoning_steps=["Professional medical consultation recommended"],
            safety_assessment="Query flagged for safety review",
            medical_evidence=["Consult healthcare professional"],
            uncertainty_indicators=["High uncertainty - medical supervision required"]
        )
    
    def _extract_medical_evidence(self, text: str) -> List[str]:
        """Extract medical evidence from response text"""
        evidence_keywords = ['study shows', 'research indicates', 'clinical trial', 'evidence suggests']
        evidence = []
        
        sentences = text.split('.')
        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in evidence_keywords):
                evidence.append(sentence.strip())
        
        return evidence[:3]  # Limit to top 3 evidence pieces
    
    def _extract_uncertainty_indicators(self, text: str) -> List[str]:
        """Extract uncertainty indicators from medical response"""
        uncertainty_keywords = ['may', 'might', 'could', 'possibly', 'uncertain', 'unclear']
        indicators = []
        
        text_lower = text.lower()
        for keyword in uncertainty_keywords:
            if keyword in text_lower:
                indicators.append(f"Uncertainty indicator: {keyword}")
        
        return indicators[:3]  # Limit to top 3 indicators
    
    def _compute_medical_confidence(self, text: str) -> float:
        """Compute confidence score for medical response"""
        # Factors that increase confidence
        confidence_factors = ['evidence', 'study', 'research', 'clinical', 'proven']
        # Factors that decrease confidence
        uncertainty_factors = ['may', 'might', 'unclear', 'uncertain', 'varies']
        
        text_lower = text.lower()
        
        confidence_count = sum(1 for factor in confidence_factors if factor in text_lower)
        uncertainty_count = sum(1 for factor in uncertainty_factors if factor in text_lower)
        
        # Base confidence adjusted by factors
        base_confidence = 0.5
        confidence_adjustment = (confidence_count - uncertainty_count) * 0.1
        
        return max(0.0, min(1.0, base_confidence + confidence_adjustment))
    
    def _assess_medical_safety(self, text: str) -> str:
        """Assess safety of medical response"""
        safety_indicators = {
            'safe': ['consult doctor', 'see physician', 'medical professional', 'healthcare provider'],
            'caution': ['side effects', 'contraindications', 'allergic reaction'],
            'warning': ['dangerous', 'harmful', 'avoid', 'emergency']
        }
        
        text_lower = text.lower()
        
        for safety_level, keywords in safety_indicators.items():
            if any(keyword in text_lower for keyword in keywords):
                return f"Safety level: {safety_level}"
        
        return "Safety assessment: Standard medical information provided"
    
    def evaluate_faithfulness(self, response: MedicalResponse, ground_truth: str) -> float:
        """Evaluate faithfulness of medical response against ground truth"""
        # Medical faithfulness considers evidence alignment
        answer_concepts = set(response.answer.lower().split())
        truth_concepts = set(ground_truth.lower().split())
        
        if not truth_concepts:
            return 0.0
        
        # Weight medical evidence more heavily
        evidence_alignment = 0.0
        if response.medical_evidence:
            evidence_text = ' '.join(response.medical_evidence).lower()
            evidence_concepts = set(evidence_text.split())
            evidence_alignment = len(evidence_concepts.intersection(truth_concepts)) / len(truth_concepts)
        
        # Standard concept alignment
        concept_alignment = len(answer_concepts.intersection(truth_concepts)) / len(truth_concepts)
        
        # Combined faithfulness score (weighted)
        return 0.7 * concept_alignment + 0.3 * evidence_alignment