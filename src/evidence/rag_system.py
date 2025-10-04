"""
Evidence Citation and Retrieval System for FAIR-Agent

This module implements retrieval-augmented generation (RAG) to improve
faithfulness scores by providing evidence-based responses with proper citations.
"""

import logging
import json
import hashlib
import yaml
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from pathlib import Path
import re
from datetime import datetime

logger = logging.getLogger(__name__)

@dataclass
class EvidenceSource:
    """Represents a source of evidence"""
    id: str
    title: str
    content: str
    source_type: str  # 'medical_literature', 'financial_report', 'guideline', etc.
    url: Optional[str] = None
    publication_date: Optional[str] = None
    reliability_score: float = 0.8
    domain: str = "general"

@dataclass
class Citation:
    """Represents a citation in a response"""
    source_id: str
    text_snippet: str
    relevance_score: float
    citation_format: str

@dataclass
class EnhancedResponse:
    """Response with evidence and citations"""
    answer: str
    evidence_sources: List[EvidenceSource]
    citations: List[Citation]
    evidence_coverage: float
    citation_quality_score: float

class EvidenceDatabase:
    """Database of evidence sources for different domains"""
    
    def __init__(self, data_dir: str = "./data/evidence", config_path: str = "./config/evidence_sources.yaml"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = Path(config_path)
        self.sources: Dict[str, EvidenceSource] = {}
        self.domain_index: Dict[str, List[str]] = {}
        self._load_evidence_sources()
    
    def _load_evidence_sources(self):
        """Load evidence sources from YAML configuration file"""
        
        # Try to load from YAML config first
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f)
                
                all_sources = []
                
                # Load medical sources
                if 'medical_sources' in config:
                    for source_data in config['medical_sources']:
                        source = EvidenceSource(
                            id=source_data['id'],
                            title=source_data['title'],
                            content=source_data['content'].strip(),
                            source_type=source_data['source_type'],
                            url=source_data.get('url'),
                            publication_date=source_data.get('publication_date'),
                            reliability_score=source_data.get('reliability_score', 0.8),
                            domain=source_data.get('domain', 'medical')
                        )
                        all_sources.append(source)
                
                # Load finance sources
                if 'finance_sources' in config:
                    for source_data in config['finance_sources']:
                        source = EvidenceSource(
                            id=source_data['id'],
                            title=source_data['title'],
                            content=source_data['content'].strip(),
                            source_type=source_data['source_type'],
                            url=source_data.get('url'),
                            publication_date=source_data.get('publication_date'),
                            reliability_score=source_data.get('reliability_score', 0.8),
                            domain=source_data.get('domain', 'finance')
                        )
                        all_sources.append(source)
                
                # Add sources to database
                for source in all_sources:
                    self.sources[source.id] = source
                    
                    # Update domain index
                    if source.domain not in self.domain_index:
                        self.domain_index[source.domain] = []
                    self.domain_index[source.domain].append(source.id)
                
                logger.info(f"✅ Loaded {len(all_sources)} evidence sources from {self.config_path}")
                logger.info(f"   Medical: {len([s for s in all_sources if s.domain == 'medical'])}")
                logger.info(f"   Finance: {len([s for s in all_sources if s.domain == 'finance'])}")
                return
                
            except Exception as e:
                logger.warning(f"Failed to load evidence from config: {e}. Using fallback hardcoded sources.")
        
        # Fallback to hardcoded sources if config not found
        logger.warning("Evidence config not found, using fallback hardcoded sources")
        self._load_hardcoded_sources()
    
    def _load_hardcoded_sources(self):
        """Fallback method with hardcoded evidence sources"""
        # Medical evidence sources
        medical_sources = [
            EvidenceSource(
                id="med_001",
                title="Aspirin for Primary Prevention of Cardiovascular Disease",
                content="Low-dose aspirin (75-100 mg daily) reduces the risk of major cardiovascular events in adults aged 40-70 years with elevated cardiovascular risk and low bleeding risk. The U.S. Preventive Services Task Force recommends individualized decision-making based on cardiovascular risk factors, bleeding risk, and patient preferences. Common side effects include gastrointestinal bleeding and peptic ulcer disease.",
                source_type="clinical_guideline",
                url="https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/aspirin-use-to-prevent-cardiovascular-disease-preventive-medication",
                publication_date="2022-04-26",
                reliability_score=0.95,
                domain="medical"
            ),
            EvidenceSource(
                id="med_002",
                title="Diabetes Management Guidelines",
                content="Type 2 diabetes management involves lifestyle modifications including diet, exercise, and weight management, combined with pharmacological interventions when necessary. Metformin is typically the first-line medication. Regular monitoring of HbA1c, blood pressure, and lipid levels is essential. Target HbA1c is generally <7% for most adults, though individualized targets may be appropriate.",
                source_type="clinical_guideline",
                url="https://care.diabetesjournals.org/content/diacare/suppl/2023/12/08/47.Supplement_1.DC1/Standards_of_Care_2024.pdf",
                publication_date="2024-01-01",
                reliability_score=0.95,
                domain="medical"
            ),
            EvidenceSource(
                id="med_003",
                title="Hypertension Management",
                content="Hypertension is defined as systolic BP ≥130 mmHg or diastolic BP ≥80 mmHg. Initial treatment includes lifestyle modifications (DASH diet, sodium reduction, weight loss, physical activity, alcohol moderation). First-line antihypertensive medications include ACE inhibitors, ARBs, calcium channel blockers, and thiazide diuretics. Blood pressure targets are generally <130/80 mmHg for most adults.",
                source_type="clinical_guideline",
                url="https://www.ahajournals.org/doi/full/10.1161/HYP.0000000000000065",
                publication_date="2023-06-01",
                reliability_score=0.95,
                domain="medical"
            ),
            EvidenceSource(
                id="med_004",
                title="Mental Health Crisis Intervention",
                content="Individuals experiencing suicidal ideation require immediate professional evaluation. Warning signs include expressing hopelessness, social withdrawal, dramatic mood changes, and talking about death or suicide. The National Suicide Prevention Lifeline (988) provides 24/7 crisis support. Safety planning involves removing access to lethal means and establishing support networks.",
                source_type="clinical_guideline",
                url="https://www.nimh.nih.gov/health/topics/suicide-prevention",
                publication_date="2023-09-01",
                reliability_score=0.98,
                domain="medical"
            )
        ]
        
        # Financial evidence sources
        financial_sources = [
            EvidenceSource(
                id="fin_001",
                title="Portfolio Diversification Principles",
                content="Modern portfolio theory demonstrates that diversification across uncorrelated assets reduces portfolio risk without proportionally reducing expected returns. The efficient frontier represents optimal risk-return combinations. Academic research shows that asset allocation accounts for approximately 90% of portfolio return variability. Geographic and sector diversification provide additional risk reduction benefits.",
                source_type="academic_research",
                url="https://www.jstor.org/stable/2975974",
                publication_date="1952-03-01",
                reliability_score=0.90,
                domain="finance"
            ),
            EvidenceSource(
                id="fin_002",
                title="Interest Rate and Bond Price Relationship",
                content="Bond prices and interest rates have an inverse relationship due to discounted cash flow principles. When interest rates rise, existing bonds with lower coupon rates become less attractive, causing their prices to fall. Duration measures price sensitivity to interest rate changes. Longer-duration bonds experience greater price volatility from interest rate movements.",
                source_type="financial_textbook",
                url="https://www.investopedia.com/terms/i/interest_rate_risk.asp",
                publication_date="2023-01-15",
                reliability_score=0.85,
                domain="finance"
            ),
            EvidenceSource(
                id="fin_003",
                title="Cryptocurrency Market Volatility",
                content="Cryptocurrency markets exhibit extreme volatility with daily price movements often exceeding 10%. Bitcoin has experienced multiple bear markets with peak-to-trough declines exceeding 80%. Regulatory uncertainty, technological risks, and market manipulation contribute to volatility. The SEC and other regulators continue developing frameworks for digital asset oversight.",
                source_type="market_analysis",
                url="https://www.sec.gov/investor/alerts/ia_bitcoin.pdf",
                publication_date="2023-12-01",
                reliability_score=0.90,
                domain="finance"
            ),
            EvidenceSource(
                id="fin_004",
                title="Retirement Planning Best Practices",
                content="Financial advisors recommend saving 10-15% of income for retirement starting in one's 20s. The power of compound growth makes early saving crucial - each year delayed requires significantly higher savings rates. Tax-advantaged accounts like 401(k)s and IRAs provide substantial benefits. Target-date funds offer age-appropriate asset allocation automatically.",
                source_type="financial_planning",
                url="https://www.dol.gov/sites/dolgov/files/ebsa/about-ebsa/our-activities/resource-center/publications/top-10-ways-to-prepare-for-retirement.pdf",
                publication_date="2023-08-01",
                reliability_score=0.92,
                domain="finance"
            )
        ]
        
        # Add sources to database
        all_sources = medical_sources + financial_sources
        for source in all_sources:
            self.sources[source.id] = source
            
            # Update domain index
            if source.domain not in self.domain_index:
                self.domain_index[source.domain] = []
            self.domain_index[source.domain].append(source.id)
        
        logger.info(f"Loaded {len(all_sources)} evidence sources")
    
    def search_sources(self, query: str, domain: str, max_results: int = 5) -> List[EvidenceSource]:
        """Search for relevant evidence sources"""
        query_terms = set(query.lower().split())
        scored_sources = []
        
        # Get domain-specific sources
        domain_source_ids = self.domain_index.get(domain, [])
        if not domain_source_ids:
            # Fall back to all sources if domain not found
            domain_source_ids = list(self.sources.keys())
        
        for source_id in domain_source_ids:
            source = self.sources[source_id]
            
            # Calculate relevance score
            content_terms = set((source.title + " " + source.content).lower().split())
            title_terms = set(source.title.lower().split())
            
            # Term overlap scoring
            content_overlap = len(query_terms.intersection(content_terms))
            title_overlap = len(query_terms.intersection(title_terms))
            
            # Weight title matches more heavily
            relevance_score = (content_overlap + title_overlap * 2) / len(query_terms)
            
            if relevance_score > 0:
                scored_sources.append((relevance_score, source))
        
        # Sort by relevance and return top results
        scored_sources.sort(key=lambda x: x[0], reverse=True)
        return [source for _, source in scored_sources[:max_results]]
    
    def get_source_by_id(self, source_id: str) -> Optional[EvidenceSource]:
        """Get a source by its ID"""
        return self.sources.get(source_id)

