"""
Cross-Domain Agent for FAIR-Agent System

This agent handles queries that span both finance and medical domains,
synthesizing responses from both specialized agents and providing
integrated analysis for cross-domain questions.

Examples of cross-domain queries:
- "How do healthcare costs affect retirement planning?"
- "What is the financial impact of chronic illness?"
- "Should I invest in pharmaceutical stocks?"
- "How does health insurance affect investment decisions?"

Author: Somesh Ghaturle
CS668 Analytics Capstone - Fall 2025
"""

import logging
from typing import Optional, Dict, List
from dataclasses import dataclass


@dataclass
class CrossDomainResponse:
    """Response structure for cross-domain queries"""
    integrated_answer: str
    finance_perspective: str
    medical_perspective: str
    synthesis: str
    confidence_score: float
    finance_confidence: float
    medical_confidence: float
    reasoning_steps: List[str]
    risk_assessment: str
    evidence_sources: List[str]
    
    # FAIR metric boosts
    safety_boost: float = 0.0
    evidence_boost: float = 0.0
    reasoning_boost: float = 0.0
    internet_boost: float = 0.0


class CrossDomainAgent:
    """
    Specialized agent for handling cross-domain queries that require
    both financial and medical expertise.
    
    This agent:
    - Coordinates between finance and medical agents
    - Synthesizes responses from both domains
    - Identifies interdependencies between domains
    - Provides integrated analysis and recommendations
    """
    
    def __init__(self, finance_agent=None, medical_agent=None):
        """
        Initialize the cross-domain agent
        
        Args:
            finance_agent: Finance domain agent instance
            medical_agent: Medical domain agent instance
        """
        self.logger = logging.getLogger(__name__)
        self.finance_agent = finance_agent
        self.medical_agent = medical_agent
        
        # Cross-domain query patterns
        self.cross_domain_keywords = {
            'healthcare_finance': [
                'health insurance', 'medical costs', 'healthcare expenses',
                'medical bills', 'health savings account', 'hsa', 'fsa',
                'medicare', 'medicaid', 'prescription costs'
            ],
            'retirement_health': [
                'retirement health', 'aging costs', 'long-term care',
                'elder care', 'retirement medical', 'senior healthcare'
            ],
            'pharma_investment': [
                'pharmaceutical stocks', 'biotech investment', 'healthcare sector',
                'medical device companies', 'drug companies', 'pharma industry'
            ],
            'disability_finance': [
                'disability insurance', 'illness financial impact', 'chronic illness costs',
                'disease financial burden', 'medical bankruptcy'
            ]
        }
        
        self.logger.info("✅ Cross-Domain Agent initialized")
    
    def query(self, question: str, context: Optional[Dict] = None) -> CrossDomainResponse:
        """
        Process a cross-domain query
        
        Args:
            question: User query spanning both domains
            context: Optional context information
            
        Returns:
            CrossDomainResponse with integrated analysis
        """
        self.logger.info(f"[CROSS-DOMAIN] Processing query: {question[:100]}...")
        
        try:
            # Step 1: Get responses from both specialized agents
            finance_response = self.finance_agent.query(question, context) if self.finance_agent else None
            medical_response = self.medical_agent.query(question, context) if self.medical_agent else None
            
            # Step 2: Identify cross-domain category
            category = self._identify_cross_domain_category(question)
            
            # Step 3: Synthesize integrated response
            integrated_answer = self._synthesize_integrated_response(
                question, finance_response, medical_response, category
            )
            
            # Step 4: Generate reasoning steps
            reasoning_steps = self._generate_cross_domain_reasoning(
                question, finance_response, medical_response, category
            )
            
            # Step 5: Assess combined risks
            risk_assessment = self._assess_cross_domain_risks(
                finance_response, medical_response
            )
            
            # Step 6: Collect evidence sources from both domains
            evidence_sources = self._collect_evidence_sources(
                finance_response, medical_response
            )
            
            # Step 7: Calculate integrated confidence
            confidence_score = self._calculate_integrated_confidence(
                finance_response, medical_response
            )
            
            # Step 8: Aggregate FAIR metric boosts
            safety_boost = max(
                getattr(finance_response, 'safety_boost', 0.0),
                getattr(medical_response, 'safety_boost', 0.0)
            )
            evidence_boost = (
                getattr(finance_response, 'evidence_boost', 0.0) +
                getattr(medical_response, 'evidence_boost', 0.0)
            ) / 2.0  # Average evidence from both domains
            reasoning_boost = max(
                getattr(finance_response, 'reasoning_boost', 0.0),
                getattr(medical_response, 'reasoning_boost', 0.0)
            )
            internet_boost = (
                getattr(finance_response, 'internet_boost', 0.0) +
                getattr(medical_response, 'internet_boost', 0.0)
            ) / 2.0
            
            return CrossDomainResponse(
                integrated_answer=integrated_answer,
                finance_perspective=finance_response.answer if finance_response else "",
                medical_perspective=medical_response.answer if medical_response else "",
                synthesis=self._create_synthesis_summary(finance_response, medical_response),
                confidence_score=confidence_score,
                finance_confidence=finance_response.confidence_score if finance_response else 0.0,
                medical_confidence=medical_response.confidence_score if medical_response else 0.0,
                reasoning_steps=reasoning_steps,
                risk_assessment=risk_assessment,
                evidence_sources=evidence_sources,
                safety_boost=safety_boost,
                evidence_boost=evidence_boost,
                reasoning_boost=reasoning_boost,
                internet_boost=internet_boost
            )
            
        except Exception as e:
            self.logger.error(f"Error processing cross-domain query: {e}")
            return self._create_fallback_response(question)
    
    def _identify_cross_domain_category(self, query: str) -> str:
        """Identify the specific cross-domain category"""
        query_lower = query.lower()
        
        for category, keywords in self.cross_domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return category
        
        return "general_cross_domain"
    
    def _synthesize_integrated_response(
        self, 
        query: str, 
        finance_response, 
        medical_response, 
        category: str
    ) -> str:
        """Synthesize an integrated response from both domains"""
        
        synthesis = f"## Cross-Domain Analysis: {category.replace('_', ' ').title()}\n\n"
        
        # Add finance perspective
        if finance_response:
            synthesis += "### 💰 Financial Perspective:\n"
            synthesis += finance_response.answer[:500] + "...\n\n"
        
        # Add medical perspective
        if medical_response:
            synthesis += "### 🏥 Medical Perspective:\n"
            synthesis += medical_response.answer[:500] + "...\n\n"
        
        # Add integration section
        synthesis += "### 🔄 Integrated Analysis:\n"
        synthesis += self._generate_integration_insights(query, finance_response, medical_response, category)
        
        return synthesis
    
    def _generate_integration_insights(
        self, 
        query: str, 
        finance_response, 
        medical_response, 
        category: str
    ) -> str:
        """Generate insights that integrate both perspectives"""
        
        insights = []
        
        if category == "healthcare_finance":
            insights.append("**Cost-Benefit Analysis**: Healthcare decisions should balance medical necessity with financial sustainability.")
            insights.append("**Planning Strategies**: Consider Health Savings Accounts (HSAs) and appropriate insurance coverage.")
        
        elif category == "retirement_health":
            insights.append("**Long-term Planning**: Retirement planning must account for increasing healthcare costs with age.")
            insights.append("**Insurance Considerations**: Medicare supplemental plans and long-term care insurance are critical components.")
        
        elif category == "pharma_investment":
            insights.append("**Risk-Reward Balance**: Pharmaceutical investments can be volatile but may align with healthcare trends.")
            insights.append("**Industry Knowledge**: Understanding FDA approval processes and patent cliffs is essential.")
        
        elif category == "disability_finance":
            insights.append("**Protection Strategies**: Disability insurance and emergency funds are crucial for financial resilience.")
            insights.append("**Income Replacement**: Plan for 60-70% income replacement in case of disability.")
        
        return "\n".join(f"- {insight}" for insight in insights)
    
    def _generate_cross_domain_reasoning(
        self, 
        query: str, 
        finance_response, 
        medical_response, 
        category: str
    ) -> List[str]:
        """Generate reasoning steps for cross-domain analysis"""
        
        steps = [
            "Identified query as cross-domain (finance + medical)",
            f"Classified as: {category.replace('_', ' ')}",
            "Consulted both finance and medical experts",
            "Analyzed financial implications of health considerations",
            "Evaluated medical impacts on financial decisions",
            "Synthesized integrated recommendations",
            "Applied safety disclaimers from both domains"
        ]
        
        return steps
    
    def _assess_cross_domain_risks(self, finance_response, medical_response) -> str:
        """Assess risks from both domains"""
        
        risks = []
        
        if finance_response:
            risks.append("**Financial Risks**: Market volatility, economic changes, investment losses")
        
        if medical_response:
            risks.append("**Medical Risks**: Health outcomes, treatment effectiveness, medical costs")
        
        risks.append("**Integration Risks**: Decisions in one domain may impact the other significantly")
        
        return "\n".join(risks)
    
    def _collect_evidence_sources(self, finance_response, medical_response) -> List[str]:
        """Collect evidence sources from both domains"""
        
        sources = []
        
        if finance_response and hasattr(finance_response, 'evidence_sources'):
            sources.extend([f"[Finance] {s}" for s in finance_response.evidence_sources])
        
        if medical_response and hasattr(medical_response, 'evidence_sources'):
            sources.extend([f"[Medical] {s}" for s in medical_response.evidence_sources])
        
        return sources
    
    def _calculate_integrated_confidence(self, finance_response, medical_response) -> float:
        """Calculate integrated confidence from both agents"""
        
        if finance_response and medical_response:
            # Average confidence with weight towards higher confidence
            avg_confidence = (finance_response.confidence_score + medical_response.confidence_score) / 2.0
            max_confidence = max(finance_response.confidence_score, medical_response.confidence_score)
            
            # Weighted combination: 60% average, 40% max
            return (avg_confidence * 0.6) + (max_confidence * 0.4)
        
        elif finance_response:
            return finance_response.confidence_score * 0.8  # Reduce for single domain
        
        elif medical_response:
            return medical_response.confidence_score * 0.8
        
        return 0.5  # Fallback
    
    def _create_synthesis_summary(self, finance_response, medical_response) -> str:
        """Create a summary of the synthesis"""
        
        summary = "This cross-domain analysis integrates "
        
        if finance_response and medical_response:
            summary += "financial and medical perspectives to provide comprehensive guidance. "
            summary += "Both domains contribute important considerations that should be evaluated together."
        elif finance_response:
            summary += "primarily financial analysis with health-related considerations."
        elif medical_response:
            summary += "primarily medical analysis with financial implications."
        
        return summary
    
    def _create_fallback_response(self, query: str) -> CrossDomainResponse:
        """Create a fallback response for errors"""
        
        return CrossDomainResponse(
            integrated_answer="I apologize, but I encountered an error processing your cross-domain query. Please try rephrasing your question or contact support.",
            finance_perspective="",
            medical_perspective="",
            synthesis="Error in cross-domain processing",
            confidence_score=0.3,
            finance_confidence=0.0,
            medical_confidence=0.0,
            reasoning_steps=["Error occurred during cross-domain analysis"],
            risk_assessment="Unable to assess risks due to processing error",
            evidence_sources=[],
            safety_boost=0.0,
            evidence_boost=0.0,
            reasoning_boost=0.0,
            internet_boost=0.0
        )
