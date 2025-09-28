#!/usr/bin/env python3
"""
FAIR-Agent System - Main Entry Point

A comprehensive AI system with specialized Finance and Medical agents,
featuring domain classification, cross-domain reasoning, and FAIR metrics evaluation.

CS668 Analytics Capstone - Fall 2025
Author: Somesh Ghaturle
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.system import FairAgentSystem
from src.utils.logger import setup_logging


def main():
    """Main entry point for FAIR-Agent system"""
    parser = argparse.ArgumentParser(
        description="FAIR-Agent System - AI agents for Finance and Medical domains"
    )
    parser.add_argument(
        "--mode", 
        choices=["web", "cli", "api"], 
        default="web",
        help="Run mode: web interface, CLI, or API only"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=8000,
        help="Port for web interface (default: 8000)"
    )
    parser.add_argument(
        "--debug", 
        action="store_true",
        help="Enable debug mode"
    )
    parser.add_argument(
        "--config", 
        type=str,
        default="config/system_config.yaml",
        help="Path to configuration file"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    log_level = logging.DEBUG if args.debug else logging.INFO
    setup_logging(level=log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting FAIR-Agent System")
    
    try:
        # Initialize the system
        system = FairAgentSystem(config_path=args.config)
        
        if args.mode == "web":
            # Run Django web interface
            system.run_web_interface(port=args.port, debug=args.debug)
        elif args.mode == "cli":
            # Run interactive CLI
            system.run_cli()
        elif args.mode == "api":
            # Run API only
            system.run_api(port=args.port)
            
    except KeyboardInterrupt:
        logger.info("System interrupted by user")
    except Exception as e:
        logger.error(f"System error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()