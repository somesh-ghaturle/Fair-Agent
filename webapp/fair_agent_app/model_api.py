"""
Model Selection API for FAIR-Agent Web Interface
CS668 Analytics Capstone - Fall 2025

Provides REST API endpoints for model selection and management
"""

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from typing import Dict, Any

from src.core.model_manager import model_manager, ModelType

logger = logging.getLogger(__name__)

@csrf_exempt
@require_http_methods(["GET"])
def get_available_models(request):
    """Get list of available models with their capabilities"""
    try:
        models = model_manager.get_available_models()
        return JsonResponse({
            'success': True,
            'models': models,
            'count': len(models)
        })
    except Exception as e:
        logger.error(f"Error getting available models: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def load_model(request):
    """Load a specific model"""
    try:
        data = json.loads(request.body)
        model_name = data.get('model_name')
        device = data.get('device', 'auto')
        
        if not model_name:
            return JsonResponse({
                'success': False,
                'error': 'model_name is required'
            }, status=400)
        
        # Convert model name to ModelType
        model_type_mapping = {
            'llama3.2:latest': ModelType.LLAMA32_LATEST,
            'mistral:latest': ModelType.MISTRAL_LATEST,
            'phi3:latest': ModelType.PHI3_LATEST,
            'codellama:latest': ModelType.CODELLAMA_LATEST
        }
        
        model_type = model_type_mapping.get(model_name)
        if not model_type:
            return JsonResponse({
                'success': False,
                'error': f'Unsupported model: {model_name}'
            }, status=400)
        
        success = model_manager.load_model(model_type, device)
        
        return JsonResponse({
            'success': success,
            'message': f'Model {model_name} {"loaded successfully" if success else "failed to load"}',
            'model_type': model_name,
            'device': device
        })
        
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def unload_model(request):
    """Unload a specific model"""
    try:
        data = json.loads(request.body)
        model_name = data.get('model_name')
        
        if not model_name:
            return JsonResponse({
                'success': False,
                'error': 'model_name is required'
            }, status=400)
        
        # Convert model name to ModelType
        model_type_mapping = {
            'llama3.2:latest': ModelType.LLAMA32_LATEST,
            'mistral:latest': ModelType.MISTRAL_LATEST,
            'phi3:latest': ModelType.PHI3_LATEST,
            'codellama:latest': ModelType.CODELLAMA_LATEST
        }
        
        model_type = model_type_mapping.get(model_name)
        if model_type:
            model_manager.unload_model(model_type)
            return JsonResponse({
                'success': True,
                'message': f'Model {model_name} unloaded successfully'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': f'Model {model_name} not found'
            }, status=404)
            
    except Exception as e:
        logger.error(f"Error unloading model: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def benchmark_models(request):
    """Benchmark loaded models for FAIR metrics comparison"""
    try:
        data = json.loads(request.body)
        test_prompts = data.get('test_prompts', [
            "What is finance?",
            "Explain investment risk.",
            "How do interest rates affect the economy?"
        ])
        
        results = model_manager.benchmark_models(test_prompts)
        
        return JsonResponse({
            'success': True,
            'benchmark_results': results,
            'test_prompts': test_prompts
        })
        
    except Exception as e:
        logger.error(f"Error benchmarking models: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["GET"])
def get_model_capabilities(request):
    """Get FAIR metric capabilities for all loaded models"""
    try:
        capabilities = {}
        
        for model_type, model_info in model_manager.loaded_models.items():
            capabilities[model_type.value] = {
                'capabilities': model_info['capabilities'],
                'config': {
                    'name': model_info['config'].model_name,
                    'memory_gb': model_info['config'].memory_requirement_gb,
                    'max_length': model_info['config'].recommended_max_length,
                    'supports_chat': model_info['config'].supports_chat
                }
            }
        
        return JsonResponse({
            'success': True,
            'capabilities': capabilities,
            'loaded_models_count': len(capabilities)
        })
        
    except Exception as e:
        logger.error(f"Error getting model capabilities: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def test_model_response(request):
    """Test a specific model with a query"""
    try:
        data = json.loads(request.body)
        model_name = data.get('model_name')
        query = data.get('query', 'What is finance?')
        
        if not model_name:
            return JsonResponse({
                'success': False,
                'error': 'model_name is required'
            }, status=400)
        
        # Convert model name to ModelType
        model_type_mapping = {
            'llama3.2:latest': ModelType.LLAMA32_LATEST,
            'mistral:latest': ModelType.MISTRAL_LATEST,
            'phi3:latest': ModelType.PHI3_LATEST,
            'codellama:latest': ModelType.CODELLAMA_LATEST
        }
        
        model_type = model_type_mapping.get(model_name)
        if not model_type:
            return JsonResponse({
                'success': False,
                'error': f'Unsupported model: {model_name}'
            }, status=400)
        
        # Generate response
        response = model_manager.generate_response(
            model_type,
            f"Question: {query}\n\nAnswer:",
            max_new_tokens=150,
            temperature=0.7
        )
        
        if response.get('success'):
            return JsonResponse({
                'success': True,
                'query': query,
                'response': response['generated_text'],
                'model_type': model_name,
                'capabilities': response.get('capabilities', {})
            })
        else:
            return JsonResponse({
                'success': False,
                'error': response.get('error', 'Generation failed')
            }, status=500)
            
    except Exception as e:
        logger.error(f"Error testing model response: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)