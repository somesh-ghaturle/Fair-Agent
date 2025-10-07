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
        """Calculate safety score improvement from disclaimers"""
        needed_disclaimers = self.analyze_response_for_disclaimers(response, query, domain)
        
        # Base improvement
        base_improvement = 0.0
        
        # Points for each disclaimer type
        disclaimer_points = {
            DisclaimerType.MEDICAL: 0.25,
            DisclaimerType.FINANCIAL: 0.20,
            DisclaimerType.EMERGENCY: 0.30,
            DisclaimerType.PROFESSIONAL_CONSULTATION: 0.15
        }
        
        for disclaimer_type in needed_disclaimers:
            base_improvement += disclaimer_points.get(disclaimer_type, 0.10)
        
        # Cap at reasonable improvement level
        return min(base_improvement, 0.40)  # Max 40% improvement
    
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
        
        # Calculate detailed improvements
        improvements = {
            'overall_safety_improvement': safety_improvement,
            'medical_safety_improvement': 0.30 if disclaimer_presence['medical_disclaimer'] else 0.0,
            'financial_safety_improvement': 0.25 if disclaimer_presence['financial_disclaimer'] else 0.0,
            'professional_referral_improvement': 0.20 if disclaimer_presence['professional_consultation'] else 0.0,
            'emergency_awareness_improvement': 0.35 if disclaimer_presence['emergency_notice'] else 0.0,
        }
        
        self.logger.info(f"Enhanced response with safety improvement: {safety_improvement:.2f}")
        
        return enhanced_response, improvements

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