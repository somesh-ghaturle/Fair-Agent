"""
Response Standardization Module for FAIR-Agent
Ensures all responses follow a consistent, professional format
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass


@dataclass
class StandardizedResponse:
    """Standardized response structure"""
    executive_summary: str
    detailed_analysis: str
    evidence_sources: List[Dict]
    reasoning_steps: List[str]
    key_takeaways: List[str]
    disclaimer: str
    confidence_score: float
    

class ResponseStandardizer:
    """
    Ensures all FAIR-Agent responses follow a consistent, professional format
    regardless of domain (finance, medical, etc.)
    """
    
    # Standard response template
    STANDARD_TEMPLATE = """
## 📋 Executive Summary

{executive_summary}

---

## 🔍 Detailed Analysis

{detailed_analysis}

---

## 📚 Evidence Sources

{evidence_sources}

---

## 💡 Chain of Thought Reasoning

{reasoning_steps}

---

## ✅ Key Takeaways

{key_takeaways}

---

{disclaimer}

---

**Confidence Level:** {confidence_score}/10
"""

    FINANCE_DISCLAIMER = """
## ⚠️ Financial Disclaimer

**This information is for educational purposes only and does not constitute financial advice.**

Key Points:
- Individual financial situations vary significantly
- Consult a licensed financial advisor before making investment decisions
- Past performance does not guarantee future results
- All investments carry risk, including potential loss of principal
- Tax implications vary by jurisdiction and personal circumstances

**Professional consultation is strongly recommended for all financial decisions.**
"""

    MEDICAL_DISCLAIMER = """
## ⚠️ Medical Disclaimer

**This information is for educational purposes only and does not constitute medical advice.**

Critical Points:
- This is NOT a substitute for professional medical advice, diagnosis, or treatment
- Always consult qualified healthcare providers for medical decisions
- Emergency situations require immediate medical attention (call 911)
- Individual health conditions vary significantly
- Treatment outcomes depend on many personal factors

**Never delay or disregard professional medical advice based on information provided here.**
"""

    @staticmethod
    def extract_confidence_from_response(response: str) -> float:
        """Extract confidence score from response text
        
        Args:
            response: The response text to extract confidence from
            
        Returns:
            float: Confidence score between 0 and 1 (defaults to 0.7)
        """
        import re
        
        # Look for patterns like "Confidence: 8/10", "Confidence Level: 7/10", etc.
        patterns = [
            r'confidence[:\s]+(\d+(?:\.\d+)?)/10',
            r'confidence[:\s]+(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)/10\s*confidence',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                score = float(match.group(1))
                # Normalize to 0-1 range if needed
                if score > 1:
                    score = score / 10
                return min(max(score, 0.0), 1.0)  # Clamp between 0 and 1
        
        # Default confidence if not found
        return 0.7

    @classmethod
    def standardize_finance_response(
        cls,
        raw_response: str,
        evidence_sources: List = None,
        confidence: float = 0.0,
        question: str = ""
    ) -> str:
        """
        Standardize a finance response to follow the template
        
        Args:
            raw_response: Raw LLM-generated response
            evidence_sources: List of evidence source objects
            confidence: Confidence score (0-1)
            question: Original user question
            
        Returns:
            Standardized formatted response
        """
        # Parse the raw response into components
        components = cls._parse_response_components(raw_response, question)
        
        # Format evidence sources
        evidence_text = cls._format_evidence_sources(evidence_sources or [])
        
        # Format reasoning steps
        reasoning_text = cls._format_reasoning_steps(components.get('reasoning', []))
        
        # Format key takeaways
        takeaways_text = cls._format_key_takeaways(components.get('main_points', []))
        
        # Build standardized response
        standardized = cls.STANDARD_TEMPLATE.format(
            executive_summary=components.get('summary', 'Analysis of your financial question.'),
            detailed_analysis=components.get('analysis', raw_response[:500]),
            evidence_sources=evidence_text,
            reasoning_steps=reasoning_text,
            key_takeaways=takeaways_text,
            disclaimer=cls.FINANCE_DISCLAIMER,
            confidence_score=round(confidence * 10, 1)
        )
        
        return standardized.strip()
    
    @classmethod
    def standardize_medical_response(
        cls,
        raw_response: str,
        evidence_sources: List = None,
        confidence: float = 0.0,
        question: str = ""
    ) -> str:
        """
        Standardize a medical response to follow the template
        
        Args:
            raw_response: Raw LLM-generated response
            evidence_sources: List of evidence source objects
            confidence: Confidence score (0-1)
            question: Original user question
            
        Returns:
            Standardized formatted response
        """
        # Parse the raw response into components
        components = cls._parse_response_components(raw_response, question)
        
        # Format evidence sources
        evidence_text = cls._format_evidence_sources(evidence_sources or [])
        
        # Format reasoning steps
        reasoning_text = cls._format_reasoning_steps(components.get('reasoning', []))
        
        # Format key takeaways
        takeaways_text = cls._format_key_takeaways(components.get('main_points', []))
        
        # Build standardized response
        standardized = cls.STANDARD_TEMPLATE.format(
            executive_summary=components.get('summary', 'Analysis of your health question.'),
            detailed_analysis=components.get('analysis', raw_response[:500]),
            evidence_sources=evidence_text,
            reasoning_steps=reasoning_text,
            key_takeaways=takeaways_text,
            disclaimer=cls.MEDICAL_DISCLAIMER,
            confidence_score=round(confidence * 10, 1)
        )
        
        return standardized.strip()
    
    @classmethod
    def _parse_response_components(cls, response: str, question: str) -> Dict:
        """
        Parse raw response into structured components
        
        Returns:
            Dict with keys: summary, analysis, reasoning, main_points
        """
        components = {
            'summary': '',
            'analysis': '',
            'reasoning': [],
            'main_points': []
        }
        
        # Try to extract executive summary (first paragraph or first 2 sentences)
        paragraphs = [p.strip() for p in response.split('\n\n') if p.strip()]
        if paragraphs:
            first_para = paragraphs[0]
            # Get first 2 sentences as summary
            sentences = re.split(r'(?<=[.!?])\s+', first_para)
            components['summary'] = ' '.join(sentences[:2]) if len(sentences) >= 2 else first_para
            
            # Rest is detailed analysis
            components['analysis'] = '\n\n'.join(paragraphs)
        else:
            components['summary'] = response[:200] + '...' if len(response) > 200 else response
            components['analysis'] = response
        
        # Extract reasoning steps (look for Step 1, Step 2, etc.)
        step_pattern = r'(?:Step\s+\d+|First|Second|Third|Next|Then|Finally)[:\s]([^.\n]+[.])'
        steps = re.findall(step_pattern, response, re.IGNORECASE)
        if steps:
            components['reasoning'] = [s.strip() for s in steps[:5]]  # Max 5 steps
        else:
            # Create reasoning steps from paragraphs
            if len(paragraphs) > 1:
                components['reasoning'] = [
                    f"Analyzed the question: {question[:100]}...",
                    f"Retrieved relevant evidence from trusted sources",
                    f"Synthesized information to provide accurate answer",
                    f"Applied domain expertise and best practices"
                ]
        
        # Extract main points (bullet points or key statements)
        bullet_pattern = r'(?:^|\n)[-•*]\s*([^\n]+)'
        bullets = re.findall(bullet_pattern, response)
        if bullets:
            components['main_points'] = [b.strip() for b in bullets[:5]]
        else:
            # Create main points from key sentences
            sentences = re.split(r'(?<=[.!?])\s+', response)
            # Pick sentences with important keywords
            important = []
            keywords = ['important', 'key', 'essential', 'should', 'must', 'recommend', 'consider']
            for sent in sentences:
                if any(kw in sent.lower() for kw in keywords):
                    important.append(sent.strip())
                    if len(important) >= 3:
                        break
            components['main_points'] = important or sentences[:3]
        
        return components
    
    @classmethod
    def _format_evidence_sources(cls, sources: List) -> str:
        """Format evidence sources into consistent structure"""
        if not sources:
            return "No specific evidence sources were retrieved for this query."
        
        formatted = []
        for i, source in enumerate(sources[:5], 1):  # Max 5 sources
            # Handle both dict and object sources
            if isinstance(source, dict):
                title = source.get('title', f'Source {i}')
                source_type = source.get('source_type', source.get('type', 'Unknown'))
                # Try both 'reliability' and 'reliability_score'
                reliability = source.get('reliability_score', source.get('reliability', 0.0))
                url = source.get('url', '')
                pub_date = source.get('publication_date', 'N/A')
            else:
                title = getattr(source, 'title', f'Source {i}')
                source_type = getattr(source, 'source_type', 'Unknown')
                reliability = getattr(source, 'reliability_score', 0.0)
                url = getattr(source, 'url', '')
                pub_date = getattr(source, 'publication_date', 'N/A')
            
            source_block = f"""**{i}. {title}**
