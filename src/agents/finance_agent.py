"""
Finance Agent Module for FAIR-Agent System

This module implements a specialized LLM agent for financial domain queries,
focusing on numerical reasoning over financial data with emphasis on
faithfulness, adaptability, interpretability, and risk-awareness.
"""

import logging
from typing import Dict, List, Optional, Union
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from dataclasses import dataclass

@dataclass
class FinanceResponse:
    """Response structure for finance agent queries"""
    answer: str
    confidence_score: float
    reasoning_steps: List[str]
    risk_assessment: str
    numerical_outputs: Dict[str, float]

class FinanceAgent:
    """
    Finance Agent specializing in financial reasoning tasks
    
    Handles queries related to:
    - Financial statement analysis
    - Numerical reasoning over financial data
    - Risk assessment and portfolio analysis
    - Market trend analysis
    """
    
    def __init__(
        self, 
        model_name: str = "meta-llama/Llama-2-7b-hf",
        device: str = "auto",
        max_length: int = 512
    ):
        """
        Initialize the Finance Agent
        
        Args:
            model_name: HuggingFace model identifier for financial reasoning
            device: Device to run the model on ('cpu', 'cuda', or 'auto')
            max_length: Maximum token length for generation
        """
        self.model_name = model_name
        self.device = device
        self.max_length = max_length
        self.logger = logging.getLogger(__name__)
        
        # Initialize tokenizer and model
        self._load_model()
        
    def _load_model(self):
        """Load the tokenizer and model for financial reasoning"""
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
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
            
            self.logger.info(f"Finance Agent loaded with model: {self.model_name}")
            
        except Exception as e:
            self.logger.error(f"Failed to load finance model: {e}")
            raise
    
    def query(
        self, 
        question: str, 
        context: Optional[Dict] = None,
        return_confidence: bool = True
    ) -> FinanceResponse:
        """
        Process a financial query and return a structured response
        
        Args:
            question: The financial question to answer
            context: Additional context (financial data, tables, etc.)
            return_confidence: Whether to compute confidence scores
            
        Returns:
            FinanceResponse with answer, confidence, reasoning, and risk assessment
        """
        try:
            # Construct prompt for financial reasoning
            prompt = self._construct_finance_prompt(question, context)
            
            # Generate response
            response = self.pipeline(
                prompt,
                max_length=self.max_length,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            generated_text = response[0]['generated_text'][len(prompt):]
            
            # Parse and structure the response
            structured_response = self._parse_finance_response(
                generated_text, 
                question,
                return_confidence
            )
            
            return structured_response
            
        except Exception as e:
            self.logger.error(f"Error processing finance query: {e}")
            return FinanceResponse(
                answer="Error processing query",
                confidence_score=0.0,
                reasoning_steps=["Error occurred during processing"],
                risk_assessment="Unable to assess",
                numerical_outputs={}
            )
    
    def _construct_finance_prompt(self, question: str, context: Optional[Dict] = None) -> str:
        """Construct a specialized prompt for financial reasoning"""
        prompt_template = """You are a financial expert AI assistant. Answer the following question with step-by-step reasoning, focusing on numerical accuracy and risk assessment.

Question: {question}

{context_section}

Please provide:
1. A clear, accurate answer
2. Step-by-step reasoning
3. Risk assessment
4. Any relevant numerical calculations

Answer:"""
        
        context_section = ""
        if context:
            context_section = f"Context: {context}\n"
        
        return prompt_template.format(
            question=question,
            context_section=context_section
        )
    
    def _parse_finance_response(
        self, 
        generated_text: str, 
        question: str,
        return_confidence: bool = True
    ) -> FinanceResponse:
        """Parse the generated response into structured format"""
        # Clean up the generated text
        text = generated_text.strip()
        
        # If text is empty, provide a fallback
        if not text:
            text = "I apologize, but I couldn't generate a complete response to your financial query."
        
        # Split into lines and filter out empty ones
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Use the first non-empty line as the primary answer, or the full text if short
        if len(text) <= 200:
            answer = text
        else:
            answer = lines[0] if lines else text[:200] + "..."
        
        reasoning_steps = lines[:5] if len(lines) > 1 else [answer]
        
        # Extract numerical outputs (simplified implementation)
        numerical_outputs = self._extract_numbers(generated_text)
        
        # Compute confidence score (simplified heuristic)
        confidence_score = 0.8 if return_confidence else 0.0
        
        # Basic risk assessment
        risk_assessment = self._assess_financial_risk(generated_text)
        
        return FinanceResponse(
            answer=answer,
            confidence_score=confidence_score,
            reasoning_steps=reasoning_steps[:5],  # Limit to top 5 steps
            risk_assessment=risk_assessment,
            numerical_outputs=numerical_outputs
        )
    
    def _extract_numbers(self, text: str) -> Dict[str, float]:
        """Extract numerical values from response text"""
        import re
        
        numbers = {}
        # Simple regex to find numbers (can be enhanced)
        number_pattern = r'(\$?[\d,]+\.?\d*)'
        matches = re.findall(number_pattern, text)
        
        for i, match in enumerate(matches[:5]):  # Limit to 5 numbers
            clean_number = match.replace('$', '').replace(',', '')
            try:
                numbers[f'value_{i+1}'] = float(clean_number)
            except ValueError:
                continue
                
        return numbers
    
    def _assess_financial_risk(self, text: str) -> str:
        """Provide basic risk assessment based on response content"""
        risk_keywords = {
            'high': ['volatile', 'risky', 'uncertain', 'fluctuation', 'crisis'],
            'medium': ['moderate', 'stable', 'average', 'standard'],
            'low': ['safe', 'secure', 'guaranteed', 'conservative', 'minimal']
        }
        
        text_lower = text.lower()
        
        for risk_level, keywords in risk_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                return f"{risk_level.capitalize()} risk identified"
        
        return "Risk assessment requires further analysis"
    
    def evaluate_faithfulness(self, response: FinanceResponse, ground_truth: str) -> float:
        """Evaluate faithfulness of the response against ground truth"""
        # Simplified faithfulness metric
        # In practice, this would use more sophisticated metrics
        answer_tokens = set(response.answer.lower().split())
        truth_tokens = set(ground_truth.lower().split())
        
        if not truth_tokens:
            return 0.0
            
        intersection = len(answer_tokens.intersection(truth_tokens))
        union = len(answer_tokens.union(truth_tokens))
        
        return intersection / union if union > 0 else 0.0