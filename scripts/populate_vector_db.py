import os
import json
import logging
import sys
from pathlib import Path
from typing import List, Dict
import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.memory.vector_store import VectorStore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATASETS_DIR = PROJECT_ROOT / "data" / "datasets"

def load_jsonl(path: Path) -> List[Dict]:
    data = []
    if not path.exists():
        logger.warning(f"File not found: {path}")
        return data
    
    with open(path, 'r') as f:
        for line in f:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return data

def populate_db():
    logger.info("Initializing Vector Store...")
    vector_store = VectorStore()
    if not vector_store.client:
        logger.error("Failed to initialize Vector Store.")
        return

    logger.info("Loading embedding model...")
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Define datasets to load
    datasets = [
        {
            "name": "FinQA",
            "path": DATASETS_DIR / "finqa" / "finance_qa.jsonl",
            "prefix": "dataset_finqa",
            "domain": "finance",
            "type": "qa_dataset"
        },
        {
            "name": "MedMCQA",
            "path": DATASETS_DIR / "medmcqa" / "medical_qa.jsonl",
            "prefix": "dataset_medmcqa",
            "domain": "medical",
            "type": "qa_dataset"
        },
        {
            "name": "PubMedQA",
            "path": DATASETS_DIR / "pubmedqa" / "medical_qa.jsonl",
            "prefix": "dataset_pubmed",
            "domain": "medical",
            "type": "qa_dataset"
        },
        {
            "name": "ConvFinQA",
            "path": DATASETS_DIR / "convfinqa" / "convfinqa.jsonl",
            "prefix": "dataset_convfin",
            "domain": "finance",
            "type": "qa_dataset"
        },
        {
            "name": "TAT-QA",
            "path": DATASETS_DIR / "tatqa" / "tatqa.jsonl",
            "prefix": "dataset_tatqa",
            "domain": "finance",
            "type": "qa_dataset"
        }
        # Add others if they exist
    ]

    total_added = 0

    for ds in datasets:
        logger.info(f"Processing {ds['name']}...")
        records = load_jsonl(ds['path'])
        logger.info(f"Loaded {len(records)} records from {ds['name']}")
        
        if not records:
            continue

        # Prepare batches
        batch_size = 100
        
        # Check which IDs already exist to skip
        # Generating IDs first
        all_ids = [f"{ds['prefix']}_{i:04d}" for i in range(len(records))]
        
        # We can't easily check 180k IDs at once in some versions of Chroma, but let's try get
        # Or just upsert (add handles updates usually, but might be slower)
        # Let's just process in batches and add. Chroma handles duplicates by updating or erroring depending on method.
        # vector_store.add_evidence uses collection.add which might error on duplicates.
        # We should check if we can use upsert.
        
        # Let's look at vector_store.add_evidence implementation
        # It calls self.evidence_collection.add
        # We should probably modify VectorStore to use upsert or check existence, 
        # but for this script we can just use the collection directly if needed.
        
        collection = vector_store.evidence_collection
        
        for i in tqdm(range(0, len(records), batch_size), desc=f"Embedding {ds['name']}"):
            batch_records = records[i:i+batch_size]
            batch_ids = all_ids[i:i+batch_size]
            
            # Check existence (optimization)
            existing = collection.get(ids=batch_ids, include=[])
            existing_ids = set(existing['ids'])
            
            # Filter out existing
            new_records = []
            new_ids = []
            for rec, rid in zip(batch_records, batch_ids):
                if rid not in existing_ids:
                    new_records.append(rec)
                    new_ids.append(rid)
            
            if not new_records:
                continue
                
            # Prepare text and metadata
            texts = [f"{ds['name']}: {r['question']}\nAnswer: {r['answer']}" for r in new_records]
            metadatas = [{
                "id": rid,
                "title": f"{ds['name']} Q&A",
                "source_type": ds['type'],
                "domain": ds['domain'],
                "is_curated": False
            } for rid in new_ids]
            
            # Compute embeddings
            embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            
            # Add to Chroma
            collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=new_ids,
                embeddings=[e.tolist() for e in embeddings]
            )
            
            total_added += len(new_records)

    logger.info(f"Population complete. Added {total_added} new documents to Vector Store.")

if __name__ == "__main__":
    populate_db()