- Type: {source_type.replace('_', ' ').title()}
- Reliability: {reliability:.0%}
- Published: {pub_date}"""
            
            if url:
                source_block += f"\n- Link: [{url}]({url})"
            
            formatted.append(source_block)
        
        return '\n\n'.join(formatted)
    
    @classmethod
    def _format_reasoning_steps(cls, steps: List[str]) -> str:
        """Format reasoning steps into numbered list"""
        if not steps:
            return "1. Analyzed the user's question\n2. Retrieved relevant evidence\n3. Synthesized information\n4. Formulated evidence-based response"
        
        formatted = []
        for i, step in enumerate(steps, 1):
            formatted.append(f"{i}. {step.strip()}")
        
        return '\n'.join(formatted)
    
    @classmethod
    def _format_key_takeaways(cls, points: List[str]) -> str:
        """Format key takeaways as bullet points"""
        if not points:
            return "- Review the detailed analysis above\n- Consult with qualified professionals\n- Consider your individual circumstances"
        
        formatted = []
        for point in points[:5]:  # Max 5 takeaways
            # Clean up the point
            clean_point = point.strip()
            if clean_point and not clean_point.startswith('-') and not clean_point.startswith('•'):
                formatted.append(f"- {clean_point}")
            else:
                formatted.append(clean_point)
        
        return '\n'.join(formatted)
    
    @classmethod
    def extract_confidence_from_response(cls, response: str) -> float:
        """
        Extract confidence score from response text if present
        
        Returns:
            Float between 0 and 1, or 0.7 as default
        """
        # Look for patterns like "Confidence: 85%" or "Confidence Score: 0.85"
        patterns = [
            r'confidence[:\s]+(\d+(?:\.\d+)?)\s*%',
            r'confidence[:\s]+(\d+(?:\.\d+)?)/10',
            r'confidence[:\s]+(\d+(?:\.\d+)?)/100',
            r'confidence score[:\s]+(\d+(?:\.\d+)?)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response, re.IGNORECASE)
            if match:
                value = float(match.group(1))
                # Normalize to 0-1 range
                if value > 1:
                    value = value / 100 if value <= 100 else value / 10
                return min(max(value, 0), 1)
        
        # Default confidence
        return 0.7
