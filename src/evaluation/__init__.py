"""
Evaluation Framework for FAIR-Agent System

This module implements evaluation metrics for assessing the performance
of FAIR agents across multiple dimensions: Faithfulness, Adaptability,
Interpretability, and Risk-awareness.
"""

from .faithfulness import FaithfulnessEvaluator
from .adaptability import AdaptabilityEvaluator
from .calibration import CalibrationEvaluator
from .robustness import RobustnessEvaluator
from .safety import SafetyEvaluator
from .interpretability import InterpretabilityEvaluator

__all__ = [
    'FaithfulnessEvaluator',
    'AdaptabilityEvaluator',
    'CalibrationEvaluator', 
    'RobustnessEvaluator',
    'SafetyEvaluator',
    'InterpretabilityEvaluator'
]