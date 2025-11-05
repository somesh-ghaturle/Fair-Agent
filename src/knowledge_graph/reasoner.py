"""
Knowledge Graph Reasoner Module

Provides reasoning capabilities over knowledge graphs for FAIR-Agent.
"""

import logging
from typing import Dict, List, Optional, Any, Set, Tuple
from collections import defaultdict

import networkx as nx
from networkx.algorithms import shortest_path, community

from ..utils.logger import get_logger
from .knowledge_graph import KnowledgeGraph


class KnowledgeGraphReasoner:
    """
    Provides reasoning capabilities over knowledge graphs

    Supports path finding, inference, community detection, and
    other graph algorithms for enhanced AI reasoning.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the knowledge graph reasoner

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = get_logger(__name__)

        self.logger.info("Knowledge Graph Reasoner initialized")

    def find_paths(self, kg: KnowledgeGraph, start_entity: str, end_entity: str,
                  max_length: int = 3) -> List[List[str]]:
        """
        Find paths between entities in the knowledge graph

        Args:
            kg: Knowledge graph to reason over
            start_entity: Starting entity ID
            end_entity: Ending entity ID
            max_length: Maximum path length

        Returns:
            List of paths (each path is a list of entity IDs)
        """
        try:
            if start_entity not in kg.network_graph or end_entity not in kg.network_graph:
                return []

            # Use NetworkX to find all simple paths
            paths = list(nx.all_simple_paths(kg.network_graph, start_entity, end_entity,
                                           cutoff=max_length))

            self.logger.debug(f"Found {len(paths)} paths from {start_entity} to {end_entity}")
            return paths

        except Exception as e:
            self.logger.error(f"Failed to find paths from {start_entity} to {end_entity}: {e}")
            return []

    def infer_relationships(self, kg: KnowledgeGraph, entity: str,
                           inference_rules: Optional[List[Dict]] = None) -> List[Dict[str, Any]]:
        """
        Infer new relationships based on existing knowledge and rules

        Args:
            kg: Knowledge graph to reason over
            entity: Entity to infer relationships for
            inference_rules: Custom inference rules

        Returns:
            List of inferred relationships
        """
        try:
            inferred_rels = []

            # Default inference rules
            if not inference_rules:
                inference_rules = self._get_default_inference_rules()

            # Apply each rule
            for rule in inference_rules:
                new_rels = self._apply_inference_rule(kg, entity, rule)
                inferred_rels.extend(new_rels)

            self.logger.debug(f"Inferred {len(inferred_rels)} relationships for {entity}")
            return inferred_rels

        except Exception as e:
            self.logger.error(f"Failed to infer relationships for {entity}: {e}")
            return []

    def _get_default_inference_rules(self) -> List[Dict]:
        """Get default inference rules for FAIR-Agent domains"""
        return [
            # Medical inference rules
            {
                "name": "treats_transitivity",
                "premise": [("X", "treats", "Y"), ("Y", "causes", "Z")],
                "conclusion": ("X", "treats", "Z"),
                "domain": "medical"
            },
            {
                "name": "symptom_indication",
                "premise": [("X", "has_symptom", "Y"), ("Y", "indicates", "Z")],
                "conclusion": ("X", "may_have", "Z"),
                "domain": "medical"
            },
            # Financial inference rules
            {
                "name": "risk_transmission",
                "premise": [("X", "invests_in", "Y"), ("Y", "has_risk", "Z")],
                "conclusion": ("X", "exposed_to", "Z"),
                "domain": "finance"
            },
            {
                "name": "diversification_benefit",
                "premise": [("X", "uses", "diversification"), ("Y", "has", "volatility")],
                "conclusion": ("X", "reduces", "Y"),
                "domain": "finance"
            }
        ]

    def _apply_inference_rule(self, kg: KnowledgeGraph, entity: str,
                            rule: Dict) -> List[Dict[str, Any]]:
        """Apply a single inference rule"""
        try:
            inferred = []

            # This is a simplified implementation
            # In production, you'd use proper rule engines like Prolog or custom matchers

            premise_patterns = rule["premise"]
            conclusion = rule["conclusion"]

            # For now, just check direct relationships
            # A full implementation would use graph pattern matching

            related_entities = kg.find_related_entities(entity)

            # Simple pattern matching for the first premise
            if premise_patterns:
                first_premise = premise_patterns[0]
                if len(first_premise) == 3:
                    _, relation, target_type = first_premise

                    # Check if entity has the required relationship
                    if relation in related_entities:
                        for related_entity in related_entities[relation]:
                            # Create inferred relationship
                            inferred.append({
                                "source": entity,
                                "target": related_entity,
                                "relation": conclusion[1] if len(conclusion) > 1 else "related_to",
                                "confidence": 0.7,  # Placeholder confidence
                                "rule": rule["name"],
                                "domain": rule.get("domain", "general")
                            })

            return inferred

        except Exception as e:
            self.logger.error(f"Failed to apply inference rule {rule.get('name', 'unknown')}: {e}")
            return []

    def detect_communities(self, kg: KnowledgeGraph) -> List[List[str]]:
        """
        Detect communities in the knowledge graph

        Args:
            kg: Knowledge graph to analyze

        Returns:
            List of communities (each community is a list of entity IDs)
        """
        try:
            # Use Louvain community detection
            communities = community.louvain_communities(kg.network_graph)

            # Convert to list of lists
            community_list = [list(comm) for comm in communities]

            self.logger.info(f"Detected {len(community_list)} communities")
            return community_list

        except Exception as e:
            self.logger.error(f"Failed to detect communities: {e}")
            return []

    def calculate_centrality(self, kg: KnowledgeGraph) -> Dict[str, float]:
        """
        Calculate centrality measures for entities

        Args:
            kg: Knowledge graph to analyze

        Returns:
            Dictionary mapping entity IDs to centrality scores
        """
        try:
            # Calculate degree centrality
            centrality = nx.degree_centrality(kg.network_graph)

            self.logger.debug(f"Calculated centrality for {len(centrality)} entities")
            return centrality

        except Exception as e:
            self.logger.error(f"Failed to calculate centrality: {e}")
            return {}

    def find_similar_entities(self, kg: KnowledgeGraph, entity: str,
                            top_k: int = 5) -> List[Tuple[str, float]]:
        """
        Find entities similar to a given entity

        Args:
            kg: Knowledge graph to analyze
            entity: Entity ID to find similar entities for
            top_k: Number of similar entities to return

        Returns:
            List of (entity_id, similarity_score) tuples
        """
        try:
            if entity not in kg.network_graph:
                return []

            # Simple similarity based on common neighbors
            similarities = {}

            entity_neighbors = set(kg.network_graph.neighbors(entity))

            for other_entity in kg.network_graph.nodes():
                if other_entity == entity:
                    continue

                other_neighbors = set(kg.network_graph.neighbors(other_entity))

                # Jaccard similarity of neighbor sets
                intersection = len(entity_neighbors & other_neighbors)
                union = len(entity_neighbors | other_neighbors)

                if union > 0:
                    similarity = intersection / union
                    similarities[other_entity] = similarity

            # Sort by similarity and return top-k
            sorted_similar = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
            top_similar = sorted_similar[:top_k]

            self.logger.debug(f"Found {len(top_similar)} similar entities for {entity}")
            return top_similar

        except Exception as e:
            self.logger.error(f"Failed to find similar entities for {entity}: {e}")
            return []

    def explain_relationship(self, kg: KnowledgeGraph, source: str, target: str) -> Dict[str, Any]:
        """
        Explain the relationship between two entities

        Args:
            kg: Knowledge graph to analyze
            source: Source entity ID
            target: Target entity ID

        Returns:
            Explanation dictionary
        """
        try:
            explanation = {
                "source": source,
                "target": target,
                "direct_relation": None,
                "paths": [],
                "inferred_relations": [],
                "confidence": 0.0
            }

            # Check for direct relationship
            if kg.network_graph.has_edge(source, target):
                edge_data = kg.network_graph.get_edge_data(source, target)
                explanation["direct_relation"] = edge_data.get("relation", "related_to")

            # Find paths
            paths = self.find_paths(kg, source, target, max_length=4)
            explanation["paths"] = paths

            # Calculate confidence based on path length and direct relations
            if explanation["direct_relation"]:
                explanation["confidence"] = 1.0
            elif paths:
                # Confidence decreases with path length
                min_path_length = min(len(path) - 1 for path in paths)  # -1 because path includes start
                explanation["confidence"] = max(0.1, 1.0 / (min_path_length + 1))
            else:
                explanation["confidence"] = 0.0

            # Try to infer relationships
            inferred = self.infer_relationships(kg, source)
            relevant_inferred = [inf for inf in inferred if inf["target"] == target]
            explanation["inferred_relations"] = relevant_inferred

            return explanation

        except Exception as e:
            self.logger.error(f"Failed to explain relationship between {source} and {target}: {e}")
            return {
                "source": source,
                "target": target,
                "error": str(e)
            }

    def validate_facts(self, kg: KnowledgeGraph, facts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Validate facts against the knowledge graph

        Args:
            kg: Knowledge graph to validate against
            facts: List of facts to validate

        Returns:
            List of validation results
        """
        try:
            results = []

            for fact in facts:
                validation = {
                    "fact": fact,
                    "is_valid": False,
                    "confidence": 0.0,
                    "supporting_evidence": [],
                    "conflicting_evidence": []
                }

                # Check if entities exist
                source = fact.get("source")
                target = fact.get("target")
                relation = fact.get("relation", "related_to")

                if not source or not target:
                    validation["error"] = "Missing source or target entity"
                    results.append(validation)
                    continue

                # Check if entities exist in graph
                if source not in kg.network_graph or target not in kg.network_graph:
                    validation["error"] = "Entity not found in knowledge graph"
                    results.append(validation)
                    continue

                # Check direct relationship
                if kg.network_graph.has_edge(source, target):
                    edge_data = kg.network_graph.get_edge_data(source, target)
                    if edge_data.get("relation") == relation:
                        validation["is_valid"] = True
                        validation["confidence"] = 1.0
                        validation["supporting_evidence"].append("Direct relationship found")

                # Check for paths (indirect evidence)
                paths = self.find_paths(kg, source, target, max_length=3)
                if paths:
                    validation["confidence"] = max(validation["confidence"], 0.5)
                    validation["supporting_evidence"].append(f"Found {len(paths)} paths between entities")

                # Check inferred relationships
                inferred = self.infer_relationships(kg, source)
                relevant_inferred = [inf for inf in inferred if inf["target"] == target and inf["relation"] == relation]
                if relevant_inferred:
                    validation["is_valid"] = True
                    validation["confidence"] = max(validation["confidence"], 0.7)
                    validation["supporting_evidence"].append("Relationship can be inferred")

                results.append(validation)

            return results

        except Exception as e:
            self.logger.error(f"Failed to validate facts: {e}")
            return []

    def get_reasoning_statistics(self, kg: KnowledgeGraph) -> Dict[str, Any]:
        """
        Get statistics about reasoning capabilities

        Args:
            kg: Knowledge graph to analyze

        Returns:
            Statistics dictionary
        """
        try:
            stats = {
                "total_entities": kg.network_graph.number_of_nodes(),
                "total_relationships": kg.network_graph.number_of_edges(),
                "communities_detected": len(self.detect_communities(kg)),
                "average_centrality": 0.0,
                "connected_components": nx.number_connected_components(kg.network_graph)
            }

            # Calculate average centrality
            centrality = self.calculate_centrality(kg)
            if centrality:
                stats["average_centrality"] = sum(centrality.values()) / len(centrality)

            return stats

        except Exception as e:
            self.logger.error(f"Failed to get reasoning statistics: {e}")
            return {}