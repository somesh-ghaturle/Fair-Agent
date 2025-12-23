"""
Verification script for FAIR-Agent Memory Systems
Tests ChromaDB (Vector Store) and NetworkX (Knowledge Graph) integration.
"""

import sys
import os
from pathlib import Path
import logging

# Setup path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def test_vector_store():
    print("\n🔍 Testing Vector Store (ChromaDB)...")
    try:
        from src.memory.vector_store import VectorStore
        vs = VectorStore()
        
        if not vs.client:
            print("❌ Vector Store client failed to initialize.")
            return False

        # Test Data
        test_id = "test_trace_001"
        test_query = "How does inflation affect bond prices?"
        test_response = "Inflation generally causes bond prices to fall."
        metadata = {"domain": "finance", "test": "true"}

        # 1. Add Trace
        print("   Adding test trace...")
        vs.add_trace(test_query, test_response, metadata)

        # 2. Search Trace
        print("   Searching for similar traces...")
        results = vs.find_similar_traces("inflation bond prices")
        
        found = False
        for res in results:
            if "Inflation generally causes" in res['content']:
                found = True
                print(f"   ✅ Found trace: {res['content'][:50]}...")
                break
        
        if found:
            print("✅ Vector Store Read/Write Test PASSED")
            return True
        else:
            print("❌ Vector Store Search failed to find inserted document.")
            return False

    except ImportError:
        print("❌ Could not import VectorStore. Check dependencies (chromadb).")
        return False
    except Exception as e:
        print(f"❌ Vector Store Test Error: {e}")
        return False

def test_knowledge_graph():
    print("\n🔍 Testing Knowledge Graph (NetworkX)...")
    try:
        from src.memory.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph()

        # Test Data
        entity1 = "Inflation"
        entity2 = "Purchasing Power"
        relation = "decreases"

        # 1. Add Relation
        print(f"   Adding relation: {entity1} --[{relation}]--> {entity2}")
        kg.add_relation(entity1, entity2, relation)

        # 2. Search/Retrieve
        print(f"   Retrieving related entities for '{entity1}'...")
        related = kg.get_related_entities(entity1)
        
        found = False
        for item in related:
            if item['entity'] == entity2 and item['relation'] == relation:
                found = True
                print(f"   ✅ Found relation: {item['relation']} {item['entity']}")
                break
        
        if found:
            print("✅ Knowledge Graph Read/Write Test PASSED")
            return True
        else:
            print("❌ Knowledge Graph failed to retrieve inserted relation.")
            return False

    except ImportError:
        print("❌ Could not import KnowledgeGraph. Check dependencies (networkx).")
        return False
    except Exception as e:
        print(f"❌ Knowledge Graph Test Error: {e}")
        return False

if __name__ == "__main__":
    print("=== FAIR-Agent Memory Verification ===")
    
    vs_status = test_vector_store()
    kg_status = test_knowledge_graph()
    
    print("\n=== Summary ===")
    print(f"Vector Store:   {'✅ WORKING' if vs_status else '❌ FAILED'}")
    print(f"Knowledge Graph:{'✅ WORKING' if kg_status else '❌ FAILED'}")
