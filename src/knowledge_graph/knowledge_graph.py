"""
Knowledge Graph Core Module

Provides the main KnowledgeGraph class for representing and managing
domain knowledge in FAIR-Agent.
"""

import logging
from typing import Dict, List, Optional, Set, Tuple, Any
from pathlib import Path
import json

from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, RDFS, OWL, XSD
from networkx import DiGraph
import owlready2 as owl

from ..utils.logger import get_logger


class KnowledgeGraph:
    """
    Main Knowledge Graph class for FAIR-Agent

    Supports both RDF (using rdflib) and property graph representations,
    with OWL ontology support for domain modeling.
    """

    def __init__(self, name: str = "fair_agent_kg", config: Optional[Dict] = None):
        """
        Initialize the knowledge graph

        Args:
            name: Name of the knowledge graph
            config: Configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self.logger = get_logger(__name__)

        # RDF Graph for semantic web representation
        self.rdf_graph = Graph()

        # NetworkX graph for algorithmic operations
        self.network_graph = DiGraph()

        # Ontology world for OWL reasoning
        self.ontology_world = owl.World()

        # Define namespaces
        self._setup_namespaces()

        # Initialize with basic FAIR-Agent ontology
        self._initialize_base_ontology()

        self.logger.info(f"Knowledge Graph '{name}' initialized")

    def _setup_namespaces(self):
        """Setup RDF namespaces for the knowledge graph"""
        self.namespaces = {
            'fair': Namespace('http://fair-agent.org/ontology#'),
            'finance': Namespace('http://fair-agent.org/finance#'),
            'medical': Namespace('http://fair-agent.org/medical#'),
            'evidence': Namespace('http://fair-agent.org/evidence#'),
            'agent': Namespace('http://fair-agent.org/agent#'),
        }

        # Bind namespaces to RDF graph
        for prefix, ns in self.namespaces.items():
            self.rdf_graph.bind(prefix, ns)

    def _initialize_base_ontology(self):
        """Initialize base FAIR-Agent ontology"""
        try:
            # Create base ontology
            onto = self.ontology_world.get_ontology("http://fair-agent.org/ontology#")

            with onto:
                # Base classes
                class Entity(owl.Thing):
                    """Base class for all entities"""
                    pass

                class Concept(Entity):
                    """Abstract concepts"""
                    pass

                class Instance(Entity):
                    """Concrete instances"""
                    pass

                # Domain-specific classes
                class FinancialConcept(Concept):
                    """Financial domain concepts"""
                    pass

                class MedicalConcept(Concept):
                    """Medical domain concepts"""
                    pass

                class Evidence(Concept):
                    """Evidence and sources"""
                    pass

                # Properties
                class has_name(owl.DataProperty):
                    """Entity name"""
                    domain = [Entity]
                    range = [str]

                class has_description(owl.DataProperty):
                    """Entity description"""
                    domain = [Entity]
                    range = [str]

                class related_to(owl.ObjectProperty):
                    """Generic relationship"""
                    domain = [Entity]
                    range = [Entity]

                class causes(owl.ObjectProperty):
                    """Causal relationship"""
                    domain = [Concept]
                    range = [Concept]

                class treats(owl.ObjectProperty):
                    """Treatment relationship"""
                    domain = [MedicalConcept]
                    range = [MedicalConcept]

                class invests_in(owl.ObjectProperty):
                    """Investment relationship"""
                    domain = [FinancialConcept]
                    range = [FinancialConcept]

            self.logger.info("Base FAIR-Agent ontology initialized")

        except Exception as e:
            self.logger.error(f"Failed to initialize base ontology: {e}")

    def add_entity(self, entity_id: str, entity_type: str, properties: Dict[str, Any],
                   domain: str = "general") -> bool:
        """
        Add an entity to the knowledge graph

        Args:
            entity_id: Unique identifier for the entity
            entity_type: Type/class of the entity
            properties: Entity properties
            domain: Domain (finance, medical, general)

        Returns:
            Success status
        """
        try:
            # Create RDF URI
            if domain in self.namespaces:
                uri = self.namespaces[domain][entity_id]
            else:
                uri = self.namespaces['fair'][entity_id]

            # Add to RDF graph
            self.rdf_graph.add((uri, RDF.type, self.namespaces['fair'][entity_type]))

            # Add properties
            for prop_name, prop_value in properties.items():
                if isinstance(prop_value, str):
                    self.rdf_graph.add((uri, self.namespaces['fair'][prop_name],
                                      Literal(prop_value, datatype=XSD.string)))
                elif isinstance(prop_value, int):
                    self.rdf_graph.add((uri, self.namespaces['fair'][prop_name],
                                      Literal(prop_value, datatype=XSD.integer)))
                elif isinstance(prop_value, float):
                    self.rdf_graph.add((uri, self.namespaces['fair'][prop_name],
                                      Literal(prop_value, datatype=XSD.float)))
                else:
                    self.rdf_graph.add((uri, self.namespaces['fair'][prop_name],
                                      Literal(str(prop_value))))

            # Add to NetworkX graph
            self.network_graph.add_node(entity_id, **properties, type=entity_type, domain=domain)

            self.logger.debug(f"Added entity: {entity_id} ({entity_type})")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add entity {entity_id}: {e}")
            return False

    def add_relationship(self, source_id: str, target_id: str, relation_type: str,
                        properties: Optional[Dict[str, Any]] = None) -> bool:
        """
        Add a relationship between entities

        Args:
            source_id: Source entity ID
            target_id: Target entity ID
            relation_type: Type of relationship
            properties: Relationship properties

        Returns:
            Success status
        """
        try:
            properties = properties or {}

            # Add to RDF graph
            source_uri = self._get_entity_uri(source_id)
            target_uri = self._get_entity_uri(target_id)

            if source_uri and target_uri:
                relation_uri = self.namespaces['fair'][relation_type]
                self.rdf_graph.add((source_uri, relation_uri, target_uri))

                # Add relationship properties as reified statements if needed
                if properties:
                    stmt_node = BNode()
                    self.rdf_graph.add((stmt_node, RDF.type, RDF.Statement))
                    self.rdf_graph.add((stmt_node, RDF.subject, source_uri))
                    self.rdf_graph.add((stmt_node, RDF.predicate, relation_uri))
                    self.rdf_graph.add((stmt_node, RDF.object, target_uri))

                    for prop_name, prop_value in properties.items():
                        self.rdf_graph.add((stmt_node, self.namespaces['fair'][prop_name],
                                          Literal(str(prop_value))))

            # Add to NetworkX graph
            self.network_graph.add_edge(source_id, target_id, relation=relation_type, **properties)

            self.logger.debug(f"Added relationship: {source_id} --{relation_type}--> {target_id}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add relationship {source_id}->{target_id}: {e}")
            return False

    def _get_entity_uri(self, entity_id: str) -> Optional[URIRef]:
        """Get RDF URI for an entity"""
        # Try different namespaces
        for ns in self.namespaces.values():
            uri = ns[entity_id]
            if (uri, None, None) in self.rdf_graph:
                return uri
        return None

    def query_entities(self, entity_type: Optional[str] = None,
                      domain: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Query entities from the knowledge graph

        Args:
            entity_type: Filter by entity type
            domain: Filter by domain

        Returns:
            List of entity dictionaries
        """
        try:
            results = []

            if entity_type:
                type_uri = self.namespaces['fair'][entity_type]
                for entity_uri in self.rdf_graph.subjects(RDF.type, type_uri):
                    entity_data = self._extract_entity_data(entity_uri)
                    if entity_data:
                        results.append(entity_data)
            else:
                # Get all entities
                for entity_uri in self.rdf_graph.subjects(RDF.type, None):
                    entity_data = self._extract_entity_data(entity_uri)
                    if entity_data:
                        results.append(entity_data)

            # Filter by domain if specified
            if domain:
                results = [e for e in results if e.get('domain') == domain]

            return results

        except Exception as e:
            self.logger.error(f"Failed to query entities: {e}")
            return []

    def _extract_entity_data(self, entity_uri: URIRef) -> Optional[Dict[str, Any]]:
        """Extract entity data from RDF graph"""
        try:
            entity_id = str(entity_uri).split('#')[-1] if '#' in str(entity_uri) else str(entity_uri)
            entity_data = {'id': entity_id}

            # Get all properties
            for prop, value in self.rdf_graph.predicate_objects(entity_uri):
                prop_name = str(prop).split('#')[-1] if '#' in str(prop) else str(prop)
                if isinstance(value, Literal):
                    entity_data[prop_name] = str(value)
                else:
                    # Handle object properties
                    obj_id = str(value).split('#')[-1] if '#' in str(value) else str(value)
                    entity_data[prop_name] = obj_id

            return entity_data

        except Exception as e:
            self.logger.error(f"Failed to extract entity data for {entity_uri}: {e}")
            return None

    def find_related_entities(self, entity_id: str, relation_type: Optional[str] = None,
                            max_depth: int = 2) -> Dict[str, List[str]]:
        """
        Find entities related to a given entity

        Args:
            entity_id: Starting entity ID
            relation_type: Filter by relationship type
            max_depth: Maximum traversal depth

        Returns:
            Dictionary of related entities by relationship type
        """
        try:
            if entity_id not in self.network_graph:
                return {}

            related = {}

            # Use NetworkX for graph traversal
            if relation_type:
                # Find specific relationship type
                neighbors = []
                for neighbor in self.network_graph.neighbors(entity_id):
                    edge_data = self.network_graph.get_edge_data(entity_id, neighbor)
                    if edge_data and edge_data.get('relation') == relation_type:
                        neighbors.append(neighbor)
                related[relation_type] = neighbors
            else:
                # Find all relationships
                for neighbor in self.network_graph.neighbors(entity_id):
                    edge_data = self.network_graph.get_edge_data(entity_id, neighbor)
                    if edge_data:
                        rel_type = edge_data.get('relation', 'related_to')
                        if rel_type not in related:
                            related[rel_type] = []
                        related[rel_type].append(neighbor)

            return related

        except Exception as e:
            self.logger.error(f"Failed to find related entities for {entity_id}: {e}")
            return {}

    def save_graph(self, filepath: str) -> bool:
        """
        Save the knowledge graph to file

        Args:
            filepath: Path to save the graph

        Returns:
            Success status
        """
        try:
            # Save RDF graph
            rdf_file = Path(filepath).with_suffix('.ttl')
            self.rdf_graph.serialize(destination=str(rdf_file), format='turtle')

            # Save NetworkX graph
            nx_file = Path(filepath).with_suffix('.json')
            graph_data = {
                'nodes': list(self.network_graph.nodes(data=True)),
                'edges': list(self.network_graph.edges(data=True))
            }

            with open(nx_file, 'w') as f:
                json.dump(graph_data, f, indent=2)

            self.logger.info(f"Knowledge graph saved to {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save knowledge graph: {e}")
            return False

    def load_graph(self, filepath: str) -> bool:
        """
        Load the knowledge graph from file

        Args:
            filepath: Path to load the graph from

        Returns:
            Success status
        """
        try:
            # Load RDF graph
            rdf_file = Path(filepath).with_suffix('.ttl')
            if rdf_file.exists():
                self.rdf_graph.parse(str(rdf_file), format='turtle')

            # Load NetworkX graph
            nx_file = Path(filepath).with_suffix('.json')
            if nx_file.exists():
                with open(nx_file, 'r') as f:
                    graph_data = json.load(f)

                self.network_graph.clear()
                self.network_graph.add_nodes_from(graph_data['nodes'])
                self.network_graph.add_edges_from(graph_data['edges'])

            self.logger.info(f"Knowledge graph loaded from {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to load knowledge graph: {e}")
            return False

    def get_statistics(self) -> Dict[str, Any]:
        """Get knowledge graph statistics"""
        return {
            'rdf_triples': len(self.rdf_graph),
            'network_nodes': self.network_graph.number_of_nodes(),
            'network_edges': self.network_graph.number_of_edges(),
            'namespaces': list(self.namespaces.keys()),
            'domains': list(set(nx_data.get('domain', 'general')
                              for _, nx_data in self.network_graph.nodes(data=True)))
        }