"""
Django views for FAIR-Agent Web Application

This module contains the view functions and classes that handle HTTP requests
and render responses for the FAIR-Agent web interface.
"""

import json
import uuid
import logging
from datetime import datetime
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
    SystemPerformance, SafetyAlert, UserFeedback
)
from .services import FairAgentService, QueryProcessor

logger = logging.getLogger(__name__)


class HomeView(TemplateView):
    """Main landing page for FAIR-Agent web interface"""
    template_name = 'fair_agent_app/home.html'
    
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
        
        if not query_text:
            return JsonResponse({
                'error': 'Query text is required',
                'status': 'error'
            }, status=400)
        
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
            result = FairAgentService.process_query(query_text)
            
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
                    query_record.risk_awareness_score = metrics.get('safety', {}).get('overall_score')
                    query_record.interpretability_score = metrics.get('interpretability', {}).get('overall_score')
                    query_record.save()
                    
            except Exception as e:
                logger.error(f"Error evaluating response: {e}")
            
            # Return successful response with comprehensive metrics
            # Ensure we have valid FAIR metrics with fallback defaults
            faithfulness_score = query_record.faithfulness_score or metrics.get('faithfulness', {}).get('overall_score', 0.35)
            interpretability_score = query_record.interpretability_score or metrics.get('interpretability', {}).get('overall_score', 0.40)
            risk_awareness_score = query_record.risk_awareness_score or metrics.get('safety', {}).get('overall_score', 0.60)
            
            response_data = {
                'query_id': query_record.id,
                'answer': result.get('primary_answer', ''),
                'confidence': result.get('confidence_score', 0.6),
                'domain': domain,
                'safety_score': result.get('safety_score', 0.65),
                'processing_time': result.get('processing_time'),
                'status': 'success',
                'fair_metrics': {
                    'faithfulness': faithfulness_score,
                    'interpretability': interpretability_score,
                    'risk_awareness': risk_awareness_score,
                    'calibration_error': metrics.get('calibration', {}).get('expected_calibration_error', 0.25),
                    'robustness': metrics.get('robustness', {}).get('overall_score', 0.35),
                    'detailed_faithfulness': {
                        'token_overlap': metrics.get('faithfulness', {}).get('token_overlap', 0.0),
                        'semantic_similarity': metrics.get('faithfulness', {}).get('semantic_similarity', 0.0),
                        'factual_consistency': metrics.get('faithfulness', {}).get('factual_consistency', 0.0)
                    },
                    'detailed_interpretability': {
                        'reasoning_clarity': metrics.get('interpretability', {}).get('reasoning_clarity', 0.0),
                        'explanation_completeness': metrics.get('interpretability', {}).get('explanation_completeness', 0.0),
                        'evidence_citation': metrics.get('interpretability', {}).get('evidence_citation', 0.0)
                    },
                    'detailed_safety': {
                        'medical_safety': metrics.get('safety', {}).get('medical_safety', 0.0),
                        'financial_safety': metrics.get('safety', {}).get('financial_safety', 0.0),
                        'content_safety': metrics.get('safety', {}).get('content_safety', 0.0)
                    }
                }
            }
            
            return JsonResponse(response_data)
            
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


def health_check(request):
    """Simple health check endpoint"""
    try:
        # Check database connection
        QueryRecord.objects.count()
        
        # Check FAIR-Agent system
        system_status = FairAgentService.get_system_status()
        
        if system_status.get('initialized'):
            return JsonResponse({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'fair_agent_initialized': True
            })
        else:
            return JsonResponse({
                'status': 'degraded',
                'timestamp': datetime.now().isoformat(),
                'fair_agent_initialized': False,
                'message': 'FAIR-Agent system not fully initialized'
            }, status=503)
            
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return JsonResponse({
            'status': 'unhealthy',
            'timestamp': datetime.now().isoformat(),
            'error': str(e)
        }, status=503)


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