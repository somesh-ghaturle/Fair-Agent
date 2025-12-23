import os
import json
import logging
import requests
import zipfile
import io
from pathlib import Path
from datasets import load_dataset

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "datasets"

def save_to_jsonl(data, output_path, limit=None):
    """Save a list of dictionaries to a JSONL file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        count = 0
        for item in data:
            if limit and count >= limit:
                break
            f.write(json.dumps(item) + '\n')
            count += 1
    logger.info(f"Saved {count} records to {output_path}")

def download_finqa():
    logger.info("Downloading FinQA...")
    url = "https://raw.githubusercontent.com/czyssrs/FinQA/master/dataset/train.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        processed = []
        for item in data:
            if 'qa' in item:
                q = item['qa']['question']
                a = item['qa']['answer']
                context = " ".join(item.get('pre_text', []) + item.get('post_text', []))
                processed.append({"question": q, "answer": str(a), "context": context})
        
        save_to_jsonl(processed, DATA_DIR / "finqa" / "finance_qa.jsonl")
    except Exception as e:
        logger.error(f"Failed to download FinQA: {e}")

def download_convfinqa():
    logger.info("Downloading ConvFinQA...")
    url = "https://github.com/czyssrs/ConvFinQA/raw/main/data.zip"
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            # Extract train.json
            # The zip contains a 'data' folder
            with z.open('data/train.json') as f:
                data = json.load(f)
                
        processed = []
        for item in data:
            # Try to extract QA pairs
            if 'qa' in item:
                processed.append({
                    "question": item['qa']['question'],
                    "answer": str(item['qa']['answer']),
                    "context": "ConvFinQA Context"
                })
            elif 'annotation' in item and 'dialogue' in item['annotation']:
                # Fallback: use dialogue
                dialogue = item['annotation']['dialogue']
                processed.append({
                    "question": "Conversational Finance Dialogue",
                    "answer": "\n".join(dialogue),
                    "context": "ConvFinQA Dialogue"
                })

        save_to_jsonl(processed, DATA_DIR / "convfinqa" / "convfinqa.jsonl")
    except Exception as e:
        logger.error(f"Failed to download ConvFinQA: {e}")

def download_tatqa():
    logger.info("Downloading TAT-QA...")
    url = "https://raw.githubusercontent.com/NExTplusplus/TAT-QA/master/dataset_raw/tatqa_dataset_train.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        processed = []
        for item in data:
            if 'questions' in item:
                for q_obj in item['questions']:
                    if 'question' in q_obj and 'answer' in q_obj:
                        processed.append({
                            "question": q_obj['question'],
                            "answer": str(q_obj['answer']),
                            "context": "TAT-QA Table/Text"
                        })
        
        save_to_jsonl(processed, DATA_DIR / "tatqa" / "tatqa.jsonl")
    except Exception as e:
        logger.error(f"Failed to download TAT-QA: {e}")

def download_medmcqa():
    logger.info("Downloading MedMCQA (via HuggingFace)...")
    try:
        dataset = load_dataset("medmcqa", split="train", trust_remote_code=True)
        processed = []
        for item in dataset:
            ans = item.get('exp')
            if not ans:
                ans = str(item.get('cop'))
            
            processed.append({
                "question": item['question'],
                "answer": str(ans),
                "context": item.get('subject_name', 'Medical')
            })
        
        save_to_jsonl(processed, DATA_DIR / "medmcqa" / "medical_qa.jsonl")
    except Exception as e:
        logger.error(f"Failed to download MedMCQA: {e}")

def download_pubmedqa():
    logger.info("Downloading PubMedQA (via HuggingFace)...")
    try:
        dataset = load_dataset("pubmed_qa", "pqa_labeled", split="train", trust_remote_code=True)
        processed = []
        for item in dataset:
            processed.append({
                "question": item['question'],
                "answer": item['long_answer'],
                "context": "\n".join(item['context']['contexts'])
            })
        
        save_to_jsonl(processed, DATA_DIR / "pubmedqa" / "medical_qa.jsonl")
    except Exception as e:
        logger.error(f"Failed to download PubMedQA: {e}")

if __name__ == "__main__":
    download_finqa()
    download_convfinqa()
    download_tatqa()
    download_medmcqa()
    download_pubmedqa()
