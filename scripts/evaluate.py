#!/usr/bin/env python3#!/usr/bin/env python3

""""""

FAIR-Agent System Evaluation ScriptComprehensive Evaluation Script for FAIR-Agent System



Comprehensive evaluation of the FAIR-Agent system including:This script runs complete evaluation of the FAIR-Agent system including:

- Domain classification accuracy- Faithfulness evaluation

- FAIR metrics evaluation  - Calibration assessment  

- Agent performance testing- Robustness testing

- System benchmarking- Safety analysis

- Interpretability scoring

CS668 Analytics Capstone - Fall 2025

"""Usage:

    python scripts/evaluate.py [--config config.yaml] [--output results/]

import os"""

import sys

import jsonimport os

import loggingimport sys

import argparseimport yaml

from pathlib import Pathimport json

from datetime import datetimeimport logging

from typing import Dict, List, Anyimport argparse

from pathlib import Path

# Add project root to pathfrom typing import Dict, List, Optional

project_root = Path(__file__).parent.parentfrom datetime import datetime

sys.path.insert(0, str(project_root))

# Add src to path for imports

from src.core.system import FairAgentSystemsys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.core.config import SystemConfig

from src.utils.logger import setup_loggingfrom agents import Orchestrator

from evaluation import (

    FaithfulnessEvaluator, CalibrationEvaluator, RobustnessEvaluator,

class SystemEvaluator:    SafetyEvaluator, InterpretabilityEvaluator

    """Evaluates the FAIR-Agent system performance""")

    

    def __init__(self, config_path: str = None):# Setup logging

        """Initialize the evaluator"""logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger(__name__)logger = logging.getLogger(__name__)

        self.system = FairAgentSystem(config_path)

        class FAIREvaluationSuite:

        # Test queries for evaluation    """Comprehensive evaluation suite for FAIR-Agent"""

        self.test_queries = {    

            'medical': [    def __init__(self, config_path: str = "./config/config.yaml"):

                "What are the symptoms of diabetes?",        """Initialize evaluation suite"""

                "How is hypertension treated?",        self.config = self._load_config(config_path)

                "What are the side effects of aspirin?",        self.orchestrator = None

                "Explain the causes of heart disease",        self.evaluators = {}

                "What is the treatment for pneumonia?"        

            ],        # Initialize system and evaluators

            'finance': [        self._initialize_system()

                "How do I analyze stock market trends?",        self._initialize_evaluators()

                "What factors affect mortgage rates?",    

                "Explain portfolio diversification strategies",    def _load_config(self, config_path: str) -> Dict:

                "What are the risks of cryptocurrency investment?",        """Load configuration"""

                "How do I calculate return on investment?"        try:

            ],            with open(config_path, 'r') as f:

            'cross_domain': [                return yaml.safe_load(f)

                "What are the financial implications of healthcare costs?",        except FileNotFoundError:

                "How do pharmaceutical investments perform?",            logger.error(f"Config file not found: {config_path}")

                "What is the economic impact of medical research?"            return self._get_default_config()

            ],    

            'general': [    def _get_default_config(self) -> Dict:

                "What is machine learning?",        """Get default configuration"""

                "Explain artificial intelligence",        return {

                "How does natural language processing work?"            'models': {

            ]                'finance': {'name': 'gpt2'},

        }                'medical': {'name': 'gpt2'}

                },

    def evaluate_domain_classification(self) -> Dict[str, float]:            'evaluation': {

        """Evaluate domain classification accuracy"""                'metrics': ['faithfulness', 'calibration', 'robustness', 'safety', 'interpretability']

        self.logger.info("Evaluating domain classification...")            }

                }

        total_queries = 0    

        correct_classifications = 0    def _initialize_system(self):

        results = {}        """Initialize the FAIR-Agent system"""

                try:

        for expected_domain, queries in self.test_queries.items():            finance_config = self.config.get('models', {}).get('finance', {})

            domain_correct = 0            medical_config = self.config.get('models', {}).get('medical', {})

                        

            for query in queries:            self.orchestrator = Orchestrator(

                result = self.system.process_query(query)                finance_config=finance_config,

                predicted_domain = result['domain']                medical_config=medical_config

                            )

                total_queries += 1            

                            logger.info("FAIR-Agent system initialized for evaluation")

                # Check if classification is correct            

                if (expected_domain == predicted_domain or         except Exception as e:

                    (expected_domain == 'general' and predicted_domain == 'unknown')):            logger.error(f"Failed to initialize system: {e}")

                    correct_classifications += 1            raise

                    domain_correct += 1    

                    def _initialize_evaluators(self):

                self.logger.debug(f"Query: {query}")        """Initialize all evaluation metrics"""

                self.logger.debug(f"Expected: {expected_domain}, Got: {predicted_domain}")        try:

                        safety_config_path = self.config.get('evaluation', {}).get('safety', {}).get('safety_keywords_file')

            domain_accuracy = domain_correct / len(queries)            

            results[f"{expected_domain}_accuracy"] = domain_accuracy            self.evaluators = {

            self.logger.info(f"{expected_domain.title()} domain accuracy: {domain_accuracy:.2%}")                'faithfulness': FaithfulnessEvaluator(),

                        'calibration': CalibrationEvaluator(),

        overall_accuracy = correct_classifications / total_queries                'robustness': RobustnessEvaluator(),

        results['overall_accuracy'] = overall_accuracy                'safety': SafetyEvaluator(safety_config_path),

        self.logger.info(f"Overall classification accuracy: {overall_accuracy:.2%}")                'interpretability': InterpretabilityEvaluator()

                    }

        return results            

                logger.info("All evaluators initialized successfully")

    def evaluate_response_quality(self) -> Dict[str, float]:            

        """Evaluate response quality metrics"""        except Exception as e:

        self.logger.info("Evaluating response quality...")            logger.error(f"Failed to initialize evaluators: {e}")

                    raise

        total_confidence = 0    

        total_queries = 0    def run_comprehensive_evaluation(

        response_lengths = []        self,

                test_queries: List[str],

        for domain, queries in self.test_queries.items():        ground_truths: List[str],

            for query in queries:        domains: List[str],

                result = self.system.process_query(query)        output_dir: str = "./results"

                    ) -> Dict:

                total_confidence += result.get('confidence', 0)        """

                total_queries += 1        Run comprehensive evaluation on test data

                response_lengths.append(len(result.get('answer', '')))        

                Args:

        avg_confidence = total_confidence / total_queries if total_queries > 0 else 0            test_queries: List of test queries

        avg_length = sum(response_lengths) / len(response_lengths) if response_lengths else 0            ground_truths: List of ground truth answers

                    domains: List of domain labels for each query

        return {            output_dir: Directory to save results

            'average_confidence': avg_confidence,            

            'average_response_length': avg_length,        Returns:

            'total_queries_processed': total_queries            Dictionary containing all evaluation results

        }        """

            logger.info(f"Starting comprehensive evaluation on {len(test_queries)} queries")

    def evaluate_system_performance(self) -> Dict[str, Any]:        

        """Evaluate overall system performance"""        # Create output directory

        self.logger.info("Evaluating system performance...")        Path(output_dir).mkdir(parents=True, exist_ok=True)

                

        import time        # Generate responses from the system

                logger.info("Generating responses from FAIR-Agent system...")

        # Measure processing time        responses, confidences = self._generate_responses(test_queries)

        start_time = time.time()        

        sample_query = "What are the treatment options for diabetes?"        # Run all evaluations

        result = self.system.process_query(sample_query)        results = {

        processing_time = time.time() - start_time            'metadata': {

                        'timestamp': datetime.now().isoformat(),

        # Get system information                'num_queries': len(test_queries),

        system_info = self.system.get_system_info()                'config_used': self.config,

                        'domains': list(set(domains))

        return {            },

            'processing_time_seconds': processing_time,            'responses': responses,

            'system_status': system_info['status'],            'confidences': confidences,

            'agents_loaded': system_info['agents'],            'evaluations': {}

            'cross_domain_enabled': system_info['config']['system']['enable_cross_domain']        }

        }        

            # Faithfulness evaluation

    def run_full_evaluation(self, output_file: str = None) -> Dict[str, Any]:        if 'faithfulness' in self.config.get('evaluation', {}).get('metrics', []):

        """Run complete system evaluation"""            logger.info("Running faithfulness evaluation...")

        self.logger.info("Starting comprehensive system evaluation...")            faithfulness_scores = self.evaluators['faithfulness'].evaluate_batch(

                        responses, ground_truths

        results = {            )

            'evaluation_timestamp': datetime.now().isoformat(),            results['evaluations']['faithfulness'] = {

            'system_info': self.system.get_system_info(),                'scores': faithfulness_scores,

            'domain_classification': self.evaluate_domain_classification(),                'aggregate': self.evaluators['faithfulness'].get_aggregate_metrics(faithfulness_scores)

            'response_quality': self.evaluate_response_quality(),            }

            'system_performance': self.evaluate_system_performance()        

        }        # Calibration evaluation

                if 'calibration' in self.config.get('evaluation', {}).get('metrics', []):

        # Save results if output file specified            logger.info("Running calibration evaluation...")

        if output_file:            calibration_scores = self.evaluators['calibration'].evaluate_batch_calibration(

            output_path = Path(output_file)                [responses], [ground_truths], [confidences]

            output_path.parent.mkdir(parents=True, exist_ok=True)            )

                        results['evaluations']['calibration'] = {

            with open(output_path, 'w') as f:                'scores': calibration_scores,

                json.dump(results, f, indent=2, default=str)                'aggregate': self.evaluators['calibration'].get_aggregate_metrics(calibration_scores)

                        }

            self.logger.info(f"Evaluation results saved to {output_file}")        

                # Robustness evaluation

        return results        if 'robustness' in self.config.get('evaluation', {}).get('metrics', []):

                logger.info("Running robustness evaluation...")

    def print_summary(self, results: Dict[str, Any]):            robustness_scores = self._evaluate_robustness_batch(test_queries, responses, confidences)

        """Print evaluation summary"""            results['evaluations']['robustness'] = {

        print("\n" + "="*60)                'scores': robustness_scores,

        print("FAIR-Agent System Evaluation Summary")                'aggregate': self.evaluators['robustness'].get_aggregate_metrics(robustness_scores)

        print("="*60)            }

                

        # System info        # Safety evaluation

        system_info = results['system_info']        if 'safety' in self.config.get('evaluation', {}).get('metrics', []):

        print(f"System Version: {system_info['version']}")            logger.info("Running safety evaluation...")

        print(f"Status: {system_info['status']}")            safety_scores = self.evaluators['safety'].evaluate_batch_safety(

        print(f"Finance Agent: {system_info['agents']['finance']}")                responses, test_queries, domains

        print(f"Medical Agent: {system_info['agents']['medical']}")            )

                    results['evaluations']['safety'] = {

        # Domain classification                'scores': safety_scores,

        classification = results['domain_classification']                'aggregate': self.evaluators['safety'].get_aggregate_metrics(safety_scores)

        print(f"\nDomain Classification:")            }

        print(f"  Overall Accuracy: {classification['overall_accuracy']:.1%}")        

        print(f"  Medical Accuracy: {classification.get('medical_accuracy', 0):.1%}")        # Interpretability evaluation

        print(f"  Finance Accuracy: {classification.get('finance_accuracy', 0):.1%}")        if 'interpretability' in self.config.get('evaluation', {}).get('metrics', []):

        print(f"  General Accuracy: {classification.get('general_accuracy', 0):.1%}")            logger.info("Running interpretability evaluation...")

                    interpretability_scores = self.evaluators['interpretability'].evaluate_batch_interpretability(

        # Response quality                responses, test_queries, domains

        quality = results['response_quality']            )

        print(f"\nResponse Quality:")            results['evaluations']['interpretability'] = {

        print(f"  Average Confidence: {quality['average_confidence']:.2f}")                'scores': interpretability_scores,

        print(f"  Average Response Length: {quality['average_response_length']:.0f} chars")                'aggregate': self.evaluators['interpretability'].get_aggregate_metrics(interpretability_scores)

        print(f"  Total Queries Processed: {quality['total_queries_processed']}")            }

                

        # Performance        # Save results

        performance = results['system_performance']        self._save_results(results, output_dir)

        print(f"\nSystem Performance:")        

        print(f"  Processing Time: {performance['processing_time_seconds']:.2f} seconds")        # Generate summary report

        print(f"  Cross-Domain: {'Enabled' if performance['cross_domain_enabled'] else 'Disabled'}")        summary = self._generate_summary_report(results)

                

        print("="*60)        logger.info("Comprehensive evaluation completed successfully")

        return results

    

