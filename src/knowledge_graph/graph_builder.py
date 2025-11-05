"""
Graph Builder Module

Builds knowledge graphs from various data sources for FAIR-Agent.
"""

import logging
from typing import Dict, List, Optional, Any, Set
from pathlib import Path
import json
import csv

from ..utils.logger import get_logger
from .knowledge_graph import KnowledgeGraph


class GraphBuilder:
    """
    Builds knowledge graphs from structured and unstructured data sources

    Supports building graphs from CSV, JSON, text documents, and domain-specific
    data formats used in FAIR-Agent.
    """

    def __init__(self, config: Optional[Dict] = None):
        """
        Initialize the graph builder

        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.logger = get_logger(__name__)

        self.logger.info("Graph Builder initialized")

    def build_from_csv(self, kg: KnowledgeGraph, csv_file: str,
                      entity_column: str, type_column: Optional[str] = None,
                      domain: str = "general") -> bool:
        """
        Build knowledge graph from CSV file

        Args:
            kg: Knowledge graph to populate
            csv_file: Path to CSV file
            entity_column: Column containing entity IDs
            type_column: Column containing entity types
            domain: Domain for entities

        Returns:
            Success status
        """
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    entity_id = row.get(entity_column)
                    if not entity_id:
                        continue

                    entity_type = row.get(type_column, "Entity") if type_column else "Entity"

                    # Remove entity and type columns from properties
                    properties = {k: v for k, v in row.items()
                                if k not in [entity_column, type_column] and v}

                    kg.add_entity(entity_id, entity_type, properties, domain)

            self.logger.info(f"Built knowledge graph from CSV: {csv_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to build from CSV {csv_file}: {e}")
            return False

    def build_from_json(self, kg: KnowledgeGraph, json_file: str,
                       entity_key: str = "id", type_key: str = "type",
                       domain: str = "general") -> bool:
        """
        Build knowledge graph from JSON file

        Args:
            kg: Knowledge graph to populate
            json_file: Path to JSON file
            entity_key: Key for entity ID
            type_key: Key for entity type
            domain: Domain for entities

        Returns:
            Success status
        """
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Handle both list and dict formats
            if isinstance(data, list):
                entities = data
            elif isinstance(data, dict) and "entities" in data:
                entities = data["entities"]
            else:
                entities = [data]

            for entity_data in entities:
                entity_id = entity_data.get(entity_key)
                if not entity_id:
                    continue

                entity_type = entity_data.get(type_key, "Entity")

                # Remove special keys from properties
                properties = {k: v for k, v in entity_data.items()
                            if k not in [entity_key, type_key]}

                kg.add_entity(entity_id, entity_type, properties, domain)

            self.logger.info(f"Built knowledge graph from JSON: {json_file}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to build from JSON {json_file}: {e}")
            return False

    def build_medical_ontology(self, kg: KnowledgeGraph) -> bool:
        """
        Build medical domain ontology and entities

        Args:
            kg: Knowledge graph to populate

        Returns:
            Success status
        """
        try:
            # Add medical concepts
            medical_concepts = [
                ("diabetes", "Disease", {"description": "Chronic metabolic disorder"}),
                ("insulin", "Medication", {"description": "Hormone for blood sugar control"}),
                ("glucose", "Biomarker", {"description": "Blood sugar measurement"}),
                ("hypertension", "Disease", {"description": "High blood pressure"}),
                ("aspirin", "Medication", {"description": "Pain reliever and anti-inflammatory"}),
                ("cardiovascular", "System", {"description": "Heart and blood vessel system"}),
            ]

            for concept_id, concept_type, properties in medical_concepts:
                kg.add_entity(concept_id, concept_type, properties, "medical")

            # Add medical relationships
            medical_relationships = [
                ("diabetes", "insulin", "treats"),
                ("diabetes", "glucose", "affects"),
                ("hypertension", "cardiovascular", "affects"),
                ("aspirin", "cardiovascular", "protects"),
                ("insulin", "glucose", "regulates"),
            ]

            for source, target, relation in medical_relationships:
                kg.add_relationship(source, target, relation)

            self.logger.info("Built medical ontology")
            return True

        except Exception as e:
            self.logger.error(f"Failed to build medical ontology: {e}")
            return False

    def build_finance_ontology(self, kg: KnowledgeGraph) -> bool:
        """
        Build finance domain ontology and entities

        Args:
            kg: Knowledge graph to populate

        Returns:
            Success status
        """
        try:
            # Add financial concepts
            finance_concepts = [
                ("diversification", "Strategy", {"description": "Spreading investments to reduce risk"}),
                ("portfolio", "Investment", {"description": "Collection of investment assets"}),
                ("risk", "Concept", {"description": "Potential for loss or gain"}),
                ("return", "Concept", {"description": "Financial gain from investment"}),
                ("volatility", "Measure", {"description": "Rate of price change"}),
                ("bonds", "Asset", {"description": "Fixed income securities"}),
                ("stocks", "Asset", {"description": "Equity securities"}),
                ("etf", "Asset", {"description": "Exchange-traded funds"}),
            ]

            for concept_id, concept_type, properties in finance_concepts:
                kg.add_entity(concept_id, concept_type, properties, "finance")

            # Add financial relationships
            finance_relationships = [
                ("diversification", "risk", "reduces"),
                ("portfolio", "diversification", "uses"),
                ("volatility", "risk", "increases"),
                ("stocks", "volatility", "has"),
                ("bonds", "volatility", "has"),
                ("etf", "diversification", "enables"),
                ("return", "risk", "correlates_with"),
            ]

            for source, target, relation in finance_relationships:
                kg.add_relationship(source, target, relation)

            self.logger.info("Built finance ontology")
            return True

        except Exception as e:
            self.logger.error(f"Failed to build finance ontology: {e}")
            return False

    def build_from_evidence_sources(self, kg: KnowledgeGraph, evidence_dir: str) -> bool:
        """
        Build knowledge graph from evidence sources

        Args:
            kg: Knowledge graph to populate
            evidence_dir: Directory containing evidence sources

        Returns:
            Success status
        """
        try:
            evidence_path = Path(evidence_dir)
            if not evidence_path.exists():
                self.logger.warning(f"Evidence directory not found: {evidence_dir}")
                return False

            # Process different types of evidence files
            for file_path in evidence_path.rglob("*"):
                if file_path.suffix.lower() in ['.json', '.csv', '.txt']:
                    self._process_evidence_file(kg, str(file_path))

            self.logger.info(f"Built knowledge graph from evidence sources: {evidence_dir}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to build from evidence sources: {e}")
            return False

    def _process_evidence_file(self, kg: KnowledgeGraph, file_path: str) -> None:
        """Process a single evidence file"""
        try:
            file_path_obj = Path(file_path)

            if file_path_obj.suffix.lower() == '.json':
                # Try to extract entities from JSON
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                if isinstance(data, dict) and "content" in data:
                    # Extract entities from content
                    entities = self._extract_entities_from_text(data["content"])
                    for entity in entities:
                        kg.add_entity(entity["id"], entity["type"],
                                    {"source": file_path}, "evidence")

            elif file_path_obj.suffix.lower() == '.txt':
                # Extract entities from text file
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                entities = self._extract_entities_from_text(content)
                for entity in entities:
                    kg.add_entity(entity["id"], entity["type"],
                                {"source": file_path}, "evidence")

        except Exception as e:
            self.logger.error(f"Failed to process evidence file {file_path}: {e}")

    def _extract_entities_from_text(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract entities from text using simple NLP

        This is a basic implementation. In production, use proper NER models.
        """
        entities = []

        # Simple keyword-based entity extraction
        medical_keywords = {
            "diabetes": "Disease",
            "cancer": "Disease",
            "heart": "Organ",
            "lung": "Organ",
            "blood": "Fluid",
            "insulin": "Medication",
            "aspirin": "Medication",
        }

        finance_keywords = {
            "stock": "Asset",
            "bond": "Asset",
            "portfolio": "Investment",
            "diversification": "Strategy",
            "risk": "Concept",
            "return": "Concept",
            "volatility": "Measure",
        }

        text_lower = text.lower()

        # Extract medical entities
        for keyword, entity_type in medical_keywords.items():
            if keyword in text_lower:
                entities.append({
                    "id": keyword,
                    "type": entity_type,
                    "domain": "medical"
                })

        # Extract finance entities
        for keyword, entity_type in finance_keywords.items():
            if keyword in text_lower:
                entities.append({
                    "id": keyword,
                    "type": entity_type,
                    "domain": "finance"
                })

        return entities

    def build_cross_domain_relationships(self, kg: KnowledgeGraph) -> bool:
        """
        Build relationships between medical and financial domains

        Args:
            kg: Knowledge graph to populate

        Returns:
            Success status
        """
        try:
            # Add cross-domain relationships
            cross_domain_rels = [
                ("diabetes", "portfolio", "affects_financially"),
                ("hypertension", "risk", "increases"),
                ("cardiovascular", "return", "impacts"),
                ("healthcare", "investment", "requires"),
            ]

            for source, target, relation in cross_domain_rels:
                kg.add_relationship(source, target, relation)

            self.logger.info("Built cross-domain relationships")
            return True

        except Exception as e:
            self.logger.error(f"Failed to build cross-domain relationships: {e}")
            return False

    def populate_from_datasets(self, kg: KnowledgeGraph, data_dir: str) -> bool:
        """
        Populate knowledge graph from FAIR-Agent datasets

        Args:
            kg: Knowledge graph to populate
            data_dir: Directory containing datasets

        Returns:
            Success status
        """
        try:
            data_path = Path(data_dir)
            if not data_path.exists():
                self.logger.warning(f"Data directory not found: {data_dir}")
                return False

            # Process different datasets
            dataset_dirs = ["medmcqa", "finqa", "pubmedqa", "tatqa"]

            for dataset in dataset_dirs:
                dataset_path = data_path / "datasets" / dataset
                if dataset_path.exists():
                    self._process_dataset(kg, str(dataset_path), dataset)

            self.logger.info(f"Populated knowledge graph from datasets: {data_dir}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to populate from datasets: {e}")
            return False

    def _process_dataset(self, kg: KnowledgeGraph, dataset_path: str, dataset_name: str) -> None:
        """Process a specific dataset"""
        try:
            # This is a simplified implementation
            # In production, you'd have specific parsers for each dataset format

            for file_path in Path(dataset_path).rglob("*.jsonl"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())

                            # Extract question and answer as entities
                            question_id = f"q_{dataset_name}_{data.get('id', 'unknown')}"
                            kg.add_entity(question_id, "Question",
                                        {"text": data.get('question', ''),
                                         "dataset": dataset_name}, "evidence")

                            answer_id = f"a_{dataset_name}_{data.get('id', 'unknown')}"
                            kg.add_entity(answer_id, "Answer",
                                        {"text": data.get('answer', ''),
                                         "dataset": dataset_name}, "evidence")

                            # Link question to answer
                            kg.add_relationship(question_id, answer_id, "has_answer")

                        except json.JSONDecodeError:
                            continue

        except Exception as e:
            self.logger.error(f"Failed to process dataset {dataset_name}: {e}")