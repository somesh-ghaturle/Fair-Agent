"""
Adaptability Evaluation Module

This module implements metrics to evaluate how well the agent adapts to
different domains, contexts, and query complexities - the "A" in FAIR.
"""

import logging
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass
import re
import numpy as np

@dataclass
class AdaptabilityScore:
    """Container for adaptability evaluation results"""
    overall_adaptability: float
    domain_switching_quality: float
    cross_domain_integration: float
    context_adaptation: float
    query_complexity_handling: float
    personalization_score: float
    details: Dict[str, Any]

class AdaptabilityEvaluator:
    """
    Evaluator for adaptability metrics
    
    Assesses how well the agent adapts to different domains, contexts,
    and user requirements. A well-adapted agent should:
    - Switch seamlessly between finance and medical domains
    - Handle cross-domain queries effectively
    - Adapt to different query complexities
    - Personalize responses based on context
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Domain keywords for classification confidence
        self.finance_keywords = {
            'investment', 'stock', 'bond', 'portfolio', 'market', 'trading', 
            'financial', 'money', 'profit', 'loss', 'risk', 'return', 
            'dividend', 'equity', 'debt', 'credit', 'loan', 'insurance',
            'tax', 'revenue', 'budget', 'savings', 'retirement', 'fund'
        }
        
        self.medical_keywords = {
            'disease', 'treatment', 'medication', 'symptom', 'diagnosis',
            'health', 'medical', 'doctor', 'patient', 'therapy', 'drug',
            'surgery', 'hospital', 'clinic', 'medicine', 'dose', 'side effect',
            'infection', 'virus', 'bacteria', 'cancer', 'heart', 'brain'
        }
        
        # Cross-domain indicators
        self.cross_domain_indicators = {
            'healthcare costs', 'medical insurance', 'pharmaceutical stocks',
            'biotech investment', 'health savings account', 'medical expenses',
            'healthcare sector', 'drug pricing', 'medical device financing',
            'telemedicine economics', 'public health funding', 'research funding'
        }
        
    def evaluate_adaptability(
        self,
        response: str,
        query: str,
        detected_domain: str,
        context: Optional[Dict[str, Any]] = None
    ) -> AdaptabilityScore:
        """
        Evaluate adaptability of agent response
        
        Args:
            response: The agent's response to evaluate
            query: The original query
            detected_domain: Domain identified by orchestrator
            context: Additional context (previous queries, user profile, etc.)
            
        Returns:
            AdaptabilityScore with detailed metrics
        """
        try:
            # Evaluate different adaptability aspects
            domain_switching = self._evaluate_domain_switching_quality(
                response, query, detected_domain
            )
            
            cross_domain = self._evaluate_cross_domain_integration(
                response, query, detected_domain
            )
            
            context_adaptation = self._evaluate_context_adaptation(
                response, query, context or {}
            )
            
            complexity_handling = self._evaluate_query_complexity_handling(
                response, query
            )
            
            personalization = self._evaluate_personalization(
                response, query, context or {}
            )
            
            # Calculate overall adaptability score
            weights = {
                'domain_switching': 0.25,
                'cross_domain': 0.25,
                'context_adaptation': 0.20,
                'complexity_handling': 0.20,
                'personalization': 0.10
            }
            
            overall_adaptability = (
                weights['domain_switching'] * domain_switching +
                weights['cross_domain'] * cross_domain +
                weights['context_adaptation'] * context_adaptation +
                weights['complexity_handling'] * complexity_handling +
                weights['personalization'] * personalization
            )
            
            # Compile details
            details = {
                'query_length': len(query.split()),
                'response_length': len(response.split()),
                'detected_domain': detected_domain,
                'weights_used': weights,
                'domain_confidence': self._calculate_domain_confidence(query),
                'cross_domain_detected': self._detect_cross_domain_query(query),
                'complexity_level': self._assess_query_complexity(query)
            }
            
            return AdaptabilityScore(
                overall_adaptability=overall_adaptability,
                domain_switching_quality=domain_switching,
                cross_domain_integration=cross_domain,
                context_adaptation=context_adaptation,
                query_complexity_handling=complexity_handling,
                personalization_score=personalization,
                details=details
            )
            
        except Exception as e:
            self.logger.error(f"Error evaluating adaptability: {e}")
            return self._default_score()
    
    def _evaluate_domain_switching_quality(
        self, 
        response: str, 
        query: str, 
        detected_domain: str
    ) -> float:
        """Evaluate how well the agent switches between domains"""
        domain_switching_score = 0.5  # Base score
        
        # Check if domain was correctly identified
        query_domain_confidence = self._calculate_domain_confidence(query)
        detected_correct = self._verify_domain_detection(query, detected_domain)
        
        if detected_correct:
            domain_switching_score += 0.25  # Correct domain detection
        
        # Check if response matches the domain appropriately
        response_domain_alignment = self._check_response_domain_alignment(
            response, detected_domain
        )
        domain_switching_score += response_domain_alignment * 0.25
        
        # Penalty for unclear domain boundaries
        if query_domain_confidence < 0.7:  # Ambiguous query
            if self._response_acknowledges_ambiguity(response):
                domain_switching_score += 0.15  # Good handling of ambiguity
            else:
                domain_switching_score -= 0.1   # Poor ambiguity handling
        
        return min(domain_switching_score, 1.0)
    
    def _evaluate_cross_domain_integration(
        self, 
        response: str, 
        query: str, 
        detected_domain: str
    ) -> float:
        """Evaluate cross-domain reasoning capability"""
        cross_domain_score = 0.4  # Base score for single-domain queries
        
        # Check if query requires cross-domain knowledge
        is_cross_domain = self._detect_cross_domain_query(query)
        
        if is_cross_domain:
            # Evaluate cross-domain integration quality
            finance_concepts = self._count_domain_concepts(response, 'finance')
            medical_concepts = self._count_domain_concepts(response, 'medical')
            
            # Good cross-domain responses should include concepts from both domains
            if finance_concepts > 0 and medical_concepts > 0:
                cross_domain_score = 0.7  # Good integration
                
                # Check for explicit cross-domain connections
                if self._has_cross_domain_connections(response):
                    cross_domain_score += 0.2  # Excellent integration
                    
            elif (detected_domain == 'finance' and finance_concepts > medical_concepts) or \
                 (detected_domain == 'medical' and medical_concepts > finance_concepts):
                cross_domain_score = 0.6  # Appropriate primary focus
            else:
                cross_domain_score = 0.3  # Poor cross-domain handling
        else:
            # Single-domain query - check for appropriate domain focus
            if detected_domain == 'finance':
                finance_concepts = self._count_domain_concepts(response, 'finance')
                cross_domain_score = min(0.8, 0.5 + (finance_concepts * 0.05))
            elif detected_domain == 'medical':
                medical_concepts = self._count_domain_concepts(response, 'medical')
                cross_domain_score = min(0.8, 0.5 + (medical_concepts * 0.05))
        
        return min(cross_domain_score, 1.0)
    
    def _evaluate_context_adaptation(
        self, 
        response: str, 
        query: str, 
        context: Dict[str, Any]
    ) -> float:
        """Evaluate adaptation to context and user needs"""
        context_score = 0.5  # Base score
        
        # Check for technical level adaptation
        query_technical_level = self._assess_technical_level(query)
        response_technical_level = self._assess_technical_level(response)
        
        # Response should match or slightly exceed query technical level
        level_match = 1.0 - abs(query_technical_level - response_technical_level) / 2.0
        context_score += level_match * 0.2
        
        # Check for context from previous interactions (if available)
        if 'previous_queries' in context:
            if self._references_previous_context(response, context['previous_queries']):
                context_score += 0.15
        
        # Check for user expertise adaptation
        if 'user_expertise' in context:
            if self._adapts_to_expertise_level(response, context['user_expertise']):
                context_score += 0.15
        
        # Check for situational adaptation
        if self._adapts_to_query_urgency(response, query):
            context_score += 0.1
        
        return min(context_score, 1.0)
    
    def _evaluate_query_complexity_handling(self, response: str, query: str) -> float:
        """Evaluate how well the agent handles query complexity"""
        complexity_score = 0.5  # Base score
        
        query_complexity = self._assess_query_complexity(query)
        response_complexity = self._assess_response_complexity(response)
        
        # Response complexity should be appropriate to query complexity
        if query_complexity <= 0.3:  # Simple query
            if response_complexity <= 0.5:  # Appropriately simple response
                complexity_score = 0.8
            else:
                complexity_score = 0.6  # Over-complicated
        elif query_complexity <= 0.7:  # Moderate query
            if 0.3 <= response_complexity <= 0.8:  # Appropriate complexity
                complexity_score = 0.8
            else:
                complexity_score = 0.5  # Mismatch
        else:  # Complex query
            if response_complexity >= 0.6:  # Sufficiently detailed
                complexity_score = 0.8
                if self._has_structured_breakdown(response):
                    complexity_score += 0.1  # Bonus for structure
            else:
                complexity_score = 0.4  # Too simple for complex query
        
        # Check for appropriate complexity indicators
        if self._has_appropriate_detail_level(response, query):
            complexity_score += 0.1
        
        return min(complexity_score, 1.0)
    
    def _evaluate_personalization(
        self, 
        response: str, 
        query: str, 
        context: Dict[str, Any]
    ) -> float:
        """Evaluate personalization and user-specific adaptation"""
        personalization_score = 0.4  # Base score (most responses are generic)
        
        # Check for personalized language patterns
        if self._uses_personalized_language(response, query):
            personalization_score += 0.2
        
        # Check for user-specific considerations
        if 'user_profile' in context:
            if self._considers_user_profile(response, context['user_profile']):
                personalization_score += 0.25
        
        # Check for adaptive recommendations
        if self._provides_adaptive_recommendations(response, query):
            personalization_score += 0.15
        
        return min(personalization_score, 1.0)
    
    # Helper methods for evaluation components
    
    def _calculate_domain_confidence(self, query: str) -> float:
        """Calculate confidence in domain classification"""
        query_lower = query.lower()
        finance_count = sum(1 for keyword in self.finance_keywords if keyword in query_lower)
        medical_count = sum(1 for keyword in self.medical_keywords if keyword in query_lower)
        
        total_keywords = finance_count + medical_count
        if total_keywords == 0:
            return 0.0
        
        max_count = max(finance_count, medical_count)
        return min(max_count / (total_keywords + 1), 1.0)
    
    def _verify_domain_detection(self, query: str, detected_domain: str) -> bool:
        """Verify if domain was correctly detected"""
        query_lower = query.lower()
        finance_count = sum(1 for keyword in self.finance_keywords if keyword in query_lower)
        medical_count = sum(1 for keyword in self.medical_keywords if keyword in query_lower)
        
        if finance_count > medical_count:
            return detected_domain == 'finance'
        elif medical_count > finance_count:
            return detected_domain == 'medical'
        else:
            return detected_domain in ['cross_domain', 'unknown']  # Ambiguous queries
    
    def _check_response_domain_alignment(self, response: str, detected_domain: str) -> float:
        """Check how well response aligns with detected domain"""
        response_lower = response.lower()
        finance_count = sum(1 for keyword in self.finance_keywords if keyword in response_lower)
        medical_count = sum(1 for keyword in self.medical_keywords if keyword in response_lower)
        
        if detected_domain == 'finance':
            total = finance_count + medical_count
            return (finance_count / max(total, 1)) if total > 0 else 0.5
        elif detected_domain == 'medical':
            total = finance_count + medical_count
            return (medical_count / max(total, 1)) if total > 0 else 0.5
        else:
            return 0.7  # Cross-domain or unknown
    
    def _detect_cross_domain_query(self, query: str) -> bool:
        """Detect if query requires cross-domain knowledge"""
        query_lower = query.lower()
        return any(indicator in query_lower for indicator in self.cross_domain_indicators)
    
    def _count_domain_concepts(self, text: str, domain: str) -> int:
        """Count domain-specific concepts in text"""
        text_lower = text.lower()
        if domain == 'finance':
            return sum(1 for keyword in self.finance_keywords if keyword in text_lower)
        elif domain == 'medical':
            return sum(1 for keyword in self.medical_keywords if keyword in text_lower)
        return 0
    
    def _has_cross_domain_connections(self, response: str) -> bool:
        """Check for explicit cross-domain connections"""
        connection_patterns = [
            r'relationship between.*and',
            r'impact.*on.*health',
            r'financial.*medical',
            r'medical.*financial',
            r'healthcare.*cost',
            r'investment.*pharmaceutical',
            r'economic.*health'
        ]
        
        response_lower = response.lower()
        return any(re.search(pattern, response_lower) for pattern in connection_patterns)
    
    def _assess_technical_level(self, text: str) -> float:
        """Assess technical complexity level (0=basic, 1=expert)"""
        # Simple heuristics based on vocabulary and sentence structure
        technical_indicators = [
            r'\b\w{12,}\b',  # Long technical terms
            r'\b[A-Z]{3,}\b',  # Acronyms
            r'\d+%',  # Statistics
            r'research shows',
            r'studies indicate',
            r'according to',
            r'specifically',
            r'mechanism',
            r'protocol',
            r'methodology'
        ]
        
        matches = sum(len(re.findall(pattern, text, re.IGNORECASE)) 
                     for pattern in technical_indicators)
        text_length = len(text.split())
        
        return min(matches / max(text_length / 10, 1), 1.0)
    
    def _assess_query_complexity(self, query: str) -> float:
        """Assess query complexity level"""
        complexity_indicators = [
            len(query.split()) > 20,  # Long query
            '?' in query and query.count('?') > 1,  # Multiple questions
            ' and ' in query.lower(),  # Multiple parts
            ' or ' in query.lower(),   # Alternatives
            'compare' in query.lower(),
            'difference' in query.lower(),
            'relationship' in query.lower(),
            'impact' in query.lower(),
            'why' in query.lower(),
            'how' in query.lower()
        ]
        
        complexity_score = sum(complexity_indicators) / len(complexity_indicators)
        return complexity_score
    
    def _assess_response_complexity(self, response: str) -> float:
        """Assess response complexity level"""
        complexity_indicators = [
            len(response.split()) > 50,
            response.count('\n') > 2,  # Multiple paragraphs
            response.count('.') > 5,   # Multiple sentences
            'however' in response.lower(),
            'therefore' in response.lower(),
            'furthermore' in response.lower(),
            'specifically' in response.lower(),
            'in addition' in response.lower()
        ]
        
        complexity_score = sum(complexity_indicators) / len(complexity_indicators)
        return complexity_score
    
    def _response_acknowledges_ambiguity(self, response: str) -> bool:
        """Check if response acknowledges query ambiguity"""
        ambiguity_phrases = [
            'depending on',
            'it depends',
            'could be interpreted',
            'multiple factors',
            'various approaches',
            'different perspectives'
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in ambiguity_phrases)
    
    def _has_structured_breakdown(self, response: str) -> bool:
        """Check if response has structured breakdown for complex topics"""
        structure_indicators = [
            'step 1' in response.lower() or 'first' in response.lower(),
            'step 2' in response.lower() or 'second' in response.lower(),
            response.count('\n') > 2,
            '1.' in response or '2.' in response,
            '•' in response or '-' in response
        ]
        
        return sum(structure_indicators) >= 2
    
    def _has_appropriate_detail_level(self, response: str, query: str) -> bool:
        """Check if response detail level matches query needs"""
        query_complexity = self._assess_query_complexity(query)
        response_complexity = self._assess_response_complexity(response)
        
        # Detail level should be proportional to query complexity
        return abs(query_complexity - response_complexity) < 0.3
    
    def _uses_personalized_language(self, response: str, query: str) -> bool:
        """Check for personalized language patterns"""
        personal_indicators = [
            'you' in response.lower(),
            'your' in response.lower(),
            'for you' in response.lower(),
            'consider' in response.lower(),
            'might want to' in response.lower()
        ]
        
        return sum(personal_indicators) >= 2
    
    def _references_previous_context(self, response: str, previous_queries: List[str]) -> bool:
        """Check if response references previous context"""
        # Simple implementation - check for continuation phrases
        context_phrases = [
            'as mentioned',
            'following up',
            'building on',
            'previously',
            'continuing'
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in context_phrases)
    
    def _adapts_to_expertise_level(self, response: str, expertise_level: str) -> bool:
        """Check adaptation to user expertise level"""
        if expertise_level == 'beginner':
            return 'basic' in response.lower() or 'simple' in response.lower()
        elif expertise_level == 'expert':
            return self._assess_technical_level(response) > 0.6
        return True  # Neutral for intermediate
    
    def _adapts_to_query_urgency(self, response: str, query: str) -> bool:
        """Check adaptation to query urgency"""
        urgent_indicators = ['urgent', 'emergency', 'immediate', 'asap', 'quickly']
        
        query_urgent = any(indicator in query.lower() for indicator in urgent_indicators)
        if query_urgent:
            response_addresses_urgency = any(
                phrase in response.lower() 
                for phrase in ['immediately', 'urgent', 'seek help', 'consult now']
            )
            return response_addresses_urgency
        
        return True  # Non-urgent queries don't need special handling
    
    def _considers_user_profile(self, response: str, user_profile: Dict[str, Any]) -> bool:
        """Check if response considers user profile"""
        # Simple implementation - could be expanded based on profile structure
        if 'age' in user_profile:
            age_considerations = ['age-appropriate', 'for your age', 'at this stage']
            if any(phrase in response.lower() for phrase in age_considerations):
                return True
        
        return False  # Default implementation
    
    def _provides_adaptive_recommendations(self, response: str, query: str) -> bool:
        """Check for adaptive/personalized recommendations"""
        recommendation_phrases = [
            'i recommend',
            'you might consider',
            'it would be advisable',
            'based on your',
            'specifically for you'
        ]
        
        response_lower = response.lower()
        return any(phrase in response_lower for phrase in recommendation_phrases)
    
    def _default_score(self) -> AdaptabilityScore:
        """Return default score for error cases"""
        return AdaptabilityScore(
            overall_adaptability=0.4,  # Conservative default
            domain_switching_quality=0.4,
            cross_domain_integration=0.4,
            context_adaptation=0.4,
            query_complexity_handling=0.4,
            personalization_score=0.3,
            details={'error': 'Evaluation failed'}
        )
    
    def evaluate_batch_adaptability(
        self,
        batch_responses: List[str],
        batch_queries: List[str],
        batch_domains: List[str],
        batch_contexts: List[Dict[str, Any]]
    ) -> List[AdaptabilityScore]:
        """Evaluate adaptability for multiple responses"""
        results = []
        
        for response, query, domain, context in zip(
            batch_responses, batch_queries, batch_domains, batch_contexts
        ):
            score = self.evaluate_adaptability(response, query, domain, context)
            results.append(score)
        
        return results
    
    def get_aggregate_metrics(self, scores: List[AdaptabilityScore]) -> Dict[str, float]:
        """Calculate aggregate metrics across multiple adaptability evaluations"""
        if not scores:
            return {}
        
        return {
            'mean_adaptability': np.mean([s.overall_adaptability for s in scores]),
            'mean_domain_switching': np.mean([s.domain_switching_quality for s in scores]),
            'mean_cross_domain': np.mean([s.cross_domain_integration for s in scores]),
            'mean_context_adaptation': np.mean([s.context_adaptation for s in scores]),
            'mean_complexity_handling': np.mean([s.query_complexity_handling for s in scores]),
            'mean_personalization': np.mean([s.personalization_score for s in scores]),
            'std_adaptability': np.std([s.overall_adaptability for s in scores])
        }