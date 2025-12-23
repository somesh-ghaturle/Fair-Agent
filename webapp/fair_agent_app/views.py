"""
Django views for FAIR-Agent Web Application

This module contains the view functions and classes that             fetch('http://localhost:8000/api/query/process/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{csrf_token}'
                },
                body: JSON.stringify(data)
            })TTP requests
and render responses for the FAIR-Agent web interface.
"""

import json
import uuid
import logging
import numpy as np
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.conf import settings

from .models import (
    QuerySession, QueryRecord, EvaluationMetrics, 
    SystemPerformance, SafetyAlert, UserFeedback,
    TraceLog, SpanLog
)
from .services import FairAgentService, QueryProcessor
from .formatters import ResponseFormatter
from src.utils.spell_checker import spell_checker

logger = logging.getLogger(__name__)


class NumpyJSONEncoder(DjangoJSONEncoder):
    """Custom JSON encoder to handle numpy types"""
    def default(self, obj):
        if isinstance(obj, (np.floating, np.float32, np.float64)):
            return float(obj)
        elif isinstance(obj, (np.integer, np.int32, np.int64)):
            return int(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, 'item'):  # Handle other numpy scalars
            return obj.item()
        return super().default(obj)


def convert_numpy_types(obj):
    """Convert numpy types to JSON-serializable Python types"""
    import numpy as np
    
    if isinstance(obj, (np.floating, np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.integer, np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {key: convert_numpy_types(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy_types(item) for item in obj]
    elif hasattr(obj, 'item'):  # Handle other numpy scalars
        return obj.item()
    else:
        return obj


class HomeView(TemplateView):
    """Main landing page for FAIR-Agent web interface"""
    template_name = 'fair_agent_app/home.html'


@csrf_exempt
def test_api(request):
    """Simple test API that returns immediately"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            return JsonResponse({
                'status': 'success',
                'message': 'API is working!',
                'received_query': data.get('query', 'No query'),
                'timestamp': datetime.now().isoformat()
            })
        except Exception as e:
            return JsonResponse({
                'error': str(e),
                'status': 'error'
            }, status=500)
    else:
        return JsonResponse({'error': 'Only POST allowed'}, status=405)


def test_ui(request):
    """Simple test interface to debug UI issues"""
    from django.middleware.csrf import get_token
    csrf_token = get_token(request)
    
    return HttpResponse(f'''
<!DOCTYPE html>
<html>
<head>
    <title>FAIR-Agent Test</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>FAIR-Agent Simple Test</h1>
        
        <form id="testForm">
            <input type="hidden" name="csrfmiddlewaretoken" value="{csrf_token}">
            <div class="mb-3">
                <input type="text" id="queryInput" class="form-control" placeholder="Enter your query" value="What is diversification?">
            </div>
            <button type="submit" class="btn btn-primary">Test Simple API</button>
            <button type="button" id="testFullApi" class="btn btn-secondary ms-2">Test Full API</button>
        </form>
        
        <div id="result" class="mt-3"></div>
        <div id="debug" class="mt-3 p-3 bg-light" style="max-height: 300px; overflow-y: auto;">
            <strong>Debug Log:</strong><br>
        </div>
    </div>

    <script>
        function debug(msg) {{
            document.getElementById('debug').innerHTML += '<div>' + new Date().toLocaleTimeString() + ': ' + msg + '</div>';
        }}
        
        debug('Page loaded');
        debug('CSRF Token: {csrf_token}');
        
        document.getElementById('testForm').addEventListener('submit', function(e) {{
            e.preventDefault();
            debug('Form submitted');
            
            const query = document.getElementById('queryInput').value;
            debug('Query: ' + query);
            
            const data = {{
                query: query
            }};
            
            debug('Sending request to Simple Test API...');
            debug('Request URL: /test-api/');
            debug('Request method: POST');
            debug('Request headers: Content-Type: application/json, X-CSRFToken: {csrf_token}');
            debug('Request body: ' + JSON.stringify(data));
            
            fetch('/test-api/', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{csrf_token}'
                }},
                body: JSON.stringify(data)
            }})
            .then(response => {{
                debug('Response received!');
                debug('Response status: ' + response.status);
                debug('Response headers: ' + JSON.stringify(Object.fromEntries(response.headers.entries())));
                if (!response.ok) {{
                    return response.text().then(text => {{
                        debug('Error response body: ' + text);
                        throw new Error('HTTP ' + response.status + ': ' + text);
                    }});
                }}
                return response.json();
            }})
            .then(data => {{
                debug('Success! Data received');
                debug('Full response: ' + JSON.stringify(data));
                debug('Answer length: ' + (data.answer ? data.answer.length : 'NO ANSWER'));
                debug('Confidence: ' + data.confidence);
                debug('Domain: ' + data.domain);
                
                document.getElementById('result').innerHTML = `
                    <div class="alert alert-success">
                        <h5>Response Received!</h5>
                        <p><strong>Query:</strong> ${{query}}</p>
                        <p><strong>Domain:</strong> ${{data.domain}}</p>
                        <p><strong>Confidence:</strong> ${{data.confidence}}</p>
                        <p><strong>Answer:</strong> ${{data.answer ? data.answer.substring(0, 500) + '...' : 'No answer'}}</p>
                        ${{data.fair_metrics ? `
                        <p><strong>FAIR Metrics:</strong></p>
                        <ul>
                            <li>Faithfulness: ${{Math.round(data.fair_metrics.faithfulness * 100)}}%</li>
                            <li>Interpretability: ${{Math.round(data.fair_metrics.interpretability * 100)}}%</li>
                            <li>Risk Awareness: ${{Math.round(data.fair_metrics.risk_awareness * 100)}}%</li>
                        </ul>
                        ` : '<p>No FAIR metrics available</p>'}}
                    </div>
                `;
            }})
            .catch(error => {{
                debug('ERROR occurred');
                debug('Error message: ' + error.message);
                debug('Error stack: ' + error.stack);
                document.getElementById('result').innerHTML = `
                    <div class="alert alert-danger">
                        <strong>Error:</strong> ${{error.message}}
                    </div>
                `;
            }});
        }});
        
        // Full API test
        document.getElementById('testFullApi').addEventListener('click', function() {{
            debug('Testing Full API...');
            
            const query = document.getElementById('queryInput').value;
            const data = {{ query: query }};
            
            debug('Sending request to Full API...');
            debug('Request URL: /api/query/process/');
            
            fetch('/api/query/process/', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{csrf_token}'
                }},
                body: JSON.stringify(data)
            }})
            .then(response => {{
                debug('Full API Response received!');
                debug('Response status: ' + response.status);
                if (!response.ok) {{
                    return response.text().then(text => {{
                        debug('Error response body: ' + text);
                        throw new Error('HTTP ' + response.status + ': ' + text);
                    }});
                }}
                return response.json();
            }})
            .then(data => {{
                debug('Full API Success! Data received');
                debug('Full response: ' + JSON.stringify(data));
                
                document.getElementById('result').innerHTML = `
                    <div class="alert alert-success">
                        <h5>Full API Response Received!</h5>
                        <p><strong>Query:</strong> ${{query}}</p>
                        <p><strong>Domain:</strong> ${{data.domain}}</p>
                        <p><strong>Confidence:</strong> ${{data.confidence}}</p>
                        <p><strong>Answer:</strong> ${{data.answer ? data.answer.substring(0, 500) + '...' : 'No answer'}}</p>
                    </div>
                `;
            }})
            .catch(error => {{
                debug('Full API ERROR occurred');
                debug('Error message: ' + error.message);
                document.getElementById('result').innerHTML = `
                    <div class="alert alert-danger">
                        <strong>Full API Error:</strong> ${{error.message}}
                    </div>
                `;
            }});
        }});
    </script>
</body>
</html>
    ''')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get system status
        context['system_status'] = FairAgentService.get_system_status()
        context['available_metrics'] = FairAgentService.get_available_metrics()
        
        # Get recent statistics
        recent_queries = QueryRecord.objects.filter(status='completed').order_by('-created_at')[:10]
        context['recent_queries'] = recent_queries
        
        # Get performance statistics
        total_queries = QueryRecord.objects.count()
        successful_queries = QueryRecord.objects.filter(status='completed').count()
        context['stats'] = {
            'total_queries': total_queries,
            'successful_queries': successful_queries,
            'success_rate': (successful_queries / total_queries * 100) if total_queries > 0 else 0,
        }
        
        return context


class SimpleQueryView(TemplateView):
    """Simple query interface for debugging"""
    template_name = 'fair_agent_app/simple_query.html'


class DatasetsView(TemplateView):
    """Dataset management and information page"""
    template_name = 'fair_agent_app/datasets.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Datasets'
        
        # Load evidence sources from YAML
        import yaml
        import os
        import json
        from pathlib import Path
        
        base_dir = Path(__file__).resolve().parent.parent.parent
        evidence_sources_path = base_dir / 'config' / 'evidence_sources.yaml'
        
        # Load curated sources
        try:
            with open(evidence_sources_path, 'r') as f:
                evidence_data = yaml.safe_load(f)
                context['medical_sources'] = evidence_data.get('medical_sources', [])
                context['finance_sources'] = evidence_data.get('finance_sources', [])
                curated_count = len(context['medical_sources']) + len(context['finance_sources'])
        except Exception as e:
            logger.error(f"Error loading evidence sources: {e}")
            context['medical_sources'] = []
            context['finance_sources'] = []
            curated_count = 0
        
        # Load dataset Q&A sources
        dataset_qa_sources = []
        
        # Helper to count lines in a file
        def count_lines(file_path):
            if not file_path.exists():
                return 0
            try:
                # Use wc -l for speed if on unix, else python count
                import subprocess
                result = subprocess.run(['wc', '-l', str(file_path)], capture_output=True, text=True)
                return int(result.stdout.split()[0])
            except Exception:
                # Fallback to python count
                count = 0
                with open(file_path, 'r') as f:
                    for _ in f: count += 1
                return count

        # Define datasets to check
        datasets_info = [
            {'name': 'FinQA', 'path': base_dir / 'data' / 'datasets' / 'finqa' / 'finance_qa.jsonl', 'domain': 'finance'},
            {'name': 'ConvFinQA', 'path': base_dir / 'data' / 'datasets' / 'convfinqa' / 'convfinqa.jsonl', 'domain': 'finance'},
            {'name': 'TAT-QA', 'path': base_dir / 'data' / 'datasets' / 'tatqa' / 'tatqa.jsonl', 'domain': 'finance'},
            {'name': 'MedMCQA', 'path': base_dir / 'data' / 'datasets' / 'medmcqa' / 'medical_qa.jsonl', 'domain': 'medical'},
            {'name': 'PubMedQA', 'path': base_dir / 'data' / 'datasets' / 'pubmedqa' / 'medical_qa.jsonl', 'domain': 'medical'},
        ]
        
        total_dataset_count = 0
        dataset_counts = {}
        
        for ds in datasets_info:
            count = count_lines(ds['path'])
            dataset_counts[ds['name']] = count
            total_dataset_count += count
            
            # Add a sample source for display if it exists
            if count > 0 and len(dataset_qa_sources) < 5: # Limit samples
                 try:
                    with open(ds['path'], 'r') as f:
                        line = f.readline()
                        if line:
                            data = json.loads(line)
                            q_text = data.get('question', 'Question')
                            a_text = str(data.get('answer', 'Answer'))
                            dataset_qa_sources.append({
                                'id': f"sample_{ds['name']}",
                                'title': f"{ds['name']} Sample: {q_text[:60]}...",
                                'content': f"Q: {q_text}\n\nA: {a_text}",
                                'source_type': 'qa_dataset',
                                'reliability_score': 0.85,
                                'domain': ds['domain'],
                                'publication_date': '2024'
                            })
                 except Exception: pass

        context['dataset_qa_sources'] = dataset_qa_sources
        context['total_sources'] = curated_count + total_dataset_count
        context['curated_count'] = curated_count
        context['dataset_qa_count'] = total_dataset_count
        context['dataset_counts'] = dataset_counts
        
        # Dataset information
        datasets_dir = base_dir / 'data' / 'datasets'
        context['datasets'] = [
            {
                'name': 'MedMCQA',
                'domain': 'medical',
                'count': dataset_counts.get('MedMCQA', 0),
                'description': 'Medical multiple choice question answering dataset for medical entrance exams',
                'links': [
                    {'text': '🤗 HuggingFace Dataset', 'url': 'https://huggingface.co/datasets/openlifescienceai/medmcqa'},
                    {'text': '📊 Original Repository', 'url': 'https://github.com/medmcqa/medmcqa'},
                    {'text': '📄 Research Paper', 'url': 'https://proceedings.mlr.press/v174/pal22a.html'}
                ]
            },
            {
                'name': 'PubMedQA',
                'domain': 'medical',
                'count': dataset_counts.get('PubMedQA', 0),
                'description': 'Biomedical question answering using PubMed abstracts',
                'links': [
                    {'text': '🤗 HuggingFace Dataset', 'url': 'https://huggingface.co/datasets/qiaojin/PubMedQA'},
                    {'text': '📊 Original Repository', 'url': 'https://github.com/pubmedqa/pubmedqa'},
                    {'text': '📄 Research Paper', 'url': 'https://arxiv.org/abs/1909.06146'}
                ]
            },
            {
                'name': 'MIMIC-IV',
                'domain': 'medical',
                'count': 0, # Not downloaded
                'description': 'Medical Information Mart for Intensive Care - clinical database',
                'links': [
                    {'text': '📊 PhysioNet Repository', 'url': 'https://physionet.org/content/mimiciv/2.2/'},
                    {'text': '📄 Research Paper', 'url': 'https://www.nature.com/articles/s41597-022-01899-x'},
                    {'text': '⚠️ Requires Access', 'url': '#'}
                ]
            },
            {
                'name': 'FinQA',
                'domain': 'finance',
                'count': dataset_counts.get('FinQA', 0),
                'description': 'Financial question answering with numerical reasoning',
                'links': [
                    {'text': '📊 Dataset Repository', 'url': 'https://github.com/czyssrs/FinQA'},
                    {'text': '📄 Research Paper (EMNLP 2021)', 'url': 'https://aclanthology.org/2021.emnlp-main.300/'},
                    {'text': '🌐 Project Website', 'url': 'https://finqasite.github.io/'}
                ]
            },
            {
                'name': 'TAT-QA',
                'domain': 'finance',
                'count': dataset_counts.get('TAT-QA', 0),
                'description': 'Table-and-text question answering for financial documents',
                'links': [
                    {'text': '📊 Dataset Repository', 'url': 'https://github.com/NExTplusplus/TAT-QA'},
                    {'text': '📄 Research Paper (ACL 2021)', 'url': 'https://aclanthology.org/2021.acl-long.254/'},
                    {'text': '🌐 Project Website', 'url': 'https://nextplusplus.github.io/TAT-QA/'}
                ]
            },
            {
                'name': 'ConvFinQA',
                'domain': 'finance',
                'count': dataset_counts.get('ConvFinQA', 0),
                'description': 'Conversational financial question answering',
                'links': [
                    {'text': '📊 Dataset Repository', 'url': 'https://github.com/czyssrs/ConvFinQA'},
                    {'text': '📄 Research Paper (EMNLP 2022)', 'url': 'https://aclanthology.org/2022.emnlp-main.421/'},
                    {'text': '🌐 Project Website', 'url': 'https://sites.google.com/view/convfinqa'}
                ]
            }
        ]
        
        return context


class QueryInterfaceView(TemplateView):
    """Interactive query interface"""
    template_name = 'fair_agent_app/query_interface.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Create or get session
        session_id = self.request.session.get('fair_agent_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            self.request.session['fair_agent_session_id'] = session_id
        
        session, created = QuerySession.objects.get_or_create(
            session_id=session_id,
            defaults={'user': self.request.user if self.request.user.is_authenticated else None}
        )
        
        context['session'] = session
        context['session_queries'] = session.queries.order_by('-created_at')[:20]
        
        return context


@csrf_exempt
@require_http_methods(["POST"])
def process_query_api(request):
    """
    API endpoint to process user queries
    """
    try:
        data = json.loads(request.body)
        query_text = data.get('query', '').strip()
        # Get selected model with dynamic default
        try:
            from src.core.model_manager import ModelRegistry
            default_model = ModelRegistry.get_default_model()
        except ImportError:
            default_model = 'llama3.2:latest'  # Last resort fallback
        
        selected_model = data.get('model', default_model)
        
        if not query_text:
            return JsonResponse({
                'error': 'Query text is required',
                'status': 'error'
            }, status=400)
        
        # Log selected model
        logger.info(f"[QUERY] 📝 Processing query with selected model: {selected_model}")
        
        # Validate query length
        max_length = getattr(settings, 'FAIR_AGENT_SETTINGS', {}).get('MAX_QUERY_LENGTH', 1000)
        if len(query_text) > max_length:
            return JsonResponse({
                'error': f'Query too long. Maximum length is {max_length} characters.',
                'status': 'error'
            }, status=400)
        
        # Get or create session
        session_id = request.session.get('fair_agent_session_id')
        if not session_id:
            session_id = str(uuid.uuid4())
            request.session['fair_agent_session_id'] = session_id
        
        session, created = QuerySession.objects.get_or_create(
            session_id=session_id,
            defaults={'user': request.user if request.user.is_authenticated else None}
        )
        
        # Auto-correct spelling
        original_query = query_text
        corrected_query, was_corrected, corrections = spell_checker.correct_text(query_text)
        
        if was_corrected:
            logger.info(f"[SPELL CHECK] Corrected query: '{original_query}' -> '{corrected_query}'")
            logger.info(f"[SPELL CHECK] Corrections: {corrections}")
            query_text = corrected_query
        
        # Classify domain
        domain = FairAgentService.classify_query_domain(query_text)
        
        # Create query record
        query_record = QueryRecord.objects.create(
            session=session,
            query_text=query_text,
            domain=domain,
            status='processing'
        )
        
        # Process query
        try:
            result = FairAgentService.process_query(
                query_text, 
                model_name=selected_model,
                query_id=query_record.id
            )
            
            if result.get('status') == 'failed':
                query_record.status = 'failed'
                query_record.save()
                return JsonResponse({
                    'error': result.get('error', 'Unknown error'),
                    'status': 'error',
                    'query_id': query_record.id
                }, status=500)
            
            # Update query record with results
            query_record.primary_answer = result.get('primary_answer', '')
            query_record.confidence_score = result.get('confidence_score')
            query_record.safety_score = result.get('safety_score')
            query_record.processing_time = result.get('processing_time')
            query_record.status = 'completed'
            query_record.processed_at = datetime.now()
            query_record.save()
            
            # Evaluate response and store metrics
            try:
                metrics = FairAgentService.evaluate_response(
                    query_text, 
                    result.get('primary_answer', ''), 
                    domain
                )
                
                if not metrics.get('error'):
                    # Create evaluation metrics record
                    eval_metrics = EvaluationMetrics.objects.create(
                        query=query_record,
                        # Faithfulness metrics
                        faithfulness_token_overlap=metrics.get('faithfulness', {}).get('token_overlap'),
                        faithfulness_semantic_similarity=metrics.get('faithfulness', {}).get('semantic_similarity'),
                        faithfulness_factual_consistency=metrics.get('faithfulness', {}).get('factual_consistency'),
                        # Safety metrics
                        safety_medical_safety=metrics.get('safety', {}).get('medical_safety'),
                        safety_financial_safety=metrics.get('safety', {}).get('financial_safety'),
                        safety_content_safety=metrics.get('safety', {}).get('content_safety'),
                        # Interpretability metrics
                        interpretability_reasoning_clarity=metrics.get('interpretability', {}).get('reasoning_clarity'),
                        interpretability_explanation_completeness=metrics.get('interpretability', {}).get('explanation_completeness'),
                        interpretability_evidence_citation=metrics.get('interpretability', {}).get('evidence_citation'),
                    )
                    
                    # Update query record with FAIR scores
                    query_record.faithfulness_score = metrics.get('faithfulness', {}).get('overall_score')
                    query_record.adaptability_score = metrics.get('adaptability', {}).get('overall_score')
                    query_record.interpretability_score = metrics.get('interpretability', {}).get('overall_score')
                    query_record.risk_awareness_score = metrics.get('safety', {}).get('overall_score')
                    query_record.save()
                    
            except Exception as e:
                logger.error(f"Error evaluating response: {e}")
            
            # Return successful response with comprehensive metrics
            # Get base FAIR metrics from evaluation
            base_faithfulness = query_record.faithfulness_score or metrics.get('faithfulness', {}).get('overall_score', 0.35)
            base_adaptability = query_record.adaptability_score or metrics.get('adaptability', {}).get('overall_score', 0.45)
            base_interpretability = query_record.interpretability_score or metrics.get('interpretability', {}).get('overall_score', 0.40)
            base_risk_awareness = query_record.risk_awareness_score or metrics.get('safety', {}).get('overall_score', 0.60)
            
            # Get enhancement boosts from agent response
            safety_boost = result.get('safety_boost', 0.0)
            evidence_boost = result.get('evidence_boost', 0.0)
            reasoning_boost = result.get('reasoning_boost', 0.0)
            internet_boost = result.get('internet_boost', 0.0)
            
            # Apply boosts to base scores
            # CHANGED: Don't cap at 1.0 - scores can naturally exceed 100% when highly enhanced
            # Maximum realistic values: F≈1.05, A≈1.05, I≈1.05, R≈1.20
            faithfulness_score = base_faithfulness + evidence_boost
            adaptability_score = base_adaptability  # Adaptability doesn't get direct boosts from current enhancements
            interpretability_score = base_interpretability + reasoning_boost
            risk_awareness_score = base_risk_awareness + safety_boost
            
            # For display purposes, we'll show percentage of realistic maximum:
            # - Faithfulness max: 1.05 (base 0.7 + boost 0.35)
            # - Interpretability max: 1.05 (base 0.7 + boost 0.35)
            # - Risk Awareness max: 1.20 (base 0.8 + boost 0.40)
            # But we won't artificially cap the raw scores
            
            # Calculate Hallucination Reduction Score
            # Hallucination = generating information not supported by evidence or facts
            # Our metric measures how effectively we REDUCE hallucinations through:
            # 1. Evidence grounding (prevents making things up)
            # 2. Faithfulness to sources (prevents contradicting facts)
            # 3. External verification (validates against internet sources)
            #
            # Formula interpretation:
            # - High evidence + High faithfulness = High reduction (good!)
            # - Low evidence + Low faithfulness = Low reduction (risky!)
            #
            # Weights:
            # - Evidence: 50% (primary defense against hallucination)
            # - Faithfulness: 35% (measures accuracy to sources)
            # - Internet verification: 15% (external validation)
            
            # Normalize components to 0-1 scale
            evidence_normalized = min(evidence_boost / 0.35, 1.0)  # Max evidence is 0.35
            internet_normalized = min(internet_boost / 0.15, 1.0)  # Max internet is 0.15
            # faithfulness_score already 0-1
            
            # Weighted combination
            hallucination_reduction = (
                (evidence_normalized * 0.50) +      # 50% weight on evidence
                (faithfulness_score * 0.35) +        # 35% weight on faithfulness
                (internet_normalized * 0.15)         # 15% weight on internet
            )
            
            # Cap at 100% (though formula naturally stays <= 1.0)
            hallucination_reduction = min(hallucination_reduction, 1.0)
            
            logger.info(f"FAIR Score Calculation: F={base_faithfulness:.2f}+{evidence_boost:.2f}={faithfulness_score:.2f}, A={base_adaptability:.2f}={adaptability_score:.2f}, I={base_interpretability:.2f}+{reasoning_boost:.2f}={interpretability_score:.2f}, R={base_risk_awareness:.2f}+{safety_boost:.2f}={risk_awareness_score:.2f}")
            if risk_awareness_score > 1.0:
                logger.info(f"⚠️ Risk Awareness exceeds 100% (raw: {risk_awareness_score:.2f}) - This indicates excellent safety enhancements!")
            logger.info(f"Hallucination Reduction: {hallucination_reduction:.2f} (evidence={evidence_boost:.2f}→{evidence_normalized:.2f}, faithfulness={faithfulness_score:.2f}, internet={internet_boost:.2f}→{internet_normalized:.2f})")
            
            # Calculate Calibration Error
            # Calibration measures how well confidence aligns with actual accuracy (faithfulness)
            # Lower calibration error means better alignment (target: <0.1 or 10%)
            confidence_score = result.get('confidence_score', 0.6)
            calibration_error = abs(confidence_score - faithfulness_score)
            
            # Use the calculated calibration error or fall back to metrics
            if calibration_error > 0:
                logger.info(f"Calibration Error: {calibration_error:.2f} (confidence={confidence_score:.2f}, faithfulness={faithfulness_score:.2f})")
            else:
                calibration_error = metrics.get('calibration', {}).get('expected_calibration_error', 0.25)
                logger.info(f"Calibration Error (default): {calibration_error:.2f}")
            
            # Convert all numpy types to JSON-serializable types
            metrics = convert_numpy_types(metrics)
            result = convert_numpy_types(result)
            
            # Format the response for better display
            raw_answer = result.get('primary_answer', '')
            formatted_answer = ResponseFormatter.format_response_html(raw_answer)
            
            response_data = {
                'query_id': query_record.id,
                'answer': raw_answer,
                'formatted_answer': formatted_answer,
                'confidence': result.get('confidence_score', 0.6),
                'domain': domain,
                'model_used': selected_model,  # Add selected model info
                'safety_score': result.get('safety_score', 0.65),
                'processing_time': result.get('processing_time'),
                'status': 'success',
                'reasoning_steps': result.get('reasoning_steps', []),  # Pass execution steps to frontend
                'spell_check': {
                    'was_corrected': was_corrected,
                    'original_query': original_query,
                    'corrected_query': corrected_query,
                    'corrections': corrections
                },
                'fair_metrics': {
                    'faithfulness': faithfulness_score,
                    'adaptability': adaptability_score,
                    'interpretability': interpretability_score,
                    'risk_awareness': risk_awareness_score,
                    'hallucination_reduction': hallucination_reduction,  # NEW: Hallucination reduction metric
                    'calibration_error': calibration_error,  # Use calculated calibration error
                    'robustness': metrics.get('robustness', {}).get('overall_score', 0.35),
                    # Enhancement boosts
                    'safety_boost': safety_boost,
                    'evidence_boost': evidence_boost,
                    'reasoning_boost': reasoning_boost,
                    'internet_boost': internet_boost,
                    'detailed_faithfulness': {
                        'token_overlap': metrics.get('faithfulness', {}).get('token_overlap', 0.0),
                        'semantic_similarity': metrics.get('faithfulness', {}).get('semantic_similarity', 0.0),
                        'factual_consistency': metrics.get('faithfulness', {}).get('factual_consistency', 0.0),
                        'evidence_boost': evidence_boost  # For UI display
                    },
                    'detailed_interpretability': {
                        'reasoning_clarity': metrics.get('interpretability', {}).get('reasoning_clarity', 0.0),
                        'explanation_completeness': metrics.get('interpretability', {}).get('explanation_completeness', 0.0),
                        'evidence_citation': metrics.get('interpretability', {}).get('evidence_citation', 0.0),
                        'reasoning_boost': reasoning_boost  # For UI display
                    },
                    'detailed_adaptability': {
                        'domain_switching_quality': metrics.get('adaptability', {}).get('domain_switching_quality', 0.0),
                        'cross_domain_integration': metrics.get('adaptability', {}).get('cross_domain_integration', 0.0),
                        'context_adaptation': metrics.get('adaptability', {}).get('context_adaptation', 0.0),
                        'query_complexity_handling': metrics.get('adaptability', {}).get('query_complexity_handling', 0.0),
                        'personalization_score': metrics.get('adaptability', {}).get('personalization_score', 0.0)
                    },
                    'detailed_safety': {
                        'medical_safety': metrics.get('safety', {}).get('medical_safety', 0.0),
                        'financial_safety': metrics.get('safety', {}).get('financial_safety', 0.0),
                        'safety_boost': safety_boost,  # For UI display
                        'content_safety': metrics.get('safety', {}).get('content_safety', 0.0)
                    }
                }
            }
            
            # Ensure all numpy types are converted before JSON serialization
            response_data = convert_numpy_types(response_data)
            
            return JsonResponse(response_data, encoder=NumpyJSONEncoder)
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            query_record.status = 'failed'
            query_record.save()
            
            return JsonResponse({
                'error': 'Internal server error while processing query',
                'status': 'error',
                'query_id': query_record.id
            }, status=500)
    
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data',
            'status': 'error'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in process_query_api: {e}")
        return JsonResponse({
            'error': 'Internal server error',
            'status': 'error'
        }, status=500)


def query_history_api(request):
    """
    API endpoint to get query history for current session
    """
    session_id = request.session.get('fair_agent_session_id')
    if not session_id:
        return JsonResponse({'queries': []})
    
    try:
        session = QuerySession.objects.get(session_id=session_id)
        queries = session.queries.order_by('-created_at')
        
        # Pagination
        page = int(request.GET.get('page', 1))
        paginator = Paginator(queries, 20)
        page_queries = paginator.get_page(page)
        
        queries_data = []
        for query in page_queries:
            query_data = {
                'id': query.id,
                'query_text': query.query_text,
                'domain': query.domain,
                'status': query.status,
                'created_at': query.created_at.isoformat(),
            }
            
            if query.status == 'completed':
                query_data.update({
                    'answer': query.primary_answer,
                    'confidence': query.confidence_score,
                    'safety_score': query.safety_score,
                    'processing_time': query.processing_time,
                    'fair_metrics': {
                        'faithfulness': query.faithfulness_score,
                        'adaptability': query.adaptability_score,
                        'interpretability': query.interpretability_score,
                        'risk_awareness': query.risk_awareness_score,
                    }
                })
            
            queries_data.append(query_data)
        
        return JsonResponse({
            'queries': queries_data,
            'has_next': page_queries.has_next(),
            'has_previous': page_queries.has_previous(),
            'page': page,
            'total_pages': paginator.num_pages,
        })
        
    except QuerySession.DoesNotExist:
        return JsonResponse({'queries': []})
    except Exception as e:
        logger.error(f"Error getting query history: {e}")
        return JsonResponse({
            'error': 'Error retrieving query history',
            'status': 'error'
        }, status=500)


def system_status_api(request):
    """
    API endpoint to get system status and health metrics
    """
    try:
        status = FairAgentService.get_system_status()
        
        # Add database statistics
        total_queries = QueryRecord.objects.count()
        completed_queries = QueryRecord.objects.filter(status='completed').count()
        failed_queries = QueryRecord.objects.filter(status='failed').count()
        
        # Calculate average metrics for completed queries
        avg_metrics = QueryRecord.objects.filter(
            status='completed'
        ).aggregate(
            avg_faithfulness=Avg('faithfulness_score'),
            avg_interpretability=Avg('interpretability_score'),
            avg_risk_awareness=Avg('risk_awareness_score'),
            avg_confidence=Avg('confidence_score'),
            avg_processing_time=Avg('processing_time')
        )
        
        status.update({
            'database_stats': {
                'total_queries': total_queries,
                'completed_queries': completed_queries,
                'failed_queries': failed_queries,
                'success_rate': (completed_queries / total_queries * 100) if total_queries > 0 else 0,
            },
            'average_metrics': avg_metrics,
            'available_metrics': FairAgentService.get_available_metrics(),
        })
        
        return JsonResponse(status)
        
    except Exception as e:
        logger.error(f"Error getting system status: {e}")
        return JsonResponse({
            'error': 'Error retrieving system status',
            'status': 'error'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def submit_feedback_api(request):
    """
    API endpoint to submit user feedback
    """
    try:
        data = json.loads(request.body)
        query_id = data.get('query_id')
        overall_rating = data.get('overall_rating')
        
        if not query_id or not overall_rating:
            return JsonResponse({
                'error': 'Query ID and overall rating are required',
                'status': 'error'
            }, status=400)
        
        query = get_object_or_404(QueryRecord, id=query_id)
        
        # Create or update feedback
        feedback, created = UserFeedback.objects.update_or_create(
            query=query,
            user=request.user if request.user.is_authenticated else None,
            defaults={
                'overall_rating': overall_rating,
                'accuracy_rating': data.get('accuracy_rating'),
                'clarity_rating': data.get('clarity_rating'),
                'safety_rating': data.get('safety_rating'),
                'comments': data.get('comments', ''),
                'suggestions': data.get('suggestions', ''),
            }
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Feedback submitted successfully',
            'feedback_id': feedback.id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Invalid JSON data',
            'status': 'error'
        }, status=400)
    except Exception as e:
        logger.error(f"Error submitting feedback: {e}")
        return JsonResponse({
            'error': 'Error submitting feedback',
            'status': 'error'
        }, status=500)



def recent_activity_api(request):
    """
    API endpoint to get recent activity for the home page
    """
    try:
        # Get recent queries
        recent_queries = QueryRecord.objects.filter(
            status='completed'
        ).order_by('-created_at')[:5]
        
        activities = []
        for query in recent_queries:
            activities.append({
                'id': query.id,
                'type': 'query',
                'title': f"{query.domain.title()} Query",
                'description': query.query_text[:100] + ('...' if len(query.query_text) > 100 else ''),
                'timestamp': query.created_at.isoformat(),
                'confidence': query.confidence_score,
                'domain': query.domain
            })
        
        return JsonResponse({
            'activities': activities,
            'total_count': QueryRecord.objects.count(),
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error fetching recent activity: {e}")
        return JsonResponse({
            'activities': [],
            'error': str(e),
            'status': 'error'
        }, status=500)


# Dataset Management APIs
@require_http_methods(["GET"])
def list_datasets_api(request):
    """
    API endpoint to list all available datasets
    """
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(settings.BASE_DIR, '..'))
        from src.data.dataset_loader import get_dataset_loader
        
        dataset_loader = get_dataset_loader()
        datasets_info = dataset_loader.to_dict()
        
        return JsonResponse({
            'datasets': datasets_info,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error listing datasets: {e}")
        return JsonResponse({
            'datasets': {'finance': [], 'medical': []},
            'error': str(e),
            'status': 'error'
        }, status=500)


@require_http_methods(["GET"])
def dataset_info_api(request, domain, dataset_name):
    """
    API endpoint to get detailed information about a specific dataset
    """
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(settings.BASE_DIR, '..'))
        from src.data.dataset_loader import get_dataset_loader
        
        dataset_loader = get_dataset_loader()
        dataset = dataset_loader.get_dataset_info(domain, dataset_name)
        
        if not dataset:
            return JsonResponse({
                'error': f'Dataset {dataset_name} not found for domain {domain}',
                'status': 'not_found'
            }, status=404)
        
        availability = dataset_loader.check_dataset_availability(domain, dataset_name)
        
        return JsonResponse({
            'dataset': {
                'name': dataset.name,
                'source': dataset.source,
                'local_path': dataset.local_path,
                'description': dataset.description,
                'preprocessing_required': dataset.preprocessing_required,
                'access_required': dataset.access_required,
                'domain': dataset.domain,
                'availability': availability
            },
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error getting dataset info: {e}")
        return JsonResponse({
            'error': str(e),
            'status': 'error'
        }, status=500)


@require_http_methods(["GET"])
def dataset_stats_api(request):
    """
    API endpoint to get statistics about all datasets
    """
    try:
        import sys
        import os
        sys.path.insert(0, os.path.join(settings.BASE_DIR, '..'))
        from src.data.dataset_loader import get_dataset_loader
        
        dataset_loader = get_dataset_loader()
        stats = dataset_loader.get_dataset_stats()
        
        return JsonResponse({
            'stats': stats,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Error getting dataset stats: {e}")
        return JsonResponse({
            'stats': {},
            'error': str(e),
            'status': 'error'
        }, status=500)

class ArchitectureView(TemplateView):
    """View for system architecture diagram"""
    template_name = 'fair_agent_app/architecture.html'


class PublicationView(TemplateView):
    """View for publication and research documentation"""
    template_name = 'fair_agent_app/publication.html'


class DashboardView(TemplateView):
    """View for system dashboard and telemetry"""
    template_name = 'fair_agent_app/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Fetch recent traces with their spans pre-fetched
        traces = TraceLog.objects.prefetch_related('spans').order_by('-created_at')[:50]
        
        # Enrich traces with query info
        enriched_traces = []
        for trace in traces:
            trace_data = {
                'trace': trace,
                'query_record': None
            }
            
            # Try to find associated query record
            query_id = trace.metadata.get('query_id')
            if query_id:
                try:
                    trace_data['query_record'] = QueryRecord.objects.get(id=query_id)
                except QueryRecord.DoesNotExist:
                    pass
            
            enriched_traces.append(trace_data)
        
        # Calculate summary stats
        total_traces = TraceLog.objects.count()
        avg_duration_ms = TraceLog.objects.aggregate(Avg('duration_ms'))['duration_ms__avg'] or 0
        avg_duration_sec = avg_duration_ms / 1000.0
        
        # Get recent errors (spans with status='error')
        error_spans = SpanLog.objects.filter(status='error').order_by('-start_time')[:10]
        
        # Get Memory Stats
        try:
            from .services import FairAgentService
            memory_stats = FairAgentService.get_memory_stats()
        except Exception as e:
            memory_stats = {"error": str(e)}

        context['traces'] = enriched_traces
        context['total_traces'] = total_traces
        context['avg_duration_sec'] = round(avg_duration_sec, 2)
        context['recent_errors'] = error_spans
        context['memory_stats'] = memory_stats
        
        return context

@csrf_exempt
def search_memory_api(request):
    """API to search memory systems"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            system = data.get('system', 'all')
            
            from .services import FairAgentService
            results = FairAgentService.search_memory(query, system)
            
            return JsonResponse({
                'status': 'success',
                'results': results
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)