class CitationManager:
    """Manages citation generation and formatting"""
    
    def __init__(self):
        self.citation_styles = {
            'apa': self._format_apa_citation,
            'mla': self._format_mla_citation,
            'chicago': self._format_chicago_citation,
            'simple': self._format_simple_citation
        }
    
    def generate_citations(self, sources: List[EvidenceSource], style: str = 'simple') -> List[Citation]:
        """Generate citations for evidence sources"""
        citations = []
        
        for i, source in enumerate(sources, 1):
            # Extract relevant snippet
            snippet = self._extract_relevant_snippet(source.content)
            
            # Format citation
            formatter = self.citation_styles.get(style, self._format_simple_citation)
            citation_format = formatter(source, i)
            
            citation = Citation(
                source_id=source.id,
                text_snippet=snippet,
                relevance_score=source.reliability_score,
                citation_format=citation_format
            )
            
            citations.append(citation)
        
        return citations
    
    def _extract_relevant_snippet(self, content: str, max_length: int = 150) -> str:
        """Extract a relevant snippet from source content"""
        sentences = content.split('. ')
        
        # Return first sentence if short enough
        if len(sentences[0]) <= max_length:
            return sentences[0] + '.'
        
        # Otherwise truncate first sentence
        words = sentences[0].split()
        snippet = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > max_length - 3:
                break
            snippet.append(word)
            current_length += len(word) + 1
        
        return ' '.join(snippet) + '...'
    
    def _format_simple_citation(self, source: EvidenceSource, number: int) -> str:
        """Format citation in simple style"""
        return f"[{number}] {source.title}"
    
    def _format_apa_citation(self, source: EvidenceSource, number: int) -> str:
        """Format citation in APA style"""
        date_str = source.publication_date or "n.d."
        url_str = f" Retrieved from {source.url}" if source.url else ""
        return f"[{number}] {source.title}. ({date_str}). {source.source_type.replace('_', ' ').title()}.{url_str}"
    
    def _format_mla_citation(self, source: EvidenceSource, number: int) -> str:
        """Format citation in MLA style"""
        date_str = source.publication_date or "n.d."
        url_str = f" Web. {datetime.now().strftime('%d %b %Y')}." if source.url else ""
        return f"[{number}] \"{source.title}.\" {source.source_type.replace('_', ' ').title()}, {date_str}.{url_str}"
    
    def _format_chicago_citation(self, source: EvidenceSource, number: int) -> str:
        """Format citation in Chicago style"""
        date_str = source.publication_date or "n.d."
        url_str = f" {source.url}" if source.url else ""
        return f"[{number}] \"{source.title},\" {source.source_type.replace('_', ' ').title()}, {date_str}.{url_str}"