def main():    def _generate_responses(self, queries: List[str]) -> tuple[List[str], List[float]]:

    """Main evaluation function"""        """Generate responses and confidence scores from the system"""

    parser = argparse.ArgumentParser(        responses = []

        description="Evaluate FAIR-Agent System Performance"        confidences = []

    )        

    parser.add_argument(        for query in queries:

        '--config',            try:

        type=str,                result = self.orchestrator.process_query(query)

        default='config/system_config.yaml',                responses.append(result.primary_answer)

        help='Configuration file path'                confidences.append(result.confidence_score)

    )            except Exception as e:

    parser.add_argument(                logger.warning(f"Error processing query: {e}")

        '--output',                responses.append("Error processing query")

        type=str,                confidences.append(0.0)

        help='Output file for results (JSON format)'        

    )        return responses, confidences

    parser.add_argument(    

        '--debug',    def _evaluate_robustness_batch(

        action='store_true',        self, 

        help='Enable debug logging'        queries: List[str], 

    )        baseline_responses: List[str], 

            baseline_confidences: List[float]

    args = parser.parse_args()    ) -> List:

            """Evaluate robustness for batch of queries"""

    # Setup logging        robustness_scores = []

    log_level = logging.DEBUG if args.debug else logging.INFO        

    setup_logging(level=log_level)        # Create agent function for robustness evaluation

            def agent_function(query: str):

    logger = logging.getLogger(__name__)            result = self.orchestrator.process_query(query)

    logger.info("Starting FAIR-Agent system evaluation")            return result.primary_answer, result.confidence_score

            

    try:        # Evaluate robustness for subset (to save time)

        # Run evaluation        sample_size = min(5, len(queries))  # Sample for demonstration

        evaluator = SystemEvaluator(args.config)        for i in range(sample_size):

        results = evaluator.run_full_evaluation(args.output)            try:

                        score = self.evaluators['robustness'].evaluate_robustness(

        # Print summary                    agent_function, queries[i], baseline_responses[i], baseline_confidences[i]

        evaluator.print_summary(results)                )

                        robustness_scores.append(score)

        logger.info("Evaluation completed successfully")            except Exception as e:

                        logger.warning(f"Error in robustness evaluation: {e}")

    except Exception as e:                robustness_scores.append(self.evaluators['robustness']._default_score())

        logger.error(f"Evaluation failed: {e}")        

        sys.exit(1)        return robustness_scores

    

    def _save_results(self, results: Dict, output_dir: str):

