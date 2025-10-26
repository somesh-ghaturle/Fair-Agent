"""
Safety Disclaimer System for FAIR-Agent

This module implements template-based safety disclaimers to improve
safety scores and ensure appropriate warnings for medical and financial advice.
"""

import re
from typing import Dict, List, Optional, Tuple
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class DisclaimerType(Enum):
    """Types of disclaimers available"""
    MEDICAL = "medical"
    FINANCIAL = "financial"
    GENERAL_HEALTH = "general_health"
    INVESTMENT_RISK = "investment_risk"
    EMERGENCY = "emergency"
    PROFESSIONAL_CONSULTATION = "professional_consultation"

class SafetyDisclaimerManager:
    """Manages safety disclaimers for agent responses"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.disclaimers = self._load_disclaimer_templates()
        self.trigger_patterns = self._load_trigger_patterns()
    
    def _load_disclaimer_templates(self) -> Dict[DisclaimerType, List[str]]:
        """Load disclaimer templates for different contexts"""
        return {
            DisclaimerType.MEDICAL: [
                "⚠️ **MEDICAL DISCLAIMER**: This information is for educational purposes only and does not constitute medical advice. Always consult with qualified healthcare professionals for medical concerns, diagnosis, and treatment decisions.",
                
                "🏥 **IMPORTANT**: This response provides general health information only. It should not replace professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.",
                
                "⚕️ **HEALTHCARE NOTICE**: Never disregard professional medical advice or delay seeking it because of information provided here. If you think you may have a medical emergency, call your doctor or emergency services immediately."
            ],
            
            DisclaimerType.FINANCIAL: [
                "💰 **FINANCIAL DISCLAIMER**: This information is for educational purposes only and does not constitute financial advice. Past performance does not guarantee future results. Investment values may fluctuate and you may lose money.",
                
                "📈 **INVESTMENT WARNING**: All investments carry risk including potential loss of principal. Consider consulting with qualified financial advisors before making investment decisions. This information should not be considered personalized investment advice.",
                
                "💸 **RISK NOTICE**: Financial markets are subject to volatility and uncertainty. Never invest money you cannot afford to lose. Consider your risk tolerance, investment objectives, and time horizon before making financial decisions."
            ],
            
            DisclaimerType.EMERGENCY: [
                "🚨 **EMERGENCY NOTICE**: If you are experiencing a medical emergency, call 911 (or your local emergency number) immediately. Do not rely on online information for emergency medical situations.",
                
                "⚡ **URGENT**: For immediate medical attention, contact emergency services. This information cannot replace emergency medical care or professional medical evaluation.",
                
                "🆘 **CRISIS RESOURCES**: If you're having thoughts of self-harm, contact the National Suicide Prevention Lifeline at 988 or your local crisis helpline immediately."
            ],
            
            DisclaimerType.PROFESSIONAL_CONSULTATION: [
                "👨‍⚕️ **PROFESSIONAL CONSULTATION RECOMMENDED**: For personalized advice tailored to your specific situation, please consult with qualified professionals in the relevant field.",
                
                "🎓 **EXPERT GUIDANCE**: This general information should be supplemented with professional consultation to address your individual circumstances and needs.",
                
                "📞 **SEEK PROFESSIONAL HELP**: Complex situations require professional evaluation. Consider scheduling a consultation with appropriate specialists."
            ]
        }
    
    def _load_trigger_patterns(self) -> Dict[DisclaimerType, List[str]]:
        """Load patterns that trigger specific disclaimers"""
        return {
            DisclaimerType.MEDICAL: [
                # Medication-related
                r'\b(medication|drug|prescription|dosage|pill|tablet|injection|insulin|antibiotic)\b',
                # Symptoms and conditions
                r'\b(symptom|pain|fever|headache|chest pain|shortness of breath|bleeding|diabetes|hypertension|cancer)\b',
                # Medical procedures
                r'\b(surgery|treatment|therapy|diagnosis|test|screening|examination)\b',
                # Body systems
                r'\b(heart|lung|liver|kidney|brain|blood|cardiovascular|respiratory)\b'
            ],
            
            DisclaimerType.FINANCIAL: [
                # Investment terms
                r'\b(invest|investment|stock|bond|mutual fund|ETF|cryptocurrency|bitcoin|portfolio)\b',
                # Financial planning
                r'\b(retirement|401k|IRA|savings|pension|financial planning|wealth)\b',
                # Risk and returns
                r'\b(return|profit|loss|risk|volatile|market|trading|buy|sell)\b',
                # Financial institutions
                r'\b(bank|broker|advisor|financial|credit|loan|mortgage|insurance)\b'
            ],
            
            DisclaimerType.EMERGENCY: [
                # Emergency symptoms
                r'\b(chest pain|difficulty breathing|severe bleeding|unconscious|overdose|poisoning)\b',
                # Crisis situations
                r'\b(suicide|self-harm|emergency|911|urgent|immediate|crisis)\b',
                # Severe conditions
                r'\b(heart attack|stroke|seizure|anaphylaxis|severe allergic reaction)\b'
            ]
        }
    
    def analyze_response_for_disclaimers(self, response: str, query: str, domain: str) -> List[DisclaimerType]:
        """Analyze response to determine what disclaimers are needed"""
        needed_disclaimers = []
        combined_text = f"{query} {response}".lower()
        
        # Check for emergency patterns ONLY if content actually contains emergency-related terms
        emergency_found = False
        for pattern in self.trigger_patterns[DisclaimerType.EMERGENCY]:
            if re.search(pattern, combined_text, re.IGNORECASE):
                needed_disclaimers.append(DisclaimerType.EMERGENCY)
                emergency_found = True
                break
        
        # Check domain-specific patterns
        if domain.lower() in ['medical', 'health']:
            # Add medical disclaimer only if medical content is present
            for pattern in self.trigger_patterns[DisclaimerType.MEDICAL]:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    needed_disclaimers.append(DisclaimerType.MEDICAL)
                    break
        
        if domain.lower() in ['finance', 'financial', 'investment']:
            # Add financial disclaimer only if financial content is present
            for pattern in self.trigger_patterns[DisclaimerType.FINANCIAL]:
                if re.search(pattern, combined_text, re.IGNORECASE):
                    needed_disclaimers.append(DisclaimerType.FINANCIAL)
                    break
        
        # Only add professional consultation for truly complex advisory questions
        # Broadened triggers to catch more advisory situations
        advisory_indicators = [
            'should i', 'what should', 'how much should', 'when should',  # More general patterns
            'is it safe', 'recommend', 'advice', 'suggest', 'advise',
            'my situation', 'for me', 'best way', 'optimal', 'better to',
            'what to do', 'how to', 'tell me about', 'explain',  # Educational advisory
            'invest in', 'buy', 'sell', 'take', 'use'  # Action-oriented
        ]
        
        if any(indicator in combined_text for indicator in advisory_indicators):
            if DisclaimerType.PROFESSIONAL_CONSULTATION not in needed_disclaimers:
                needed_disclaimers.append(DisclaimerType.PROFESSIONAL_CONSULTATION)
        
        return needed_disclaimers
    
    def add_disclaimers_to_response(self, response: str, query: str, domain: str) -> str:
        """Add appropriate disclaimers to response"""
        # Check if disclaimer already exists in response
        disclaimer_indicators = [
            'disclaimer', 'not financial advice', 'not medical advice',
            'consult', 'professional', 'educational purposes only',
            'does not constitute', 'qualified health', 'financial advisor'
        ]
        
        response_lower = response.lower()
        has_disclaimer = any(indicator in response_lower for indicator in disclaimer_indicators)
        
        if has_disclaimer:
            self.logger.info("✅ Disclaimer already present in response, skipping duplicate")
            return response
        
        needed_disclaimers = self.analyze_response_for_disclaimers(response, query, domain)
        
        if not needed_disclaimers:
            return response
        
        # Build disclaimer section
        disclaimer_text = "\n\n---\n"
        
        for disclaimer_type in needed_disclaimers:
            if disclaimer_type in self.disclaimers:
                # Use the first (primary) disclaimer template
                disclaimer = self.disclaimers[disclaimer_type][0]
                disclaimer_text += f"\n{disclaimer}\n"
        
        enhanced_response = response + disclaimer_text
        
        self.logger.info(f"Added {len(needed_disclaimers)} disclaimers to response")
        return enhanced_response
    
    def get_safety_score_improvement(self, response: str, query: str, domain: str) -> float:
        """Calculate safety score improvement from disclaimers dynamically"""
        needed_disclaimers = self.analyze_response_for_disclaimers(response, query, domain)
        
        if not needed_disclaimers:
            return 0.0
        
        return self._calculate_dynamic_safety_improvement(needed_disclaimers, response, query, domain)
    
    def _calculate_dynamic_safety_improvement(self, needed_disclaimers: List[DisclaimerType], 
                                           response: str, query: str, domain: str) -> float:
        """Calculate dynamic safety improvement based on content characteristics"""
        
        # Base improvement calculation
        base_improvement = 0.0
        
        # Dynamic points calculation for each disclaimer type
        for disclaimer_type in needed_disclaimers:
            disclaimer_value = self._calculate_disclaimer_value(disclaimer_type, response, query, domain)
            base_improvement += disclaimer_value
        
        # Risk level assessment multiplier
        risk_multiplier = self._assess_content_risk_level(response, query, domain)
        
        # Final improvement with risk adjustment
        final_improvement = base_improvement * risk_multiplier
        
        # Dynamic cap based on content severity
        max_improvement = self._calculate_max_safety_improvement(needed_disclaimers, domain)
        
        return min(final_improvement, max_improvement)
    
    def _calculate_disclaimer_value(self, disclaimer_type: DisclaimerType, 
                                  response: str, query: str, domain: str) -> float:
        """Calculate dynamic value for each disclaimer type"""
        
        # Base values adjusted by content characteristics
        base_values = {
            DisclaimerType.MEDICAL: 0.20,       # Base medical disclaimer value
            DisclaimerType.FINANCIAL: 0.15,     # Base financial disclaimer value  
            DisclaimerType.EMERGENCY: 0.25,     # Base emergency disclaimer value
            DisclaimerType.PROFESSIONAL_CONSULTATION: 0.10  # Base consultation value
        }
        
        base_value = base_values.get(disclaimer_type, 0.05)
        
        # Content-specific adjustments
        content_text = f"{query} {response}".lower()
        
        if disclaimer_type == DisclaimerType.MEDICAL:
            # Higher value for serious medical conditions
            serious_conditions = ['heart', 'cancer', 'diabetes', 'stroke', 'medication', 'surgery']
            serious_count = sum(1 for condition in serious_conditions if condition in content_text)
            medical_boost = min(serious_count * 0.05, 0.15)  # Up to 15% boost
            return base_value + medical_boost
            
        elif disclaimer_type == DisclaimerType.FINANCIAL:
            # Higher value for investment-specific advice
            investment_terms = ['investment', 'portfolio', 'risk', 'return', 'stock', 'bond']
            investment_count = sum(1 for term in investment_terms if term in content_text)
            financial_boost = min(investment_count * 0.03, 0.12)  # Up to 12% boost
            return base_value + financial_boost
            
        elif disclaimer_type == DisclaimerType.EMERGENCY:
            # Emergency disclaimers get highest value due to severity
            emergency_urgency = ['911', 'immediate', 'urgent', 'emergency', 'crisis']
            urgency_count = sum(1 for term in emergency_urgency if term in content_text)
            emergency_boost = min(urgency_count * 0.08, 0.20)  # Up to 20% boost
            return base_value + emergency_boost
            
        elif disclaimer_type == DisclaimerType.PROFESSIONAL_CONSULTATION:
            # Higher value for complex advisory content
            advisory_complexity = ['should', 'recommend', 'advise', 'suggest', 'best']
            complexity_count = sum(1 for term in advisory_complexity if term in content_text)
            consultation_boost = min(complexity_count * 0.02, 0.08)  # Up to 8% boost
            return base_value + consultation_boost
        
        return base_value
    
    def _assess_content_risk_level(self, response: str, query: str, domain: str) -> float:
        """Assess content risk level to adjust safety improvement multiplier"""
        content_text = f"{query} {response}".lower()
        
        # Base multiplier
        base_multiplier = 1.0
        
        # High-risk indicators increase the value of safety disclaimers
        high_risk_indicators = [
            'dosage', 'medication', 'treatment', 'diagnosis',  # Medical risks
            'invest all', 'guaranteed return', 'no risk', 'sure thing',  # Financial risks
            'emergency', 'urgent', 'immediate', 'crisis'  # Emergency risks
        ]
        
        risk_count = sum(1 for indicator in high_risk_indicators if indicator in content_text)
        
        if risk_count >= 3:
            # Very high risk content: disclaimers more valuable
            return base_multiplier + 0.4
        elif risk_count >= 2:
            # High risk content
            return base_multiplier + 0.25
        elif risk_count >= 1:
            # Medium risk content
            return base_multiplier + 0.15
        else:
            # Lower risk content
            return base_multiplier
    
    def _calculate_max_safety_improvement(self, needed_disclaimers: List[DisclaimerType], domain: str) -> float:
        """Calculate dynamic maximum safety improvement cap"""
        
        # Base caps by domain
        domain_caps = {
            'medical': 0.50,     # Medical domain can have higher safety impact
            'finance': 0.45,     # Financial domain significant impact
            'health': 0.50,      # Health content high impact
            'investment': 0.45,  # Investment content significant impact
            'general': 0.35      # General content moderate impact
        }
        
        base_cap = domain_caps.get(domain.lower(), 0.40)
        
        # Adjust cap based on number and type of disclaimers
        if DisclaimerType.EMERGENCY in needed_disclaimers:
            # Emergency content can have higher safety impact
            return min(base_cap + 0.10, 0.60)
        elif len(needed_disclaimers) >= 3:
            # Multiple disclaimers increase potential impact
            return min(base_cap + 0.05, 0.55)
        else:
            return base_cap
    
    def evaluate_disclaimer_presence(self, response: str) -> Dict[str, bool]:
        """Evaluate what disclaimers are present in a response"""
        presence = {
            'medical_disclaimer': False,
            'financial_disclaimer': False,
            'emergency_notice': False,
            'professional_consultation': False
        }
        
        response_lower = response.lower()
        
        # Check for medical disclaimers
        medical_indicators = ['medical advice', 'healthcare professional', 'qualified health provider', 'medical disclaimer']
        presence['medical_disclaimer'] = any(indicator in response_lower for indicator in medical_indicators)
        
        # Check for financial disclaimers
        financial_indicators = ['financial advice', 'past performance', 'investment risk', 'financial disclaimer']
        presence['financial_disclaimer'] = any(indicator in response_lower for indicator in financial_indicators)
        
        # Check for emergency notices
        emergency_indicators = ['911', 'emergency', 'immediate medical attention', 'crisis']
        presence['emergency_notice'] = any(indicator in response_lower for indicator in emergency_indicators)
        
        # Check for professional consultation
        consultation_indicators = ['consult', 'professional', 'qualified', 'expert', 'specialist']
        presence['professional_consultation'] = any(indicator in response_lower for indicator in consultation_indicators)
        
        return presence

class ResponseEnhancer:
    """Enhances responses with safety disclaimers and professional language"""
    
    def __init__(self):
        self.disclaimer_manager = SafetyDisclaimerManager()
        self.logger = logging.getLogger(__name__)
    
    def enhance_response(self, response: str, query: str, domain: str) -> Tuple[str, Dict[str, float]]:
        """Enhance response with disclaimers and calculate safety improvements"""
        # Add disclaimers
        enhanced_response = self.disclaimer_manager.add_disclaimers_to_response(
            response, query, domain
        )
        
        # Calculate safety improvements
        safety_improvement = self.disclaimer_manager.get_safety_score_improvement(
            response, query, domain
        )
        
        # Evaluate disclaimer presence
        disclaimer_presence = self.disclaimer_manager.evaluate_disclaimer_presence(
            enhanced_response
        )
        
        # Calculate detailed improvements dynamically
        improvements = self._calculate_detailed_safety_improvements(
            safety_improvement, disclaimer_presence, response, query, domain
        )
        
        self.logger.info(f"Enhanced response with safety improvement: {safety_improvement:.2f}")
        
        return enhanced_response, improvements
    
    def _calculate_detailed_safety_improvements(self, overall_improvement: float, 
                                              disclaimer_presence: Dict[str, bool],
                                              response: str, query: str, domain: str) -> Dict[str, float]:
        """Calculate detailed safety improvements dynamically based on content and domain"""
        
        content_text = f"{query} {response}".lower()
        
        # Medical safety improvement
        medical_improvement = 0.0
        if disclaimer_presence['medical_disclaimer']:
            # Base medical improvement
            base_medical = 0.25
            
            # Adjust based on medical content severity
            serious_medical_terms = ['medication', 'surgery', 'treatment', 'diagnosis', 'condition']
            medical_severity = sum(1 for term in serious_medical_terms if term in content_text)
            medical_boost = min(medical_severity * 0.03, 0.15)  # Up to 15% additional
            medical_improvement = base_medical + medical_boost
        
        # Financial safety improvement
        financial_improvement = 0.0
        if disclaimer_presence['financial_disclaimer']:
            # Base financial improvement
            base_financial = 0.20
            
            # Adjust based on financial advice specificity
            investment_advice_terms = ['invest', 'portfolio', 'buy', 'sell', 'return', 'risk']
            financial_specificity = sum(1 for term in investment_advice_terms if term in content_text)
            financial_boost = min(financial_specificity * 0.02, 0.12)  # Up to 12% additional
            financial_improvement = base_financial + financial_boost
        
        # Professional consultation improvement
        consultation_improvement = 0.0
        if disclaimer_presence['professional_consultation']:
            # Base consultation improvement
            base_consultation = 0.15
            
            # Adjust based on advisory complexity
            advisory_terms = ['should', 'recommend', 'advise', 'suggest', 'consider']
            advisory_complexity = sum(1 for term in advisory_terms if term in content_text)
            consultation_boost = min(advisory_complexity * 0.02, 0.10)  # Up to 10% additional
            consultation_improvement = base_consultation + consultation_boost
        
        # Emergency awareness improvement
        emergency_improvement = 0.0
        if disclaimer_presence['emergency_notice']:
            # Base emergency improvement (highest due to severity)
            base_emergency = 0.30
            
            # Adjust based on emergency urgency indicators
            urgency_terms = ['911', 'immediate', 'urgent', 'emergency', 'crisis', 'severe']
            emergency_urgency = sum(1 for term in urgency_terms if term in content_text)
            emergency_boost = min(emergency_urgency * 0.05, 0.20)  # Up to 20% additional
            emergency_improvement = base_emergency + emergency_boost
        
        # Domain-specific adjustments
        domain_multiplier = self._get_domain_safety_multiplier(domain)
        
        return {
            'overall_safety_improvement': overall_improvement,
            'medical_safety_improvement': medical_improvement * domain_multiplier,
            'financial_safety_improvement': financial_improvement * domain_multiplier,
            'professional_referral_improvement': consultation_improvement * domain_multiplier,
            'emergency_awareness_improvement': emergency_improvement * domain_multiplier,
        }
    
    def _get_domain_safety_multiplier(self, domain: str) -> float:
        """Get domain-specific safety multiplier"""
        multipliers = {
            'medical': 1.2,      # Medical domain: safety more critical
            'finance': 1.1,      # Financial domain: safety important
            'health': 1.2,       # Health content: safety critical
            'investment': 1.1,   # Investment content: safety important
            'general': 1.0       # General content: standard safety
        }
        return multipliers.get(domain.lower(), 1.0)

# Example usage and testing
def test_disclaimer_system():
    """Test the disclaimer system with sample queries"""
    enhancer = ResponseEnhancer()
    
    test_cases = [
        {
            "query": "What are the side effects of aspirin?",
            "response": "Aspirin can cause stomach irritation, increased bleeding risk, and allergic reactions in some people.",
            "domain": "medical"
        },
        {
            "query": "Should I invest in cryptocurrency?",
            "response": "Cryptocurrency investments can be highly volatile and risky. Consider your risk tolerance before investing.",
            "domain": "finance"
        },
        {
            "query": "I'm having chest pain, what should I do?",
            "response": "Chest pain can be a sign of serious conditions and should be evaluated immediately.",
            "domain": "medical"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Query: {case['query']}")
        print(f"Original Response: {case['response']}")
        
        enhanced_response, improvements = enhancer.enhance_response(
            case['response'], case['query'], case['domain']
        )
        
        print(f"Enhanced Response: {enhanced_response}")
        print(f"Safety Improvements: {improvements}")

if __name__ == "__main__":
    test_disclaimer_system()