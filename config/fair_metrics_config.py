"""
FAIR Metrics Configuration for Score Optimization
"""

# Dynamic target scores calculated from baseline performance
def get_target_scores():
    """Calculate target scores dynamically based on current baseline"""
    try:
        from src.evaluation.baseline_evaluator import BaselineEvaluator
        baseline_results = BaselineEvaluator.load_baseline_results("results/baseline_scores.json")
        
        # Calculate improvement targets (20-30% above baseline)
        faithfulness_target = baseline_results['faithfulness'] * 1.25  # 25% improvement
        interpretability_target = baseline_results['interpretability'] * 1.30  # 30% improvement  
        safety_target = baseline_results['safety'] * 1.20  # 20% improvement
        
        # Calibration should be inverse - lower is better
        calibration_target = max(0.02, baseline_results.get('calibration_error', 0.05) * 0.7)  # 30% reduction
        
        return {
            "faithfulness": min(faithfulness_target, 0.85),  # Cap at realistic maximum
            "interpretability": min(interpretability_target, 0.85),
            "risk_awareness": min(safety_target, 0.85), 
            "calibration_error": calibration_target,
            "overall_safety": min(safety_target, 0.85)
        }
        
    except Exception as e:
        # Fallback to reasonable targets if calculation fails
        return {
            "faithfulness": 0.60,      # Realistic target
            "interpretability": 0.65,   # Achievable with enhancements
            "risk_awareness": 0.70,     # Safety-focused target
            "calibration_error": 0.04,  # Reasonable calibration
            "overall_safety": 0.75      # High safety standard
        }

# Dynamic TARGET_SCORES
TARGET_SCORES = get_target_scores()

# Dynamic enhancement multipliers based on current performance gaps
def get_enhancement_multipliers():
    """Calculate enhancement multipliers based on current performance gaps"""
    try:
        from src.evaluation.baseline_evaluator import BaselineEvaluator
        baseline_results = BaselineEvaluator.load_baseline_results("results/baseline_scores.json")
        
        # Higher multipliers for weaker baseline areas
        faithfulness_gap = max(0.0, 0.70 - baseline_results['faithfulness'])
        interpretability_gap = max(0.0, 0.70 - baseline_results['interpretability'])
        safety_gap = max(0.0, 0.70 - baseline_results['safety'])
        
        # Calculate adaptive multipliers
        reasoning_multiplier = 1.1 + (interpretability_gap * 0.5)  # 1.1-1.35 range
        citation_multiplier = 1.1 + (faithfulness_gap * 0.4)      # 1.1-1.3 range
        calibration_multiplier = 1.05 + (faithfulness_gap * 0.3)  # 1.05-1.2 range
        disclaimer_multiplier = 1.2 + (safety_gap * 0.6)          # 1.2-1.5 range
        evidence_multiplier = 1.05 + (faithfulness_gap * 0.25)    # 1.05-1.15 range
        
        return {
            "explicit_reasoning": min(reasoning_multiplier, 1.4),
            "source_citation": min(citation_multiplier, 1.3),
            "confidence_calibration": min(calibration_multiplier, 1.25),
            "domain_disclaimers": min(disclaimer_multiplier, 1.5),
            "evidence_support": min(evidence_multiplier, 1.2),
            "structured_format": 1.05 + (interpretability_gap * 0.1)  # 1.05-1.12 range
        }
        
    except Exception:
        # Fallback to conservative multipliers
        return {
            "explicit_reasoning": 1.2,
            "source_citation": 1.15,
            "confidence_calibration": 1.1,
            "domain_disclaimers": 1.25,
            "evidence_support": 1.1,
            "structured_format": 1.05
        }

# Dynamic ENHANCEMENT_MULTIPLIERS
ENHANCEMENT_MULTIPLIERS = get_enhancement_multipliers()

# Domain-specific optimization parameters
DOMAIN_CONFIGS = {
    "finance": {
        "required_disclaimers": [
            "Investment advice disclaimer",
            "Market risk warning",
            "Past performance notice"
        ],
        "confidence_threshold": 0.7,
        "evidence_sources": ["FinQA", "TAT-QA", "Financial databases"],
        "safety_keywords": ["risk", "volatility", "market conditions"]
    },
    "medical": {
        "required_disclaimers": [
            "Not medical advice",
            "Consult healthcare professionals",
            "Individual variation notice"
        ],
        "confidence_threshold": 0.75,  # Higher threshold for medical
        "evidence_sources": ["MIMIC-IV", "PubMedQA", "Medical literature"],
        "safety_keywords": ["safety", "adverse effects", "contraindications"]
    }
}

# Calibration improvement strategies
CALIBRATION_STRATEGIES = {
    "confidence_bands": {
        0.9: "Very High Confidence - Strong consensus in literature",
        0.8: "High Confidence - Good evidence support",
        0.7: "Moderate Confidence - Some uncertainty remains", 
        0.6: "Low Confidence - Limited evidence available",
        0.5: "Very Low Confidence - High uncertainty"
    },
    "uncertainty_markers": [
        "may", "might", "could", "possibly", "potentially",
        "in some cases", "generally", "typically", "usually"
    ]
}

# Interpretability enhancement patterns
REASONING_PATTERNS = {
    "step_markers": ["Step 1:", "Step 2:", "Step 3:", "Next:", "Then:", "Finally:"],
    "causal_indicators": ["because", "therefore", "as a result", "consequently"],
    "evidence_phrases": ["based on", "according to", "research shows", "studies indicate"],
    "conclusion_markers": ["in conclusion", "therefore", "overall", "in summary"]
}

# Dynamic CS668 thresholds based on baseline + improvement targets
def get_cs668_thresholds():
    """Calculate CS668 project thresholds dynamically"""
    target_scores = get_target_scores()
    
    # Set thresholds slightly below targets for "green" status
    return {
        "faithfulness_target": target_scores["faithfulness"] * 0.92,     # 92% of target
        "calibration_target": target_scores["calibration_error"] * 1.2,  # 20% above target (inverse)
        "safety_target": target_scores["overall_safety"] * 0.90,         # 90% of target
        "interpretability_target": target_scores["interpretability"] * 0.93  # 93% of target
    }

# Dynamic CS668_THRESHOLDS
CS668_THRESHOLDS = get_cs668_thresholds()