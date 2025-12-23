"""
Knowledge Graph Implementation using NetworkX
Learns entities and relationships from user queries and system responses.
"""

import logging
import networkx as nx
import json
from pathlib import Path
import os
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

class KnowledgeGraph:
    def __init__(self, persist_path: str = None):
        if persist_path:
            self.persist_path = Path(persist_path)
        else:
            root_dir = Path(__file__).resolve().parent.parent.parent
            self.persist_path = root_dir / "data" / "knowledge_graph" / "graph.json"
            
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        
        self.graph = nx.MultiDiGraph()
        self.load_graph()

    def load_graph(self):
        """Load graph from disk"""
        if self.persist_path.exists():
            try:
                with open(self.persist_path, 'r') as f:
                    data = json.load(f)
                    # Handle both 'edges' and 'links' keys for compatibility
                    if 'edges' in data:
                        self.graph = nx.node_link_graph(data, edges="edges")
                    else:
                        self.graph = nx.node_link_graph(data)
                logger.info(f"✅ Loaded Knowledge Graph with {self.graph.number_of_nodes()} nodes")
            except Exception as e:
                logger.error(f"Failed to load Knowledge Graph: {e}")
                self.graph = nx.MultiDiGraph()

    def save_graph(self):
        """Save graph to disk"""
        try:
            # Explicitly use 'edges' for consistency
            data = nx.node_link_data(self.graph, edges="edges")
            with open(self.persist_path, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info("Saved Knowledge Graph to disk")
        except Exception as e:
            logger.error(f"Failed to save Knowledge Graph: {e}")

    def add_entity(self, entity: str, type: str = "concept"):
        """Add an entity node to the graph"""
        if not self.graph.has_node(entity):
            self.graph.add_node(entity, type=type)

    def add_relation(self, source: str, target: str, relation: str, weight: float = 1.0):
        """Add a relationship edge between entities"""
        self.add_entity(source)
        self.add_entity(target)
        self.graph.add_edge(source, target, relation=relation, weight=weight)
        self.save_graph()

    def get_related_entities(self, entity: str, limit: int = 5) -> List[Dict]:
        """Get entities related to the given entity"""
        if not self.graph.has_node(entity):
            return []
        
        related = []
        for neighbor in self.graph.neighbors(entity):
            edges = self.graph.get_edge_data(entity, neighbor)
            for key, data in edges.items():
                related.append({
                    "entity": neighbor,
                    "relation": data.get("relation", "related_to"),
                    "weight": data.get("weight", 1.0)
                })
        
        # Sort by weight
        related.sort(key=lambda x: x["weight"], reverse=True)
        return related[:limit]

    def extract_and_learn(self, text: str, llm_client=None):
        """
        Extract entities and relations from text using LLM and update graph.
        This is a simplified implementation. In a real system, you'd use an LLM
        to parse the text into (Subject, Predicate, Object) triples.
        """
        if not llm_client:
            return

        # Prompt for the LLM to extract triples
        prompt = f"""
        Extract knowledge graph triples from the following text.
        Format: Subject | Predicate | Object
        Text: {text}
        """
        
        try:
            # This is a placeholder for the actual LLM call
            # response = llm_client.generate(prompt)
            # triples = parse_response(response)
            # for s, p, o in triples:
            #     self.add_relation(s, o, p)
            pass
        except Exception as e:
            logger.error(f"Error extracting knowledge: {e}")

    def search_graph(self, query_terms: List[str]) -> List[str]:
        """Search the graph for relevant context based on query terms"""
        context = []
        for term in query_terms:
            # Simple case-insensitive matching
            for node in self.graph.nodes():
                if term.lower() in str(node).lower():
                    related = self.get_related_entities(node)
                    for rel in related:
                        context.append(f"{node} is {rel['relation']} {rel['entity']}")
        return list(set(context))  # Deduplicate
