"""
Vector Store Implementation using ChromaDB
Stores evidence embeddings and execution traces for semantic retrieval.
"""

import logging
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
import os
from pathlib import Path
import json

logger = logging.getLogger(__name__)

class VectorStore:
    def __init__(self, persist_directory: str = None):
        if persist_directory:
            self.persist_directory = persist_directory
        else:
            # Default to data/vector_store
            root_dir = Path(__file__).resolve().parent.parent.parent
            self.persist_directory = str(root_dir / "data" / "vector_store")
            
        os.makedirs(self.persist_directory, exist_ok=True)
        
        try:
            self.client = chromadb.PersistentClient(path=self.persist_directory)
            logger.info(f"✅ ChromaDB initialized at {self.persist_directory}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize ChromaDB: {e}")
            self.client = None

        # Initialize collections
        self.evidence_collection = self._get_or_create_collection("evidence")
        self.trace_collection = self._get_or_create_collection("traces")
        self.telemetry_collection = self._get_or_create_collection("telemetry")

    def _get_or_create_collection(self, name: str):
        if not self.client:
            return None
        try:
            return self.client.get_or_create_collection(name=name)
        except Exception as e:
            logger.error(f"Failed to get/create collection {name}: {e}")
            return None

    def add_evidence(self, documents: List[str], metadatas: List[Dict], ids: List[str], embeddings: Optional[List[List[float]]] = None):
        """Add evidence documents to the vector store"""
        if not self.evidence_collection:
            return
        
        try:
            self.evidence_collection.add(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
                embeddings=embeddings
            )
            logger.debug(f"Added {len(documents)} documents to evidence collection")
        except Exception as e:
            logger.error(f"Error adding evidence: {e}")

    def query_evidence(self, query_texts: List[str], n_results: int = 5) -> Dict:
        """Query the evidence collection"""
        if not self.evidence_collection:
            return {"documents": [], "metadatas": [], "distances": []}
            
        try:
            return self.evidence_collection.query(
                query_texts=query_texts,
                n_results=n_results
            )
        except Exception as e:
            logger.error(f"Error querying evidence: {e}")
            return {"documents": [], "metadatas": [], "distances": []}

    def add_trace(self, query: str, response: str, metadata: Dict):
        """Add a semantic trace (query/response pair) to the vector store for conversation history"""
        if not self.trace_collection:
            return
            
        try:
            # Combine query and response for the document content
            document = f"Query: {query}\nResponse: {response}"
            
            # Generate a unique ID if not provided
            trace_id = metadata.get("trace_id", str(hash(document)))
            
            self.trace_collection.add(
                documents=[document],
                metadatas=[metadata],
                ids=[trace_id]
            )
            logger.info(f"Added semantic trace {trace_id} to vector store")
        except Exception as e:
            logger.error(f"Error adding semantic trace: {e}")

    def add_telemetry(self, trace_data: Dict):
        """Add an operational telemetry trace to the vector store"""
        if not self.telemetry_collection:
            return

        try:
            # Create a text representation of the telemetry for embedding
            # We focus on status, duration, and any error messages
            status = trace_data.get("status", "unknown")
            duration = trace_data.get("duration_ms", 0)
            trace_id = trace_data.get("trace_id", "unknown")
            domain = trace_data.get("domain", "unknown")
            
            document = f"Trace ID: {trace_id}\nStatus: {status}\nDuration: {duration}ms\nDomain: {domain}"
            
            # Add error info if present
            if status == "error":
                document += f"\nError: {trace_data.get('error', 'Unknown error')}"
            
            self.telemetry_collection.add(
                documents=[document],
                metadatas=[trace_data],
                ids=[trace_id]
            )
            logger.debug(f"Added telemetry trace {trace_id} to vector store")
        except Exception as e:
            logger.error(f"Error adding telemetry: {e}")

    def find_similar_traces(self, query: str, n_results: int = 3) -> List[Dict]:
        """Find similar past traces for a given query"""
        if not self.trace_collection:
            return []
            
        try:
            results = self.trace_collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            traces = []
            if results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    traces.append({
                        'content': doc,
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else 0
                    })
            return traces
        except Exception as e:
            logger.error(f"Error querying traces: {e}")
            return []
