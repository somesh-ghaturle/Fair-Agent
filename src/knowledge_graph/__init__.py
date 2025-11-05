"""
Knowledge Graph Module for FAIR-Agent

This module provides knowledge graph capabilities for representing and reasoning
about domain knowledge in finance and medical domains.
"""

from .knowledge_graph import KnowledgeGraph
from .ontology_manager import OntologyManager
from .graph_builder import GraphBuilder
from .reasoner import KnowledgeGraphReasoner

__all__ = [
    'KnowledgeGraph',
    'OntologyManager',
    'GraphBuilder',
    'KnowledgeGraphReasoner'
]