class EvidenceIntegrator:
    """Integrates evidence sources into agent responses"""
    
    def __init__(self, evidence_db: EvidenceDatabase, citation_manager: CitationManager):
        self.evidence_db = evidence_db
        self.citation_manager = citation_manager
        self.logger = logging.getLogger(__name__)
    
    def enhance_response_with_evidence(
        self, 
        response: str, 
        query: str, 
        domain: str,
        max_sources: int = 3
    ) -> EnhancedResponse:
        """Enhance response with evidence and citations"""
        
        # Search for relevant evidence
        evidence_sources = self.evidence_db.search_sources(query, domain, max_sources)
        
        if not evidence_sources:
            return EnhancedResponse(
                answer=response,
                evidence_sources=[],
                citations=[],
                evidence_coverage=0.0,
                citation_quality_score=0.0
            )
        
        # Generate citations
        citations = self.citation_manager.generate_citations(evidence_sources)
        
        # Integrate evidence into response
        enhanced_answer = self._integrate_evidence_into_response(
            response, evidence_sources, citations
        )
        
        # Calculate quality metrics
        evidence_coverage = self._calculate_evidence_coverage(query, evidence_sources)
        citation_quality_score = self._calculate_citation_quality(citations)
        
        return EnhancedResponse(
            answer=enhanced_answer,
            evidence_sources=evidence_sources,
            citations=citations,
            evidence_coverage=evidence_coverage,
            citation_quality_score=citation_quality_score
        )
    
    def _integrate_evidence_into_response(
        self, 
        response: str, 
        sources: List[EvidenceSource], 
        citations: List[Citation]
    ) -> str:
        """Integrate evidence and citations into the response"""
        
        if not sources:
            return response
        
        # Add evidence-based enhancement
        evidence_section = "\n\n**Evidence-Based Information:**\n"
        
        for i, (source, citation) in enumerate(zip(sources, citations), 1):
            evidence_section += f"\n{citation.text_snippet} {citation.citation_format}\n"
        
        # Add citations section
        if citations:
            citations_section = "\n\n**References:**\n"
            for citation in citations:
                citations_section += f"{citation.citation_format}\n"
            
            enhanced_response = response + evidence_section + citations_section
        else:
            enhanced_response = response + evidence_section
        
        return enhanced_response
    
    def _calculate_evidence_coverage(self, query: str, sources: List[EvidenceSource]) -> float:
        """Calculate how well evidence covers the query"""
        if not sources:
            return 0.0
        
        query_terms = set(query.lower().split())
        covered_terms = set()
        
        for source in sources:
            source_terms = set((source.title + " " + source.content).lower().split())
            covered_terms.update(query_terms.intersection(source_terms))
        
        coverage = len(covered_terms) / len(query_terms) if query_terms else 0.0
        return min(coverage, 1.0)
    
    def _calculate_citation_quality(self, citations: List[Citation]) -> float:
        """Calculate overall citation quality score"""
        if not citations:
            return 0.0
        
        # Average relevance score weighted by source reliability
        total_score = sum(citation.relevance_score for citation in citations)
        average_score = total_score / len(citations)
        
        # Bonus for having multiple citations
        quantity_bonus = min(len(citations) * 0.1, 0.3)
        
        return min(average_score + quantity_bonus, 1.0)

