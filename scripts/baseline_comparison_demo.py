#!/usr/bin/env python3
"""
Baseline Comparison Demo

This script demonstrates the difference between using hardcoded baseline values
versus calculated baseline values in the FAIR evaluation system.
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.evaluation.comprehensive_evaluator import FairAgentEvaluator

def main():
    print("="*70)
    print("🔍 BASELINE CALCULATION DEMONSTRATION")
    print("="*70)
    
    print("\n📊 COMPARISON: Hardcoded vs. Calculated Baselines\n")
    
    # Initialize evaluator with hardcoded baselines (default)
    evaluator_hardcoded = FairAgentEvaluator()
    
    # Initialize evaluator with calculated baselines
    baseline_file = "results/baseline_scores.json"
    evaluator_calculated = FairAgentEvaluator(baseline_file=baseline_file)
    
    # Sample current FAIR scores (from recent evaluation)
    current_scores = {
        'faithfulness': 0.633,
        'adaptability': 0.802,
        'interpretability': 0.376,
        'safety': 0.666
    }
    
    print("Current FAIR-Agent Performance:")
    for metric, score in current_scores.items():
        print(f"  • {metric.title():>15}: {score:.3f} ({score*100:.1f}%)")
    
    print("\n" + "-"*70)
    print("BASELINE COMPARISON:")
    print("-"*70)
    
    # Calculate improvements using both baselines
    print(f"{'Metric':<15} {'Hardcoded':<10} {'Calculated':<11} {'Hard-Imp':<10} {'Calc-Imp':<10}")
    print("-" * 60)
    
    for metric in current_scores:
        # Map metric names
        baseline_key = 'risk_awareness' if metric == 'safety' else metric
        
        hardcoded_baseline = evaluator_hardcoded.baseline_scores.get(baseline_key, 0.5)
        calculated_baseline = evaluator_calculated.baseline_scores.get(baseline_key, 0.5)
        
        current = current_scores[metric]
        
        hard_improvement = ((current - hardcoded_baseline) / hardcoded_baseline) * 100 if hardcoded_baseline > 0 else 0
        calc_improvement = ((current - calculated_baseline) / calculated_baseline) * 100 if calculated_baseline > 0 else 0
        
        print(f"{metric:<15} {hardcoded_baseline:<10.3f} {calculated_baseline:<11.3f} "
              f"{hard_improvement:<10.1f}% {calc_improvement:<10.1f}%")
    
    print("\n" + "="*70)
    print("📈 ANALYSIS:")
    print("="*70)
    
    # Analysis
    print("\n🔍 Key Findings:")
    
    if abs(evaluator_hardcoded.baseline_scores['faithfulness'] - evaluator_calculated.baseline_scores['faithfulness']) > 0.1:
        print("• ⚠️ FAITHFULNESS: Significant difference between hardcoded and calculated baselines")
        print(f"  - Hardcoded assumes {evaluator_hardcoded.baseline_scores['faithfulness']:.1%} baseline faithfulness")
        print(f"  - Actual measurement shows {evaluator_calculated.baseline_scores['faithfulness']:.1%} baseline faithfulness")
    
    if abs(evaluator_hardcoded.baseline_scores['interpretability'] - evaluator_calculated.baseline_scores['interpretability']) > 0.1:
        print("• ⚠️ INTERPRETABILITY: Major discrepancy in baseline assumptions")
        print(f"  - Hardcoded assumes {evaluator_hardcoded.baseline_scores['interpretability']:.1%} baseline interpretability")
        print(f"  - Actual measurement shows {evaluator_calculated.baseline_scores['interpretability']:.1%} baseline interpretability")
    
    # Load baseline details
    try:
        with open(baseline_file, 'r') as f:
            baseline_data = json.load(f)
        
        print(f"\n📊 Calculated Baseline Details:")
        print(f"  • Evaluation Date: {baseline_data['timestamp'][:19]}")
        print(f"  • Queries Tested: {baseline_data['evaluation_details']['total_queries']}")
        print(f"  • Evaluation Time: {baseline_data['evaluation_details']['evaluation_time']:.2f}s")
        
    except Exception as e:
        print(f"\n❌ Could not load baseline details: {e}")
    
    print(f"\n🎯 RECOMMENDATIONS:")
    print("="*50)
    
    # Check if Ollama was running during baseline calculation
    baseline_scores = evaluator_calculated.baseline_scores
    if all(score == 0.4 for score in [baseline_scores['faithfulness']]) and baseline_scores['interpretability'] < 0.3:
        print("⚠️ WARNING: Baseline evaluation may have failed due to Ollama not running")
        print("   • Start Ollama: `ollama serve`")
        print("   • Re-run baseline evaluation with working LLM")
        print("   • Current baselines are based on fallback responses only")
    else:
        print("✅ GOOD: Baseline evaluation completed with actual LLM responses")
        
        # Provide specific recommendations
        significant_diffs = []
        for metric in current_scores:
            baseline_key = 'risk_awareness' if metric == 'safety' else metric
            hardcoded = evaluator_hardcoded.baseline_scores.get(baseline_key, 0.5)
            calculated = evaluator_calculated.baseline_scores.get(baseline_key, 0.5)
            
            if abs(hardcoded - calculated) > 0.1:
                significant_diffs.append(metric)
        
        if significant_diffs:
            print(f"🔧 UPDATE NEEDED: Hardcoded baselines for {', '.join(significant_diffs)}")
            print("   • Use calculated values for more accurate improvement measurements")
        else:
            print("✅ GOOD: Hardcoded baselines are reasonably close to calculated values")
    
    print(f"\n💡 IMPACT ON FAIR EVALUATION:")
    print("   • More accurate baselines → More reliable improvement measurements")
    print("   • Dynamic baseline calculation → Adapts to model changes")
    print("   • Evidence-based evaluation → Better trustworthiness assessment")
    
    print("\n" + "="*70)
    print("🎉 Baseline comparison demonstration complete!")
    print("="*70)

if __name__ == "__main__":
    main()