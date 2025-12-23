"""
Ollama Client for FAIR-Agent
Provides interface to Ollama models for faster local inference
"""

import requests
import json
import logging
import time
from typing import Optional, Dict, Any
try:
    from src.observability.telemetry import get_telemetry
except ImportError:
    # Fallback for when imported as top-level module
    from observability.telemetry import get_telemetry

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        Initialize Ollama client
        
        Args:
            base_url: Base URL for Ollama API (default: http://localhost:11434)
        """
        self.base_url = base_url
        self.logger = logging.getLogger(__name__)
        self.api_endpoint = f"{base_url}/api/generate"
        self.telemetry = get_telemetry()
        
    def generate(
        self,
        model: str,
        prompt: str,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        stream: bool = False
    ) -> Optional[str]:
        """
        Generate text using Ollama model
        
        Args:
            model: Model name (e.g., 'llama3.2', 'llama3', 'codellama')
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Top-p sampling parameter
            stream: Whether to stream response
            
        Returns:
            Generated text or None if error
        """
        self.telemetry.start_span("ollama_generate", metadata={
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature
        })
        start_time = time.time()
        
        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": stream,
                "options": {
                    "temperature": temperature,
                    "top_p": top_p,
                    "num_predict": max_tokens
                }
            }
            
            self.logger.info(f"Calling Ollama API with model: {model}")
            
            response = requests.post(
                self.api_endpoint,
                json=payload,
                timeout=120  # Increased timeout for complex RAG queries
            )
            
            if response.status_code == 200:
                result_text = ""
                if stream:
                    # Handle streaming response
                    full_text = ""
                    for line in response.iter_lines():
                        if line:
                            data = json.loads(line)
                            if 'response' in data:
                                full_text += data['response']
                    result_text = full_text
                else:
                    # Handle non-streaming response
                    data = response.json()
                    result_text = data.get('response', '')
                
                # Record metrics
                duration = time.time() - start_time
                self.telemetry.record_metric("llm_latency", duration)
                self.telemetry.increment_counter("llm_requests_total")
                
                # Estimate tokens (rough approximation: 4 chars per token)
                estimated_tokens = len(result_text) / 4
                self.telemetry.record_metric("llm_tokens_generated", estimated_tokens)
                
                self.telemetry.end_span("ollama_generate", status="success")
                return result_text
            else:
                self.logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                self.telemetry.increment_counter("llm_errors")
                self.telemetry.end_span("ollama_generate", status="error", error=f"HTTP {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            self.logger.error("Ollama API timeout")
            self.telemetry.increment_counter("llm_timeouts")
            self.telemetry.end_span("ollama_generate", status="error", error="Timeout")
            return None
        except requests.exceptions.ConnectionError:
            self.logger.error("Cannot connect to Ollama - is it running? (ollama serve)")
            self.telemetry.increment_counter("llm_connection_errors")
            self.telemetry.end_span("ollama_generate", status="error", error="ConnectionError")
            return None
        except Exception as e:
            self.logger.error(f"Ollama generation error: {str(e)}")
            self.telemetry.increment_counter("llm_errors")
            self.telemetry.end_span("ollama_generate", status="error", error=str(e))
            return None
    
    def is_available(self) -> bool:
        """
        Check if Ollama service is available
        
        Returns:
            True if Ollama is running and accessible
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def list_models(self) -> list:
        """
        List available Ollama models
        
        Returns:
            List of model names
        """
        try:
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [model['name'] for model in data.get('models', [])]
            return []
        except:
            return []
