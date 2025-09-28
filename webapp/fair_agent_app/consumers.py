"""
WebSocket consumers for real-time FAIR-Agent interactions
"""

import json
import asyncio
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import QuerySession, QueryRecord
from .services import QueryProcessor

logger = logging.getLogger(__name__)


class QueryConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time query processing"""
    
    async def connect(self):
        self.session_id = self.scope['url_route']['kwargs']['session_id']
        self.group_name = f'query_{self.session_id}'
        
        # Join session group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Send connection confirmation
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'session_id': self.session_id
        }))
    
    async def disconnect(self, close_code):
        # Leave session group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_type = data.get('type')
            
            if message_type == 'process_query':
                await self.handle_process_query(data)
            elif message_type == 'get_status':
                await self.handle_get_status(data)
            else:
                await self.send(text_data=json.dumps({
                    'type': 'error',
                    'message': f'Unknown message type: {message_type}'
                }))
                
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON format'
            }))
        except Exception as e:
            logger.error(f"Error in QueryConsumer.receive: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Internal server error'
            }))
    
    async def handle_process_query(self, data):
        """Handle query processing request"""
        query_text = data.get('query', '').strip()
        
        if not query_text:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Query text is required'
            }))
            return
        
        try:
            # Send processing started message
            await self.send(text_data=json.dumps({
                'type': 'query_processing_started',
                'query': query_text
            }))
            
            # Get or create session
            session = await self.get_or_create_session()
            
            # Create query record
            query_record = await self.create_query_record(session, query_text)
            
            # Send query created message
            await self.send(text_data=json.dumps({
                'type': 'query_created',
                'query_id': query_record.id,
                'domain': query_record.domain
            }))
            
            # Process query asynchronously
            result = await QueryProcessor.process_query_async(query_text)
            
            if result.get('status') == 'failed':
                await self.update_query_record(query_record.id, status='failed')
                await self.send(text_data=json.dumps({
                    'type': 'query_failed',
                    'query_id': query_record.id,
                    'error': result.get('error', 'Unknown error')
                }))
                return
            
            # Update query record with results
            await self.update_query_record(
                query_record.id,
                status='completed',
                primary_answer=result.get('primary_answer', ''),
                confidence_score=result.get('confidence_score'),
                safety_score=result.get('safety_score'),
                processing_time=result.get('processing_time')
            )
            
            # Evaluate response
            try:
                metrics = await QueryProcessor.evaluate_response_async(
                    query_text,
                    result.get('primary_answer', ''),
                    query_record.domain
                )
                
                # Send evaluation results
                await self.send(text_data=json.dumps({
                    'type': 'evaluation_completed',
                    'query_id': query_record.id,
                    'metrics': metrics
                }))
                
            except Exception as e:
                logger.error(f"Error evaluating response: {e}")
            
            # Send final result
            await self.send(text_data=json.dumps({
                'type': 'query_completed',
                'query_id': query_record.id,
                'answer': result.get('primary_answer', ''),
                'confidence': result.get('confidence_score'),
                'domain': query_record.domain,
                'safety_score': result.get('safety_score'),
                'processing_time': result.get('processing_time')
            }))
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Error processing query'
            }))
    
    async def handle_get_status(self, data):
        """Handle status request"""
        try:
            from .services import FairAgentService
            status = FairAgentService.get_system_status()
            
            await self.send(text_data=json.dumps({
                'type': 'status_update',
                'status': status
            }))
            
        except Exception as e:
            logger.error(f"Error getting status: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Error getting system status'
            }))
    
    @database_sync_to_async
    def get_or_create_session(self):
        """Get or create query session"""
        session, created = QuerySession.objects.get_or_create(
            session_id=self.session_id
        )
        return session
    
    @database_sync_to_async
    def create_query_record(self, session, query_text):
        """Create query record"""
        from .services import FairAgentService
        domain = FairAgentService.classify_query_domain(query_text)
        
        return QueryRecord.objects.create(
            session=session,
            query_text=query_text,
            domain=domain,
            status='processing'
        )
    
    @database_sync_to_async
    def update_query_record(self, query_id, **kwargs):
        """Update query record"""
        QueryRecord.objects.filter(id=query_id).update(**kwargs)


class MetricsConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for real-time metrics updates"""
    
    async def connect(self):
        self.group_name = 'metrics_updates'
        
        # Join metrics group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Start sending periodic updates
        asyncio.create_task(self.send_periodic_updates())
    
    async def disconnect(self, close_code):
        # Leave metrics group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
    
    async def send_periodic_updates(self):
        """Send periodic metrics updates"""
        while True:
            try:
                metrics = await self.get_current_metrics()
                await self.send(text_data=json.dumps({
                    'type': 'metrics_update',
                    'metrics': metrics
                }))
                
                # Wait 10 seconds before next update
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Error sending metrics update: {e}")
                await asyncio.sleep(10)
    
    @database_sync_to_async
    def get_current_metrics(self):
        """Get current system metrics"""
        from django.db.models import Avg, Count
        
        # Get query statistics
        total_queries = QueryRecord.objects.count()
        completed_queries = QueryRecord.objects.filter(status='completed').count()
        failed_queries = QueryRecord.objects.filter(status='failed').count()
        
        # Get average FAIR metrics
        avg_metrics = QueryRecord.objects.filter(
            status='completed'
        ).aggregate(
            avg_faithfulness=Avg('faithfulness_score'),
            avg_interpretability=Avg('interpretability_score'),
            avg_risk_awareness=Avg('risk_awareness_score'),
            avg_confidence=Avg('confidence_score')
        )
        
        # Get domain distribution
        domain_stats = list(QueryRecord.objects.values('domain').annotate(
            count=Count('id')
        ).order_by('-count'))
        
        return {
            'query_stats': {
                'total': total_queries,
                'completed': completed_queries,
                'failed': failed_queries,
                'success_rate': (completed_queries / total_queries * 100) if total_queries > 0 else 0,
            },
            'avg_metrics': avg_metrics,
            'domain_stats': domain_stats,
            'timestamp': str(asyncio.get_event_loop().time())
        }