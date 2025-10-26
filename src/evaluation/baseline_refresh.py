"""
Baseline Auto-Refresh System

This module provides automatic baseline recalculation functionality
to keep baseline scores up-to-date with model changes and improvements.
"""

import logging
import schedule
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any
import yaml

logger = logging.getLogger(__name__)

class BaselineRefreshManager:
    """
    Manages automatic refresh of baseline scores
    
    This class handles:
    - Periodic baseline recalculation
    - Baseline staleness detection
    - Automatic refresh scheduling
    - Configuration-driven refresh intervals
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize baseline refresh manager
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = config_path or "config/config.yaml"
        self.config = self._load_config()
        
        # Extract baseline configuration
        baseline_config = self.config.get('evaluation', {}).get('baseline', {})
        
        self.auto_calculate = baseline_config.get('auto_calculate', True)
        self.cache_file = baseline_config.get('cache_file', 'results/baseline_scores.json')
        self.queries_per_domain = baseline_config.get('queries_per_domain', 5)
        self.recalculate_interval_days = baseline_config.get('recalculate_interval_days', 7)
        self.fallback_to_hardcoded = baseline_config.get('fallback_to_hardcoded', True)
        
        self._refresh_thread = None
        self._stop_refresh = False
        
        logger.info(f"Baseline refresh manager initialized:")
        logger.info(f"  Auto-calculate: {self.auto_calculate}")
        logger.info(f"  Refresh interval: {self.recalculate_interval_days} days")
        logger.info(f"  Cache file: {self.cache_file}")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            with open(self.config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.warning(f"Could not load config from {self.config_path}: {e}")
            return {}
    
    def is_baseline_stale(self) -> bool:
        """
        Check if baseline scores are stale and need refresh
        
        Returns:
            True if baselines need refresh, False otherwise
        """
        baseline_path = Path(self.cache_file)
        
        if not baseline_path.exists():
            logger.info("📊 Baseline file not found - needs initial calculation")
            return True
        
        try:
            import json
            with open(baseline_path, 'r') as f:
                baseline_data = json.load(f)
            
            # Check timestamp
            timestamp_str = baseline_data.get('timestamp')
            if not timestamp_str:
                logger.warning("⚠️ Baseline file missing timestamp - assuming stale")
                return True
            
            # Parse timestamp
            try:
                baseline_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                if baseline_time.tzinfo is None:
                    # Handle naive datetime
                    baseline_time = datetime.fromisoformat(timestamp_str)
                else:
                    # Convert to local time for comparison
                    baseline_time = baseline_time.replace(tzinfo=None)
            except ValueError:
                logger.warning("⚠️ Invalid timestamp format - assuming stale")
                return True
            
            # Check if older than refresh interval
            age_days = (datetime.now() - baseline_time).days
            is_stale = age_days >= self.recalculate_interval_days
            
            if is_stale:
                logger.info(f"📅 Baseline is {age_days} days old (limit: {self.recalculate_interval_days}) - needs refresh")
            else:
                logger.info(f"✅ Baseline is {age_days} days old - still fresh")
            
            return is_stale
            
        except Exception as e:
            logger.warning(f"⚠️ Error checking baseline staleness: {e} - assuming stale")
            return True
    
    def refresh_baseline_scores(self) -> bool:
        """
        Refresh baseline scores by running evaluation
        
        Returns:
            True if refresh successful, False otherwise
        """
        if not self.auto_calculate:
            logger.info("🚫 Auto-calculate disabled - skipping baseline refresh")
            return False
        
        logger.info("🔄 Starting baseline refresh...")
        
        try:
            from src.evaluation.baseline_evaluator import BaselineEvaluator
            
            # Initialize evaluator
            evaluator = BaselineEvaluator()
            
            # Run baseline evaluation
            logger.info(f"📊 Running baseline evaluation with {self.queries_per_domain} queries per domain...")
            results = evaluator.run_baseline_evaluation(
                num_queries_per_domain=self.queries_per_domain
            )
            
            # Ensure directory exists
            baseline_path = Path(self.cache_file)
            baseline_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save results
            evaluator.save_baseline_results(results, str(baseline_path))
            
            logger.info("✅ Baseline refresh completed successfully")
            logger.info(f"New baseline scores:")
            logger.info(f"  Faithfulness: {results.avg_faithfulness:.3f}")
            logger.info(f"  Adaptability: {results.avg_adaptability:.3f}")
            logger.info(f"  Interpretability: {results.avg_interpretability:.3f}")
            logger.info(f"  Safety: {results.avg_safety:.3f}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Baseline refresh failed: {e}")
            if self.fallback_to_hardcoded:
                logger.warning("⚠️ Using hardcoded fallback baselines")
            return False
    
    def ensure_baseline_available(self) -> bool:
        """
        Ensure baseline scores are available, refresh if necessary
        
        Returns:
            True if baselines are available, False otherwise
        """
        if self.is_baseline_stale():
            return self.refresh_baseline_scores()
        else:
            logger.info("✅ Current baseline scores are fresh")
            return True
    
    def start_automatic_refresh(self):
        """Start automatic baseline refresh in background thread"""
        if not self.auto_calculate:
            logger.info("🚫 Auto-calculate disabled - not starting automatic refresh")
            return
        
        if self._refresh_thread and self._refresh_thread.is_alive():
            logger.warning("⚠️ Automatic refresh already running")
            return
        
        logger.info(f"🚀 Starting automatic baseline refresh (every {self.recalculate_interval_days} days)")
        
        # Schedule daily checks
        schedule.clear()
        schedule.every().day.at("02:00").do(self._check_and_refresh)
        
        # Start scheduler thread
        self._stop_refresh = False
        self._refresh_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._refresh_thread.start()
        
        # Initial check
        self.ensure_baseline_available()
    
    def stop_automatic_refresh(self):
        """Stop automatic baseline refresh"""
        logger.info("🛑 Stopping automatic baseline refresh")
        self._stop_refresh = True
        schedule.clear()
        
        if self._refresh_thread and self._refresh_thread.is_alive():
            self._refresh_thread.join(timeout=5)
    
    def _check_and_refresh(self):
        """Check if refresh is needed and perform it"""
        try:
            if self.is_baseline_stale():
                self.refresh_baseline_scores()
        except Exception as e:
            logger.error(f"❌ Error in scheduled baseline refresh: {e}")
    
    def _run_scheduler(self):
        """Run the scheduler in background thread"""
        logger.info("⏰ Baseline refresh scheduler started")
        
        while not self._stop_refresh:
            try:
                schedule.run_pending()
                time.sleep(3600)  # Check every hour
            except Exception as e:
                logger.error(f"❌ Error in scheduler thread: {e}")
                time.sleep(3600)  # Continue after error
        
        logger.info("⏹️ Baseline refresh scheduler stopped")
    
    def get_baseline_status(self) -> Dict[str, Any]:
        """
        Get current baseline status information
        
        Returns:
            Dictionary with baseline status details
        """
        baseline_path = Path(self.cache_file)
        
        if not baseline_path.exists():
            return {
                'exists': False,
                'stale': True,
                'age_days': None,
                'last_updated': None,
                'needs_refresh': True
            }
        
        try:
            import json
            with open(baseline_path, 'r') as f:
                baseline_data = json.load(f)
            
            timestamp_str = baseline_data.get('timestamp')
            if timestamp_str:
                baseline_time = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
                if baseline_time.tzinfo:
                    baseline_time = baseline_time.replace(tzinfo=None)
                
                age_days = (datetime.now() - baseline_time).days
                is_stale = age_days >= self.recalculate_interval_days
            else:
                age_days = None
                is_stale = True
            
            return {
                'exists': True,
                'stale': is_stale,
                'age_days': age_days,
                'last_updated': timestamp_str,
                'needs_refresh': is_stale,
                'scores': baseline_data.get('baseline_scores', {}),
                'auto_refresh_enabled': self.auto_calculate
            }
            
        except Exception as e:
            logger.warning(f"Error getting baseline status: {e}")
            return {
                'exists': True,
                'stale': True,
                'age_days': None,
                'last_updated': None,
                'needs_refresh': True,
                'error': str(e)
            }


# Global instance for easy access
_refresh_manager = None

def get_refresh_manager(config_path: Optional[str] = None) -> BaselineRefreshManager:
    """Get or create global refresh manager instance"""
    global _refresh_manager
    if _refresh_manager is None:
        _refresh_manager = BaselineRefreshManager(config_path)
    return _refresh_manager

def ensure_baseline_available(config_path: Optional[str] = None) -> bool:
    """
    Convenience function to ensure baseline scores are available
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        True if baselines are available, False otherwise
    """
    manager = get_refresh_manager(config_path)
    return manager.ensure_baseline_available()

def start_auto_refresh(config_path: Optional[str] = None):
    """
    Convenience function to start automatic baseline refresh
    
    Args:
        config_path: Path to configuration file
    """
    manager = get_refresh_manager(config_path)
    manager.start_automatic_refresh()

def stop_auto_refresh():
    """Convenience function to stop automatic baseline refresh"""
    global _refresh_manager
    if _refresh_manager:
        _refresh_manager.stop_automatic_refresh()

def get_baseline_status(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Convenience function to get baseline status
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Dictionary with baseline status details
    """
    manager = get_refresh_manager(config_path)
    return manager.get_baseline_status()