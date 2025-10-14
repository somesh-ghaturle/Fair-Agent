"""
System Configuration Module for FAIR-Agent

Handles configuration loading and management for the FAIR-Agent system.
"""

import yaml
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class AgentConfig:
    """Configuration for individual agents"""
    model_name: str = "llama3.2:latest"
    device: str = "auto"
    max_length: int = 1024
    temperature: float = 0.7
    top_p: float = 0.9
    alternative_models: list = field(default_factory=list)
    enable_model_switching: bool = False


@dataclass
class SystemConfig:
    """Main system configuration"""
    
    # Agent configurations
    finance_agent: AgentConfig = field(default_factory=AgentConfig)
    medical_agent: AgentConfig = field(default_factory=AgentConfig)
    
    # System settings
    enable_cross_domain: bool = True
    log_level: str = "INFO"
    
    # Web interface settings
    web_host: str = "127.0.0.1"
    web_port: int = 8000
    debug_mode: bool = False
    
    # Database settings
    database_url: str = "sqlite:///fair_agent.db"
    
    # Evaluation settings
    enable_fair_metrics: bool = True
    evaluation_timeout: int = 30
    
    @classmethod
    def load_from_file(cls, config_path: str) -> 'SystemConfig':
        """Load configuration from YAML file"""
        config_file = Path(config_path)
        
        if not config_file.exists():
            logging.warning(f"Config file {config_path} not found, using defaults")
            return cls()
        
        try:
            with open(config_file, 'r') as f:
                config_data = yaml.safe_load(f)
            
            # Create agent configs
            finance_config = AgentConfig(**config_data.get('finance_agent', {}))
            medical_config = AgentConfig(**config_data.get('medical_agent', {}))
            
            # Create system config
            system_data = config_data.get('system', {})
            config = cls(
                finance_agent=finance_config,
                medical_agent=medical_config,
                **system_data
            )
            
            logging.info(f"Configuration loaded from {config_path}")
            return config
            
        except Exception as e:
            logging.error(f"Error loading config from {config_path}: {e}")
            logging.info("Using default configuration")
            return cls()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary"""
        return {
            'finance_agent': {
                'model_name': self.finance_agent.model_name,
                'device': self.finance_agent.device,
                'max_length': self.finance_agent.max_length,
                'temperature': self.finance_agent.temperature,
                'top_p': self.finance_agent.top_p
            },
            'medical_agent': {
                'model_name': self.medical_agent.model_name,
                'device': self.medical_agent.device,
                'max_length': self.medical_agent.max_length,
                'temperature': self.medical_agent.temperature,
                'top_p': self.medical_agent.top_p
            },
            'system': {
                'enable_cross_domain': self.enable_cross_domain,
                'log_level': self.log_level,
                'web_host': self.web_host,
                'web_port': self.web_port,
                'debug_mode': self.debug_mode,
                'database_url': self.database_url,
                'enable_fair_metrics': self.enable_fair_metrics,
                'evaluation_timeout': self.evaluation_timeout
            }
        }
    
    def save_to_file(self, config_path: str):
        """Save configuration to YAML file"""
        config_file = Path(config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)
            
            logging.info(f"Configuration saved to {config_path}")
            
        except Exception as e:
            logging.error(f"Error saving config to {config_path}: {e}")
            raise