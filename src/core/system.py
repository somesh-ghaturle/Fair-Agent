"""
Main System Module for FAIR-Agent

Integrates all components and provides different interface modes.
"""

import os
import sys
import logging
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

from .config import SystemConfig
from ..agents.orchestrator import Orchestrator
from ..utils.logger import setup_logging


class FairAgentSystem:
    """
    Main FAIR-Agent System class
    
    Coordinates all system components and provides different interface modes.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the FAIR-Agent system
        
        Args:
            config_path: Path to configuration file
        """
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        if config_path:
            self.config = SystemConfig.load_from_file(config_path)
        else:
            self.config = SystemConfig()
        
        # Initialize orchestrator
        self.orchestrator = None
        self._initialize_orchestrator()
    
    def _initialize_orchestrator(self):
        """Initialize the orchestrator with agents"""
        try:
            finance_config = {
                'model_name': self.config.finance_agent.model_name,
                'device': self.config.finance_agent.device,
                'max_length': self.config.finance_agent.max_length
            }
            
            medical_config = {
                'model_name': self.config.medical_agent.model_name,
                'device': self.config.medical_agent.device,
                'max_length': self.config.medical_agent.max_length
            }
            
            self.orchestrator = Orchestrator(
                finance_config=finance_config,
                medical_config=medical_config,
                enable_cross_domain=self.config.enable_cross_domain,
                enable_knowledge_graph=True  # Enable knowledge graph by default
            )
            
            self.logger.info("FAIR-Agent system initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize system: {e}")
            raise
    
    def _initialize_baseline_refresh(self):
        """Initialize baseline auto-refresh system"""
        try:
            from ..evaluation.baseline_refresh import start_auto_refresh
            
            # Start automatic baseline refresh
            start_auto_refresh()
            self.logger.info("Baseline auto-refresh system started")
            
        except Exception as e:
            self.logger.warning(f"Could not start baseline auto-refresh: {e}")
            self.logger.warning("Baseline scores will use manual refresh only")
    
    def process_query(self, query: str, context: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Process a query through the system
        
        Args:
            query: The user query
            context: Optional context information
            
        Returns:
            Dictionary with response and metadata
        """
        if not self.orchestrator:
            raise RuntimeError("System not properly initialized")
        
        try:
            response = self.orchestrator.process_query(query, context)
            
            return {
                'answer': response.primary_answer,
                'domain': response.domain.value,
                'confidence': response.confidence_score,
                'routing_explanation': response.routing_explanation,
                'finance_response': response.finance_response,
                'medical_response': response.medical_response,
                'cross_domain_analysis': response.cross_domain_analysis
            }
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return {
                'answer': f"Error processing query: {str(e)}",
                'domain': 'error',
                'confidence': 0.0,
                'routing_explanation': f"System error: {str(e)}"
            }
    
    def run_web_interface(self, port: Optional[int] = None, debug: bool = False):
        """
        Run the web interface using Django
        
        Args:
            port: Port number (defaults to config value)
            debug: Enable debug mode
        """
        port = port or self.config.web_port
        debug = debug or self.config.debug_mode
        
        self.logger.info(f"Starting web interface on port {port}")
        
        # Set environment variables for Django
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')
        os.environ['FAIR_AGENT_PORT'] = str(port)
        os.environ['FAIR_AGENT_DEBUG'] = str(debug)
        
        # Change to webapp directory
        webapp_dir = Path(__file__).parent.parent.parent / 'webapp'
        original_cwd = os.getcwd()
        
        try:
            os.chdir(webapp_dir)
            
            # Run Django development server
            cmd = [
                sys.executable, 
                'manage.py', 
                'runserver', 
                f"{self.config.web_host}:{port}"
            ]
            
            if debug:
                cmd.append('--debug')
            
            subprocess.run(cmd)
            
        except KeyboardInterrupt:
            self.logger.info("Web interface stopped by user")
        except Exception as e:
            self.logger.error(f"Error running web interface: {e}")
            raise
        finally:
            os.chdir(original_cwd)
    
    def run_cli(self):
        """Run interactive command-line interface"""
        self.logger.info("Starting CLI interface")
        
        print("=" * 60)
        print("FAIR-Agent System - Interactive CLI")
        print("=" * 60)
        print("Enter your queries below. Type 'quit' or 'exit' to stop.")
        print("Commands:")
        print("  help    - Show this help")
        print("  status  - Show system status")
        print("  config  - Show configuration")
        print("=" * 60)
        
        while True:
            try:
                query = input("\n> ").strip()
                
                if query.lower() in ['quit', 'exit', 'q']:
                    print("Goodbye!")
                    break
                
                elif query.lower() == 'help':
                    print("\nAvailable commands:")
                    print("  help    - Show this help")
                    print("  status  - Show system status")
                    print("  config  - Show configuration")
                    print("  quit    - Exit the CLI")
                    print("\nOr enter any query for analysis by the FAIR-Agent system.")
                    continue
                
                elif query.lower() == 'status':
                    print(f"\nSystem Status:")
                    print(f"  Orchestrator: {'Initialized' if self.orchestrator else 'Not initialized'}")
                    print(f"  Cross-domain: {'Enabled' if self.config.enable_cross_domain else 'Disabled'}")
                    print(f"  FAIR metrics: {'Enabled' if self.config.enable_fair_metrics else 'Disabled'}")
                    continue
                
                elif query.lower() == 'config':
                    print(f"\nConfiguration:")
                    print(f"  Finance model: {self.config.finance_agent.model_name}")
                    print(f"  Medical model: {self.config.medical_agent.model_name}")
                    print(f"  Log level: {self.config.log_level}")
                    continue
                
                elif not query:
                    continue
                
                # Process the query
                print(f"\nProcessing: {query}")
                print("-" * 40)
                
                result = self.process_query(query)
                
                print(f"Domain: {result['domain']}")
                print(f"Confidence: {result['confidence']:.2f}")
                print(f"Answer: {result['answer']}")
                
                if result.get('routing_explanation'):
                    print(f"Routing: {result['routing_explanation']}")
                
            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def run_api(self, port: Optional[int] = None):
        """
        Run API-only mode (future implementation)
        
        Args:
            port: Port number for API
        """
        port = port or self.config.web_port
        self.logger.info(f"API-only mode not yet implemented. Use web mode on port {port}")
        raise NotImplementedError("API-only mode will be implemented in future versions")
    
    def get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            'system': 'FAIR-Agent',
            'version': '1.0.0',
            'status': 'running' if self.orchestrator else 'error',
            'config': self.config.to_dict(),
            'agents': {
                'finance': self.config.finance_agent.model_name,
                'medical': self.config.medical_agent.model_name
            }
        }