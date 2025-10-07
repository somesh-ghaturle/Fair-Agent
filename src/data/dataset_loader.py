"""
Dataset Loader Module for FAIR-Agent

Loads datasets from config.yaml for training and evaluation purposes.
Supports HuggingFace datasets and local file paths.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import json

logger = logging.getLogger(__name__)


@dataclass
class DatasetInfo:
    """Information about a dataset"""
    name: str
    source: str
    local_path: str
    preprocessing_required: bool
    access_required: bool = False
    domain: str = "general"
    description: str = ""
    loaded: bool = False


class DatasetLoader:
    """Loads and manages datasets from configuration"""
    
    def __init__(self, config_path: str = "./config/config.yaml"):
        self.config_path = Path(config_path)
        self.datasets: Dict[str, List[DatasetInfo]] = {
            'finance': [],
            'medical': []
        }
        self._load_dataset_configs()
    
    def _load_dataset_configs(self):
        """Load dataset configurations from YAML file"""
        
        if not self.config_path.exists():
            logger.warning(f"Config file {self.config_path} not found")
            return
        
        try:
            with open(self.config_path, 'r') as f:
                config = yaml.safe_load(f)
            
            datasets_config = config.get('datasets', {})
            
            # Load finance datasets
            if 'finance' in datasets_config:
                for dataset_data in datasets_config['finance']:
                    dataset_info = DatasetInfo(
                        name=dataset_data['name'],
                        source=dataset_data['source'],
                        local_path=dataset_data['local_path'],
                        preprocessing_required=dataset_data.get('preprocessing_required', False),
                        access_required=dataset_data.get('access_required', False),
                        domain='finance',
                        description=self._get_dataset_description(dataset_data['name'])
                    )
                    self.datasets['finance'].append(dataset_info)
            
            # Load medical datasets
            if 'medical' in datasets_config:
                for dataset_data in datasets_config['medical']:
                    dataset_info = DatasetInfo(
                        name=dataset_data['name'],
                        source=dataset_data['source'],
                        local_path=dataset_data['local_path'],
                        preprocessing_required=dataset_data.get('preprocessing_required', False),
                        access_required=dataset_data.get('access_required', False),
                        domain='medical',
                        description=self._get_dataset_description(dataset_data['name'])
                    )
                    self.datasets['medical'].append(dataset_info)
            
            total_count = len(self.datasets['finance']) + len(self.datasets['medical'])
            logger.info(f"✅ Loaded {total_count} dataset configurations")
            logger.info(f"   Finance: {len(self.datasets['finance'])} datasets")
            logger.info(f"   Medical: {len(self.datasets['medical'])} datasets")
            
        except Exception as e:
            logger.error(f"Error loading dataset configs: {e}")
    
    def _get_dataset_description(self, dataset_name: str) -> str:
        """Get description for known datasets"""
        descriptions = {
            'finqa': 'Financial Question Answering dataset with numerical reasoning',
            'tatqa': 'Tabular and Textual dataset for question answering in finance',
            'convfinqa': 'Conversational Financial QA dataset',
            'mimiciv': 'Medical Information Mart for Intensive Care IV - Clinical database',
            'pubmedqa': 'Biomedical Question Answering dataset from PubMed abstracts',
            'medmcqa': 'Medical Multiple Choice Question Answering dataset'
        }
        return descriptions.get(dataset_name, 'Dataset for domain-specific training')
    
    def get_datasets_by_domain(self, domain: str) -> List[DatasetInfo]:
        """Get all datasets for a specific domain"""
        return self.datasets.get(domain, [])
    
    def get_all_datasets(self) -> Dict[str, List[DatasetInfo]]:
        """Get all available datasets"""
        return self.datasets
    
    def get_dataset_info(self, domain: str, dataset_name: str) -> Optional[DatasetInfo]:
        """Get information about a specific dataset"""
        for dataset in self.datasets.get(domain, []):
            if dataset.name == dataset_name:
                return dataset
        return None
    
    def check_dataset_availability(self, domain: str, dataset_name: str) -> Dict[str, Any]:
        """Check if a dataset is available locally"""
        dataset = self.get_dataset_info(domain, dataset_name)
        
        if not dataset:
            return {
                'available': False,
                'reason': 'Dataset not found in configuration'
            }
        
        local_path = Path(dataset.local_path)
        
        if local_path.exists():
            # Check if path contains data
            files = list(local_path.glob('*'))
            return {
                'available': True,
                'location': str(local_path),
                'file_count': len(files),
                'requires_download': False
            }
        else:
            return {
                'available': False,
                'location': str(local_path),
                'requires_download': True,
                'source': dataset.source,
                'access_required': dataset.access_required
            }
    
    def load_dataset_samples(self, domain: str, dataset_name: str, max_samples: int = 100) -> List[Dict[str, str]]:
        """Load sample data from a dataset"""
        dataset = self.get_dataset_info(domain, dataset_name)
        
        if not dataset:
            logger.warning(f"Dataset {dataset_name} not found for domain {domain}")
            return []
        
        local_path = Path(dataset.local_path)
        samples = []
        
        # Try to load from HuggingFace datasets format first
        if local_path.exists():
            try:
                # Try loading as HuggingFace dataset (saved with save_to_disk)
                from datasets import load_from_disk
                
                logger.info(f"[DATASET] Loading {dataset_name} from {local_path}")
                hf_dataset = load_from_disk(str(local_path))
                
                # Process based on dataset type
                for i, item in enumerate(hf_dataset):
                    if i >= max_samples:
                        break
                    
                    # Format based on dataset
                    if dataset_name == 'pubmedqa':
                        # PubMedQA format: question, context, long_answer, final_decision
                        sample = {
                            'question': item.get('question', ''),
                            'answer': item.get('long_answer', item.get('final_decision', '')),
                            'context': str(item.get('context', {}))[:500] if item.get('context') else ''
                        }
                        samples.append(sample)
                    
                    elif dataset_name in ['finqa', 'tatqa', 'convfinqa']:
                        # Finance datasets - adapt format
                        sample = {
                            'question': item.get('question', item.get('text', '')),
                            'answer': item.get('answer', item.get('exe_ans', item.get('label', ''))),
                            'context': str(item.get('pre_text', item.get('table', '')))[:500] if 'pre_text' in item or 'table' in item else ''
                        }
                        samples.append(sample)
                    
                    elif dataset_name == 'medmcqa':
                        # MedMCQA format
                        sample = {
                            'question': item.get('question', ''),
                            'answer': item.get('cop', item.get('exp', '')),
                            'context': ''
                        }
                        samples.append(sample)
                    
                    else:
                        # Generic format - try to extract question/answer
                        sample = {
                            'question': item.get('question', item.get('text', str(item)[:200])),
                            'answer': item.get('answer', item.get('label', item.get('response', ''))),
                            'context': item.get('context', '')
                        }
                        samples.append(sample)
                
                logger.info(f"[DATASET] ✅ Loaded {len(samples)} samples from {dataset_name}")
                return samples
                
            except ImportError:
                logger.warning(f"[DATASET] HuggingFace datasets library not available")
            except Exception as e:
                logger.warning(f"[DATASET] Could not load HuggingFace dataset: {e}")
            
            # Fallback: Try to load from JSON files
            json_files = list(local_path.glob('*.json')) + list(local_path.glob('*.jsonl'))
            
            for json_file in json_files[:1]:  # Load from first file only
                try:
                    if json_file.suffix == '.jsonl':
                        # Load JSONL (one JSON object per line)
                        with open(json_file, 'r') as f:
                            for i, line in enumerate(f):
                                if i >= max_samples:
                                    break
                                samples.append(json.loads(line))
                    else:
                        # Load regular JSON
                        with open(json_file, 'r') as f:
                            data = json.load(f)
                            if isinstance(data, list):
                                samples = data[:max_samples]
                            elif isinstance(data, dict):
                                samples = [data]
                    
                    logger.info(f"[DATASET] Loaded {len(samples)} samples from {dataset_name} (JSON)")
                    break
                    
                except Exception as e:
                    logger.error(f"[DATASET] Error loading {json_file}: {e}")
        
        return samples
    
    def get_dataset_stats(self) -> Dict[str, Any]:
        """Get statistics about available datasets"""
        stats = {
            'total_datasets': 0,
            'by_domain': {},
            'available_locally': 0,
            'requires_download': 0,
            'requires_access': 0
        }
        
        for domain, datasets in self.datasets.items():
            stats['total_datasets'] += len(datasets)
            stats['by_domain'][domain] = len(datasets)
            
            for dataset in datasets:
                availability = self.check_dataset_availability(domain, dataset.name)
                
                if availability['available']:
                    stats['available_locally'] += 1
                else:
                    stats['requires_download'] += 1
                
                if dataset.access_required:
                    stats['requires_access'] += 1
        
        return stats
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert dataset information to dictionary"""
        result = {}
        
        for domain, datasets in self.datasets.items():
            result[domain] = []
            for dataset in datasets:
                result[domain].append({
                    'name': dataset.name,
                    'source': dataset.source,
                    'local_path': dataset.local_path,
                    'description': dataset.description,
                    'preprocessing_required': dataset.preprocessing_required,
                    'access_required': dataset.access_required,
                    'domain': dataset.domain,
                    'availability': self.check_dataset_availability(domain, dataset.name)
                })
        
        return result


# Global dataset loader instance
_dataset_loader = None

def get_dataset_loader(config_path: str = "./config/config.yaml") -> DatasetLoader:
    """Get or create global dataset loader instance"""
    global _dataset_loader
    
    if _dataset_loader is None:
        _dataset_loader = DatasetLoader(config_path)
    
    return _dataset_loader
