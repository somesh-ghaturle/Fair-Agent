#!/usr/bin/env python3
"""
Knowledge Graph Demo Script

Demonstrates the knowledge graph capabilities integrated with FAIR-Agent.
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.knowledge_graph import KnowledgeGraph, GraphBuilder, KnowledgeGraphReasoner
from src.agents.orchestrator import Orchestrator


def demo_basic_knowledge_graph():
    """Demonstrate basic knowledge graph functionality"""
    print("🔍 FAIR-Agent Knowledge Graph Demo")
    print("=" * 50)

    # Create knowledge graph
    kg = KnowledgeGraph(name="demo_kg")

    # Create graph builder
    builder = GraphBuilder()

    # Build domain ontologies
    print("🏗️ Building domain ontologies...")
    builder.build_medical_ontology(kg)
    builder.build_finance_ontology(kg)
    builder.build_cross_domain_relationships(kg)

    # Display statistics
    stats = kg.get_statistics()
    print(f"📊 Knowledge Graph Statistics:")
    print(f"   RDF Triples: {stats['rdf_triples']}")
    print(f"   Network Nodes: {stats['network_nodes']}")
    print(f"   Network Edges: {stats['network_edges']}")
    print(f"   Domains: {', '.join(stats['domains'])}")
    print()

    # Demonstrate entity queries
    print("🔎 Querying entities...")
    medical_entities = kg.query_entities(domain="medical")
    finance_entities = kg.query_entities(domain="finance")

    print(f"Medical entities found: {len(medical_entities)}")
    print(f"Finance entities found: {len(finance_entities)}")
    print()

    # Demonstrate relationship finding
    print("🔗 Finding relationships...")
    diabetes_relations = kg.find_related_entities("diabetes")
    portfolio_relations = kg.find_related_entities("portfolio")

    print(f"Diabetes relationships: {diabetes_relations}")
    print(f"Portfolio relationships: {portfolio_relations}")
    print()

    # Create reasoner and demonstrate reasoning
    print("🧠 Knowledge Graph Reasoning...")
    reasoner = KnowledgeGraphReasoner()

    # Find paths between concepts
    paths = reasoner.find_paths(kg, "diabetes", "insulin", max_length=3)
    print(f"Paths from diabetes to insulin: {len(paths)} found")

    # Calculate centrality
    centrality = reasoner.calculate_centrality(kg)
    if centrality:
        top_entities = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
        print("Top 5 most central entities:")
        for entity, score in top_entities:
            print(".3f")
    print()

    return kg


def demo_integrated_orchestrator():
    """Demonstrate knowledge graph integration with orchestrator"""
    print("🎯 FAIR-Agent Orchestrator with Knowledge Graph")
    print("=" * 50)

    try:
        # Initialize orchestrator with knowledge graph enabled
        orchestrator = Orchestrator(enable_knowledge_graph=True)

        # Test queries
        test_queries = [
            "What is diabetes and how is it treated?",
            "How does portfolio diversification work?",
            "What are the financial impacts of chronic illness?"
        ]

        for query in test_queries:
            print(f"\n❓ Query: {query}")
            print("-" * 40)

            result = orchestrator.process_query(query)

            print(f"📋 Domain: {result.domain.value}")
            print(".2f")
            print(f"📝 Answer: {result.primary_answer[:200]}...")
            print(f"🔧 Routing: {result.routing_explanation}")

    except Exception as e:
        print(f"❌ Error in orchestrator demo: {e}")


def demo_advanced_reasoning():
    """Demonstrate advanced reasoning capabilities"""
    print("🚀 Advanced Knowledge Graph Reasoning")
    print("=" * 50)

    # Create and populate knowledge graph
    kg = KnowledgeGraph(name="advanced_kg")
    builder = GraphBuilder()
    builder.build_medical_ontology(kg)
    builder.build_finance_ontology(kg)

    reasoner = KnowledgeGraphReasoner()

    # Demonstrate community detection
    print("🏘️ Detecting communities...")
    communities = reasoner.detect_communities(kg)
    print(f"Found {len(communities)} communities")

    for i, community in enumerate(communities[:3]):  # Show first 3
        print(f"  Community {i+1}: {community}")

    print()

    # Demonstrate relationship explanation
    print("💡 Explaining relationships...")
    explanation = reasoner.explain_relationship("diabetes", "insulin")
    print(f"Relationship explanation: {explanation.get('explanation', 'N/A')}")

    print()

    # Demonstrate fact validation
    print("✅ Validating facts...")
    facts_to_validate = [
        {"source": "diabetes", "target": "insulin", "relation": "treats"},
        {"source": "portfolio", "target": "risk", "relation": "reduces"},
        {"source": "diabetes", "target": "portfolio", "relation": "affects_financially"}
    ]

    validation_results = reasoner.validate_facts(kg, facts_to_validate)
    for result in validation_results:
        fact = result["fact"]
        is_valid = result["is_valid"]
        confidence = result["confidence"]
        print(".2f")

    print()

    # Show reasoning statistics
    print("📈 Reasoning Statistics...")
    stats = reasoner.get_reasoning_statistics(kg)
    for key, value in stats.items():
        if isinstance(value, float):
            print(".3f")
        else:
            print(f"   {key}: {value}")


def main():
    """Main demo function"""
    print("🧠 FAIR-Agent Knowledge Graph Implementation")
    print("=" * 60)
    print()

    try:
        # Basic knowledge graph demo
        kg = demo_basic_knowledge_graph()

        # Integrated orchestrator demo
        demo_integrated_orchestrator()

        # Advanced reasoning demo
        demo_advanced_reasoning()

        print("\n✅ Knowledge Graph Demo Completed Successfully!")
        print("\n💡 Key Features Implemented:")
        print("   • Multi-modal knowledge representation (RDF + NetworkX)")
        print("   • Domain-specific ontologies (Medical & Finance)")
        print("   • Graph reasoning and inference")
        print("   • Integration with FAIR-Agent orchestrator")
        print("   • Path finding and relationship discovery")
        print("   • Community detection and centrality analysis")
        print("   • Fact validation and explanation")

    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()