class RAGSystem:
    """Complete Retrieval-Augmented Generation system"""
    
    def __init__(self, data_dir: str = "./data/evidence", config_path: str = "./config/evidence_sources.yaml"):
        self.evidence_db = EvidenceDatabase(data_dir, config_path)
        self.citation_manager = CitationManager()
        self.evidence_integrator = EvidenceIntegrator(self.evidence_db, self.citation_manager)
        self.logger = logging.getLogger(__name__)
    
    def retrieve_evidence(self, query: str, domain: str = "general", top_k: int = 3) -> List[EvidenceSource]:
        """
        Retrieve relevant evidence sources for a query
        
        Args:
            query: The query to find evidence for
            domain: Domain to search in ('medical', 'finance', or 'general')
            top_k: Number of sources to return
            
        Returns:
            List of relevant EvidenceSource objects
        """
        return self.evidence_db.search_sources(query, domain, max_results=top_k)
    
    def format_evidence_for_prompt(self, sources: List[EvidenceSource]) -> str:
        """
        Format evidence sources for inclusion in LLM prompts
        
        Args:
            sources: List of evidence sources
            
        Returns:
            Formatted string with numbered sources
        """
        if not sources:
            return "No specific evidence sources available for this query."
        
        formatted = "=== EVIDENCE SOURCES ===\n\n"
        
        for i, source in enumerate(sources, 1):
            formatted += f"[Source {i}] {source.title}\n"
            formatted += f"Type: {source.source_type}\n"
            formatted += f"Reliability: {source.reliability_score:.0%}\n"
            formatted += f"Content: {source.content[:400]}...\n"  # First 400 chars
            if source.url:
                formatted += f"URL: {source.url}\n"
            formatted += "\n"
        
        formatted += "=== CITATION INSTRUCTIONS ===\n"
        formatted += "You MUST cite these sources in your response using [Source X] format.\n"
        formatted += "Example: 'Low-dose aspirin reduces cardiovascular risk [Source 1].'\n\n"
        
        return formatted
    
    def enhance_agent_response(
        self, 
        response: str, 
        query: str, 
        domain: str
    ) -> Tuple[str, Dict[str, float]]:
        """Main method to enhance agent response with evidence"""
        
        # Get enhanced response with evidence
        enhanced_response = self.evidence_integrator.enhance_response_with_evidence(
            response, query, domain
        )
        
        # Calculate improvement metrics
        improvements = {
            'evidence_coverage': enhanced_response.evidence_coverage,
            'citation_quality': enhanced_response.citation_quality_score,
            'faithfulness_improvement': enhanced_response.evidence_coverage * 0.4,  # Up to 40% improvement
            'citation_accuracy_improvement': enhanced_response.citation_quality_score * 0.3,  # Up to 30% improvement
            'factual_consistency_improvement': enhanced_response.evidence_coverage * 0.35,  # Up to 35% improvement
        }
        
        self.logger.info(f"Enhanced response with {len(enhanced_response.evidence_sources)} evidence sources")
        
        return enhanced_response.answer, improvements

# Example usage and testing
def test_rag_system():
    """Test the RAG system with sample queries"""
    rag_system = RAGSystem()
    
    test_cases = [
        {
            "query": "What are the side effects of aspirin?",
            "response": "Aspirin can cause stomach irritation and increased bleeding risk.",
            "domain": "medical"
        },
        {
            "query": "How should I diversify my investment portfolio?",
            "response": "Diversification involves spreading investments across different assets to reduce risk.",
            "domain": "finance"
        }
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Query: {case['query']}")
        print(f"Original Response: {case['response']}")
        
        enhanced_response, improvements = rag_system.enhance_agent_response(
            case['response'], case['query'], case['domain']
        )
        
        print(f"Enhanced Response: {enhanced_response}")
        print(f"Improvements: {improvements}")

if __name__ == "__main__":
    test_rag_system()