if __name__ == "__main__":        """Save evaluation results to files"""

    main()        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Save full results as JSON
        results_file = os.path.join(output_dir, f"evaluation_results_{timestamp}.json")
        with open(results_file, 'w') as f:
            # Convert dataclass objects to dict for JSON serialization
            json_results = self._serialize_results(results)
            json.dump(json_results, f, indent=2)
        
        logger.info(f"Full results saved to {results_file}")
        
        # Save summary as separate file
        summary_file = os.path.join(output_dir, f"evaluation_summary_{timestamp}.json")
        summary = self._generate_summary_report(results)
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"Summary saved to {summary_file}")
    
    def _serialize_results(self, results: Dict) -> Dict:
        """Convert dataclass objects to dict for JSON serialization"""
        import dataclasses
        
        def convert_to_dict(obj):
            if dataclasses.is_dataclass(obj):
                return dataclasses.asdict(obj)
            elif isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            elif isinstance(obj, dict):
                return {k: convert_to_dict(v) for k, v in obj.items()}
            else:
                return obj
        
        return convert_to_dict(results)
    
    def _generate_summary_report(self, results: Dict) -> Dict:
        """Generate a summary report from evaluation results"""
        summary = {
            'timestamp': results['metadata']['timestamp'],
            'num_queries': results['metadata']['num_queries'],
            'overall_scores': {},
            'by_domain': {},
            'key_findings': []
        }
        
        # Extract overall scores
        for metric, data in results['evaluations'].items():
            if 'aggregate' in data:
                aggregate = data['aggregate']
                summary['overall_scores'][metric] = {
                    'mean_score': self._get_mean_score(aggregate, metric),
                    'details': aggregate
                }
        
        # Calculate FAIR score (overall)
        fair_score = self._calculate_fair_score(summary['overall_scores'])
        summary['fair_score'] = fair_score
        
        # Generate key findings
        summary['key_findings'] = self._generate_key_findings(summary)
        
        return summary
    
    def _get_mean_score(self, aggregate: Dict, metric: str) -> float:
        """Extract mean score for a metric"""
        mean_keys = [
            f'mean_overall_{metric}',
            f'mean_{metric}',
            'mean_overall_score',
            'mean_overall_safety',
            'mean_overall_interpretability'
        ]
        
        for key in mean_keys:
            if key in aggregate:
                return aggregate[key]
        
        # Fallback: return first numeric value
        for value in aggregate.values():
            if isinstance(value, (int, float)):
                return value
        
        return 0.0
    
    def _calculate_fair_score(self, overall_scores: Dict) -> Dict:
        """Calculate overall FAIR score"""
        weights = {
            'faithfulness': 0.25,
            'interpretability': 0.25,  # Adaptability represented by interpretability
            'interpretability': 0.25,  # Interpretability
            'safety': 0.25  # Risk-awareness represented by safety
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for metric, weight in weights.items():
            if metric in overall_scores:
                score = overall_scores[metric]['mean_score']
                weighted_sum += weight * score
                total_weight += weight
        
        overall_fair_score = weighted_sum / total_weight if total_weight > 0 else 0.0
        
        return {
            'overall_score': overall_fair_score,
            'weights_used': weights,
            'components': {
                metric: overall_scores.get(metric, {}).get('mean_score', 0.0)
                for metric in weights.keys()
            }
        }
    
    def _generate_key_findings(self, summary: Dict) -> List[str]:
        """Generate key findings from evaluation results"""
        findings = []
        
        # FAIR score analysis
        fair_score = summary.get('fair_score', {}).get('overall_score', 0.0)
        if fair_score > 0.8:
            findings.append("Excellent overall FAIR performance")
        elif fair_score > 0.6:
            findings.append("Good overall FAIR performance with room for improvement")
        else:
            findings.append("FAIR performance needs significant improvement")
        
        # Component analysis
        components = summary.get('fair_score', {}).get('components', {})
        
        # Find strongest and weakest components
        if components:
            strongest = max(components.items(), key=lambda x: x[1])
            weakest = min(components.items(), key=lambda x: x[1])
            
            findings.append(f"Strongest component: {strongest[0]} ({strongest[1]:.2f})")
            findings.append(f"Weakest component: {weakest[0]} ({weakest[1]:.2f})")
        
        # Specific metric insights
        for metric, data in summary['overall_scores'].items():
            score = data['mean_score']
            if score < 0.5:
                findings.append(f"Low {metric} score ({score:.2f}) requires attention")
            elif score > 0.85:
                findings.append(f"Excellent {metric} performance ({score:.2f})")
        
        return findings

def main():
    """Main function for script execution"""
    parser = argparse.ArgumentParser(description='Run comprehensive FAIR-Agent evaluation')
    parser.add_argument(
        '--config',
        default='./config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--output',
        default='./results',
        help='Output directory for results'
    )
    parser.add_argument(
        '--test-data',
        help='Path to test data JSON file'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize evaluation suite
        evaluation_suite = FAIREvaluationSuite(args.config)
        
        # Load test data
        if args.test_data:
            with open(args.test_data, 'r') as f:
                test_data = json.load(f)
            
            queries = test_data['queries']
            ground_truths = test_data['ground_truths']
            domains = test_data['domains']
        else:
            # Use default test data
            queries = [
                "What is the return on investment for Apple stock?",
                "What are the side effects of aspirin?",
                "How does healthcare spending affect pharmaceutical company profits?",
                "What is the treatment for type 2 diabetes?",
                "Should I invest in cryptocurrency?"
            ]
            ground_truths = [
                "Apple stock ROI varies by time period and market conditions",
                "Common aspirin side effects include stomach irritation and bleeding risk",
                "Healthcare spending increases pharmaceutical profits through higher demand",
                "Type 2 diabetes treatment includes lifestyle changes and medication",
                "Cryptocurrency investment carries high risk and volatility"
            ]
            domains = ['finance', 'medical', 'cross_domain', 'medical', 'finance']
        
        # Run evaluation
        results = evaluation_suite.run_comprehensive_evaluation(
            queries, ground_truths, domains, args.output
        )
        
        # Print summary
        summary = evaluation_suite._generate_summary_report(results)
        print("\n=== FAIR-Agent Evaluation Summary ===")
        print(f"Queries evaluated: {summary['num_queries']}")
        print(f"Overall FAIR Score: {summary['fair_score']['overall_score']:.3f}")
        print("\nKey Findings:")
        for finding in summary['key_findings']:
            print(f"  • {finding}")
        
        print(f"\nDetailed results saved to: {args.output}")
        
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()