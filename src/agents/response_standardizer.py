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

**Transparency Score:** {transparency_score}%
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
        
        # Calculate transparency score (based on evidence and reasoning)
        transparency = 50.0  # Base
        if evidence_sources: transparency += 20.0
        if components.get('reasoning'): transparency += 20.0
        if confidence > 0.7: transparency += 10.0
        
        # Build standardized response
        standardized = cls.STANDARD_TEMPLATE.format(
            executive_summary=components.get('summary', 'Analysis of your financial question.').strip(),
            detailed_analysis=components.get('analysis', raw_response[:500]).strip(),
            evidence_sources=evidence_text.strip(),
            reasoning_steps=reasoning_text.strip(),
            key_takeaways=takeaways_text.strip(),
            disclaimer=cls.FINANCE_DISCLAIMER.strip(),
            confidence_score=round(confidence * 10, 1),
            transparency_score=min(round(transparency, 1), 100.0)
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
        
        # Calculate transparency score (based on evidence and reasoning)
        transparency = 50.0  # Base
        if evidence_sources: transparency += 20.0
        if components.get('reasoning'): transparency += 20.0
        if confidence > 0.7: transparency += 10.0
        
        # Build standardized response
        standardized = cls.STANDARD_TEMPLATE.format(
            executive_summary=components.get('summary', 'Analysis of your health question.').strip(),
            detailed_analysis=components.get('analysis', raw_response[:500]).strip(),
            evidence_sources=evidence_text.strip(),
            reasoning_steps=reasoning_text.strip(),
            key_takeaways=takeaways_text.strip(),
            disclaimer=cls.MEDICAL_DISCLAIMER.strip(),
            confidence_score=round(confidence * 10, 1),
            transparency_score=min(round(transparency, 1), 100.0)
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
        
        # Check if response follows the "Step" format (Structured)
        step_pattern = r'\*\*Step\s+(\d+):\s*([^*]+)\*\*\s*\n(.*?)(?=\n\*\*Step|\Z)'
        steps_found = re.findall(step_pattern, response, re.DOTALL)
        
        if steps_found:
            # We have a structured response!
            step_dict = {int(s[0]): (s[1].strip(), s[2].strip()) for s in steps_found}
            
            # 1. Summary: Use Step 1 (Understanding) content
            if 1 in step_dict:
                components['summary'] = step_dict[1][1]
            else:
                components['summary'] = response[:200] + '...'
            
            # 2. Analysis: Use Step 2 (Evidence) and Step 3 (Analysis)
            analysis_parts = []
            if 2 in step_dict:
                analysis_parts.append(f"**{step_dict[2][0]}**\n{step_dict[2][1]}")
            if 3 in step_dict:
                analysis_parts.append(f"**{step_dict[3][0]}**\n{step_dict[3][1]}")
            
            if analysis_parts:
                components['analysis'] = '\n\n'.join(analysis_parts)
            else:
                components['analysis'] = response
            
            # 3. Reasoning: Extract titles of the steps as the reasoning flow
            components['reasoning'] = [f"{title}" for num, (title, content) in step_dict.items()]
            
            # 4. Main Points: Extract from Step 4 (Conclusion) or Step 5/6
            # Look for conclusion/recommendation steps
            conclusion_step = None
            for step_num in [4, 5, 6]:
                if step_num in step_dict:
                    conclusion_step = step_dict[step_num][1]
                    break
            
            if conclusion_step:
                # Split conclusion into sentences or bullets
                # Check for bullets first
                bullets = re.findall(r'(?:^|\n)[-•*]\s*([^\n]+)', conclusion_step)
                if bullets:
                    components['main_points'] = bullets
                else:
                    # Split by sentences
                    components['main_points'] = [s.strip() for s in re.split(r'(?<=[.!?])\s+', conclusion_step) if len(s.strip()) > 10]
            
            return components

        # Fallback for Unstructured Response
        
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
        
        # Extract reasoning steps (look for Step 1, Step 2, etc. in unstructured text)
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
        # Improved regex to avoid matching headers like **Step 1** as bullets
        bullet_pattern = r'(?:^|\n)(?<!\*)([-•*])\s+([^\n]+)'
        bullets = re.findall(bullet_pattern, response)
        if bullets:
            components['main_points'] = [b[1].strip() for b in bullets[:5]]
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
            
        # If summary is too short, try to improve it
        if len(components['summary']) < 50 and len(components['analysis']) > 100:
             components['summary'] = components['analysis'][:200] + "..."
        
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
            
            # Format reliability as percentage
            if isinstance(reliability, (int, float)):
                rel_str = f"{reliability:.0%}" if reliability <= 1.0 else f"{reliability}%"
            else:
                rel_str = str(reliability)

            source_text = f"**{i}. {title}**\n\n"
            source_text += f"- **Type:** {source_type}\n"
            source_text += f"- **Reliability:** {rel_str}\n"
            if pub_date and pub_date != 'N/A':
                source_text += f"- **Published:** {pub_date}\n"
            if url:
                source_text += f"- **Link:** [{url}]({url})\n"
            
            formatted.append(source_text)
            
        return "\n".join(formatted)
    
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
            # Remove existing bullets to ensure consistency
            clean_point = clean_point.lstrip('-•* ').strip()
            if clean_point:
                formatted.append(f"- {clean_point}")
        
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
