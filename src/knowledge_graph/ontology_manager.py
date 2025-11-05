"""
Ontology Manager Module

Manages OWL ontologies for domain knowledge representation in FAIR-Agent.
"""

import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

import owlready2 as owl

from ..utils.logger import get_logger


class OntologyManager:
    """
    Manages OWL ontologies for structured domain knowledge

    Provides functionality to create, load, and reason with ontologies
    for finance and medical domains.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the ontology manager

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = get_logger(__name__)

        # Ontology world
        self.world = owl.World()

        # Loaded ontologies
        self.ontologies = {}

        # Base IRI for FAIR-Agent ontologies
        self.base_iri = "http://fair-agent.org"

        self.logger.info("Ontology Manager initialized")

    def create_domain_ontology(self, domain: str, name: str) -> Optional[owl.Ontology]:
        """
        Create a new domain ontology

        Args:
            domain: Domain name (finance, medical)
            name: Ontology name

        Returns:
            Created ontology or None if failed
        """
        try:
            iri = f"{self.base_iri}/{domain}/{name}#"
            onto = self.world.get_ontology(iri)

            self.ontologies[f"{domain}_{name}"] = onto

            with onto:
                # Add basic classes
                class DomainEntity(owl.Thing):
                    """Base entity for this domain"""
                    pass

                class Concept(DomainEntity):
                    """Domain concepts"""
                    pass

                class Relation(DomainEntity):
                    """Domain relationships"""
                    pass

            self.logger.info(f"Created ontology: {domain}/{name}")
            return onto

        except Exception as e:
            self.logger.error(f"Failed to create ontology {domain}/{name}: {e}")
            return None

    def load_ontology_from_file(self, filepath: str, name: str) -> Optional[owl.Ontology]:
        """
        Load ontology from OWL file

        Args:
            filepath: Path to OWL file
            name: Name for the loaded ontology

        Returns:
            Loaded ontology or None if failed
        """
        try:
            onto = self.world.get_ontology(f"file://{filepath}")
            onto.load()

            self.ontologies[name] = onto
            self.logger.info(f"Loaded ontology from {filepath}")
            return onto

        except Exception as e:
            self.logger.error(f"Failed to load ontology from {filepath}: {e}")
            return None

    def add_class(self, ontology_name: str, class_name: str,
                  parent_classes: Optional[List[str]] = None) -> bool:
        """
        Add a class to an ontology

        Args:
            ontology_name: Name of the ontology
            class_name: Name of the class to add
            parent_classes: List of parent class names

        Returns:
            Success status
        """
        try:
            if ontology_name not in self.ontologies:
                self.logger.error(f"Ontology {ontology_name} not found")
                return False

            onto = self.ontologies[ontology_name]

            with onto:
                # Determine parent classes
                parents = []
                if parent_classes:
                    for parent_name in parent_classes:
                        parent_class = getattr(onto, parent_name, None)
                        if parent_class:
                            parents.append(parent_class)
                        else:
                            self.logger.warning(f"Parent class {parent_name} not found")

                if not parents:
                    parents = [owl.Thing]

                # Create the class
                NewClass = type(class_name, tuple(parents), {})
                setattr(onto, class_name, NewClass)

            self.logger.debug(f"Added class {class_name} to ontology {ontology_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add class {class_name}: {e}")
            return False

    def add_property(self, ontology_name: str, property_name: str, property_type: str,
                    domain: Optional[List[str]] = None, range: Optional[List[Any]] = None) -> bool:
        """
        Add a property to an ontology

        Args:
            ontology_name: Name of the ontology
            property_name: Name of the property
            property_type: Type of property (ObjectProperty, DataProperty, AnnotationProperty)
            domain: Domain classes
            range: Range classes or datatypes

        Returns:
            Success status
        """
        try:
            if ontology_name not in self.ontologies:
                self.logger.error(f"Ontology {ontology_name} not found")
                return False

            onto = self.ontologies[ontology_name]

            with onto:
                # Create property based on type
                if property_type == "ObjectProperty":
                    prop_class = owl.ObjectProperty
                elif property_type == "DataProperty":
                    prop_class = owl.DataProperty
                elif property_type == "AnnotationProperty":
                    prop_class = owl.AnnotationProperty
                else:
                    self.logger.error(f"Unknown property type: {property_type}")
                    return False

                # Create the property
                NewProperty = type(property_name, (prop_class,), {})
                setattr(onto, property_name, NewProperty)

                prop = getattr(onto, property_name)

                # Set domain
                if domain:
                    domain_classes = []
                    for class_name in domain:
                        cls = getattr(onto, class_name, None)
                        if cls:
                            domain_classes.append(cls)
                    if domain_classes:
                        prop.domain = domain_classes

                # Set range
                if range:
                    if property_type == "DataProperty":
                        # For data properties, range should be datatypes
                        prop.range = range
                    else:
                        # For object properties, range should be classes
                        range_classes = []
                        for class_name in range:
                            cls = getattr(onto, class_name, None)
                            if cls:
                                range_classes.append(cls)
                        if range_classes:
                            prop.range = range_classes

            self.logger.debug(f"Added {property_type} {property_name} to ontology {ontology_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to add property {property_name}: {e}")
            return False

    def create_individual(self, ontology_name: str, class_name: str,
                         individual_name: str) -> Optional[owl.Thing]:
        """
        Create an individual (instance) of a class

        Args:
            ontology_name: Name of the ontology
            class_name: Name of the class
            individual_name: Name of the individual

        Returns:
            Created individual or None if failed
        """
        try:
            if ontology_name not in self.ontologies:
                self.logger.error(f"Ontology {ontology_name} not found")
                return None

            onto = self.ontologies[ontology_name]

            with onto:
                cls = getattr(onto, class_name, None)
                if not cls:
                    self.logger.error(f"Class {class_name} not found in ontology {ontology_name}")
                    return None

                individual = cls(individual_name)
                setattr(onto, individual_name, individual)

            self.logger.debug(f"Created individual {individual_name} of class {class_name}")
            return individual

        except Exception as e:
            self.logger.error(f"Failed to create individual {individual_name}: {e}")
            return None

    def run_reasoner(self, ontology_name: str) -> bool:
        """
        Run OWL reasoner on an ontology

        Args:
            ontology_name: Name of the ontology

        Returns:
            Success status
        """
        try:
            if ontology_name not in self.ontologies:
                self.logger.error(f"Ontology {ontology_name} not found")
                return False

            onto = self.ontologies[ontology_name]

            # Run HermiT reasoner (default)
            owl.sync_reasoner(onto, debug=False)

            self.logger.info(f"Reasoner completed for ontology {ontology_name}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to run reasoner on {ontology_name}: {e}")
            return False

    def query_ontology(self, ontology_name: str, query: str) -> List[Dict[str, Any]]:
        """
        Query an ontology using SPARQL

        Args:
            ontology_name: Name of the ontology
            query: SPARQL query string

        Returns:
            Query results
        """
        try:
            if ontology_name not in self.ontologies:
                self.logger.error(f"Ontology {ontology_name} not found")
                return []

            onto = self.ontologies[ontology_name]

            # Execute SPARQL query
            results = list(onto.world.sparql(query))

            # Convert results to dictionaries
            processed_results = []
            for result in results:
                result_dict = {}
                for var_name, value in result.items():
                    if hasattr(value, 'name'):
                        result_dict[str(var_name)] = value.name
                    else:
                        result_dict[str(var_name)] = str(value)
                processed_results.append(result_dict)

            return processed_results

        except Exception as e:
            self.logger.error(f"Failed to query ontology {ontology_name}: {e}")
            return []

    def save_ontology(self, ontology_name: str, filepath: str) -> bool:
        """
        Save ontology to file

        Args:
            ontology_name: Name of the ontology
            filepath: Path to save the ontology

        Returns:
            Success status
        """
        try:
            if ontology_name not in self.ontologies:
                self.logger.error(f"Ontology {ontology_name} not found")
                return False

            onto = self.ontologies[ontology_name]

            # Save ontology
            onto.save(file=str(filepath))

            self.logger.info(f"Ontology {ontology_name} saved to {filepath}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to save ontology {ontology_name}: {e}")
            return False

    def get_ontology_info(self, ontology_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an ontology

        Args:
            ontology_name: Name of the ontology

        Returns:
            Ontology information dictionary
        """
        try:
            if ontology_name not in self.ontologies:
                return None

            onto = self.ontologies[ontology_name]

            info = {
                'name': ontology_name,
                'iri': onto.base_iri,
                'classes': len(list(onto.classes())),
                'properties': len(list(onto.properties())),
                'individuals': len(list(onto.individuals())),
            }

            return info

        except Exception as e:
            self.logger.error(f"Failed to get ontology info for {ontology_name}: {e}")
            return None

    def list_ontologies(self) -> List[str]:
        """List all loaded ontologies"""
        return list(self.ontologies.keys())