#!/usr/bin/env python3
"""
Baseline Evaluation Script

This script runs actual baseline evaluation to calculate real baseline scores
instead of using hardcoded values.
"""

import asyncio
import argparse
import logging
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.evaluation.baseline_evaluator import BaselineEvaluator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run baseline evaluation"""
    parser = argparse.ArgumentParser(description='Run FAIR-Agent Baseline Evaluation')
    parser.add_argument(
        '--queries-per-domain', 
        type=int, 
        default=5,
        help='Number of queries to test per domain (default: 5)'
    )
    parser.add_argument(
        '--output-file',
        type=str,
        default='results/baseline_scores.json',
        help='Output file for baseline results'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("🚀 Starting FAIR-Agent Baseline Evaluation")
    logger.info(f"Queries per domain: {args.queries_per_domain}")
    logger.info(f"Output file: {args.output_file}")
    
    try:
        # Initialize baseline evaluator
        evaluator = BaselineEvaluator()
        
        # Run baseline evaluation
        logger.info("📊 Running baseline evaluation (this may take a few minutes)...")
        results = evaluator.run_baseline_evaluation(
            num_queries_per_domain=args.queries_per_domain
        )
        
        # Display results
        print("\n" + "="*60)
        print("📊 BASELINE EVALUATION RESULTS")
        print("="*60)
        print(f"Total Queries Evaluated: {results.total_queries}")
        print(f"Evaluation Time: {results.evaluation_time:.2f} seconds")
        print("\n📈 BASELINE SCORES:")
        print(f"  • Faithfulness:     {results.avg_faithfulness:.3f} ({results.avg_faithfulness*100:.1f}%)")
        print(f"  • Adaptability:     {results.avg_adaptability:.3f} ({results.avg_adaptability*100:.1f}%)")
        print(f"  • Interpretability: {results.avg_interpretability:.3f} ({results.avg_interpretability*100:.1f}%)")
        print(f"  • Safety:           {results.avg_safety:.3f} ({results.avg_safety*100:.1f}%)")
        
        # Calculate overall score
        overall_baseline = (
            results.avg_faithfulness + 
            results.avg_adaptability + 
            results.avg_interpretability + 
            results.avg_safety
        ) / 4
        print(f"\n🎯 Overall Baseline Score: {overall_baseline:.3f} ({overall_baseline*100:.1f}%)")
        
        # Save results
        output_path = Path(args.output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        evaluator.save_baseline_results(results, str(output_path))
        
        print(f"\n💾 Results saved to: {output_path}")
        
        # Compare with hardcoded values
        print("\n" + "="*60)
        print("📋 COMPARISON WITH CURRENT HARDCODED VALUES")
        print("="*60)
        
        hardcoded_scores = {
            'faithfulness': 0.65,
            'adaptability': 0.50,  # Estimated
            'interpretability': 0.45,
            'safety': 0.40
        }
        
        actual_scores = {
            'faithfulness': results.avg_faithfulness,
            'adaptability': results.avg_adaptability,
            'interpretability': results.avg_interpretability,
            'safety': results.avg_safety
        }
        
        for metric in hardcoded_scores:
            hardcoded = hardcoded_scores[metric]
            actual = actual_scores[metric]
            difference = actual - hardcoded
            percentage_diff = (difference / hardcoded) * 100 if hardcoded > 0 else 0
            
            status = "✅" if abs(percentage_diff) < 10 else "⚠️" if abs(percentage_diff) < 25 else "❌"
            
            print(f"{status} {metric.title():>15}: "
                  f"Hardcoded={hardcoded:.3f}, "
                  f"Actual={actual:.3f}, "
                  f"Diff={difference:+.3f} ({percentage_diff:+.1f}%)")
        
        print("\n🎯 RECOMMENDATIONS:")
        if overall_baseline < 0.5:
            print("• ⚠️ Baseline performance is low - consider adjusting evaluation criteria")
        else:
            print("• ✅ Baseline performance is reasonable")
        
        large_differences = [
            metric for metric, hardcoded in hardcoded_scores.items()
            if abs(actual_scores[metric] - hardcoded) > 0.1
        ]
        
        if large_differences:
            print(f"• 🔧 Update hardcoded baseline values for: {', '.join(large_differences)}")
        else:
            print("• ✅ Hardcoded baseline values are reasonably accurate")
        
        print("\n" + "="*60)
        print("🎉 Baseline evaluation completed successfully!")
        print("="*60)
        
    except KeyboardInterrupt:
        print("\n⏹️ Evaluation stopped by user")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"❌ Baseline evaluation failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()