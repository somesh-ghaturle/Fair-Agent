"""
Django admin configuration for FAIR-Agent models
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import (
    QuerySession, QueryRecord, EvaluationMetrics, 
    SystemPerformance, SafetyAlert, UserFeedback
)


@admin.register(QuerySession)
class QuerySessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'updated_at', 'is_active', 'query_count']
    list_filter = ['is_active', 'created_at', 'updated_at']
    search_fields = ['session_id', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    
    def query_count(self, obj):
        return obj.queries.count()
    query_count.short_description = 'Queries'


class EvaluationMetricsInline(admin.StackedInline):
    model = EvaluationMetrics
    extra = 0
    readonly_fields = ['created_at']


class UserFeedbackInline(admin.TabularInline):
    model = UserFeedback
    extra = 0
    readonly_fields = ['created_at']


class SafetyAlertInline(admin.TabularInline):
    model = SafetyAlert
    extra = 0
    readonly_fields = ['created_at']


@admin.register(QueryRecord)
class QueryRecordAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'query_preview', 'domain', 'status', 'confidence_score', 
        'safety_score', 'processing_time', 'created_at'
    ]
    list_filter = ['domain', 'status', 'created_at', 'processed_at']
    search_fields = ['query_text', 'primary_answer']
    readonly_fields = ['created_at', 'processed_at']
    inlines = [EvaluationMetricsInline, UserFeedbackInline, SafetyAlertInline]
    
    fieldsets = (
        ('Query Information', {
            'fields': ('session', 'query_text', 'domain', 'status')
        }),
        ('Response Data', {
            'fields': ('primary_answer', 'confidence_score', 'safety_score')
        }),
        ('FAIR Metrics', {
            'fields': (
                'faithfulness_score', 'adaptability_score', 
                'interpretability_score', 'risk_awareness_score'
            )
        }),
        ('Timing', {
            'fields': ('created_at', 'processed_at', 'processing_time')
        }),
        ('Additional Data', {
            'fields': ('additional_data',),
            'classes': ['collapse']
        })
    )
    
    def query_preview(self, obj):
        return obj.query_text[:100] + "..." if len(obj.query_text) > 100 else obj.query_text
    query_preview.short_description = 'Query'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('session')


@admin.register(EvaluationMetrics)
class EvaluationMetricsAdmin(admin.ModelAdmin):
    list_display = [
        'query_id', 'query_domain', 'faithfulness_overall', 
        'safety_overall', 'interpretability_overall', 'created_at'
    ]
    list_filter = ['query__domain', 'created_at']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Query Reference', {
            'fields': ('query',)
        }),
        ('Faithfulness Metrics', {
            'fields': (
                'faithfulness_token_overlap', 'faithfulness_semantic_similarity',
                'faithfulness_factual_consistency'
            )
        }),
        ('Calibration Metrics', {
            'fields': ('calibration_ece', 'calibration_mce', 'calibration_brier_score')
        }),
        ('Robustness Metrics', {
            'fields': (
                'robustness_semantic_score', 'robustness_syntactic_score',
                'robustness_adversarial_score'
            )
        }),
        ('Safety Metrics', {
            'fields': (
                'safety_medical_safety', 'safety_financial_safety',
                'safety_content_safety'
            )
        }),
        ('Interpretability Metrics', {
            'fields': (
                'interpretability_reasoning_clarity',
                'interpretability_explanation_completeness',
                'interpretability_evidence_citation'
            )
        })
    )
    
    def query_id(self, obj):
        return obj.query.id
    query_id.short_description = 'Query ID'
    
    def query_domain(self, obj):
        return obj.query.domain
    query_domain.short_description = 'Domain'
    
    def faithfulness_overall(self, obj):
        return obj.query.faithfulness_score
    faithfulness_overall.short_description = 'Faithfulness'
    
    def safety_overall(self, obj):
        return obj.query.risk_awareness_score
    safety_overall.short_description = 'Safety'
    
    def interpretability_overall(self, obj):
        return obj.query.interpretability_score
    interpretability_overall.short_description = 'Interpretability'


@admin.register(SystemPerformance)
class SystemPerformanceAdmin(admin.ModelAdmin):
    list_display = [
        'timestamp', 'total_queries', 'successful_queries', 
        'failed_queries', 'success_rate', 'average_response_time'
    ]
    list_filter = ['timestamp']
    readonly_fields = ['timestamp']
    
    fieldsets = (
        ('Performance Metrics', {
            'fields': (
                'timestamp', 'total_queries', 'successful_queries', 
                'failed_queries', 'average_response_time'
            )
        }),
        ('FAIR Metrics Averages', {
            'fields': (
                'avg_faithfulness_score', 'avg_adaptability_score',
                'avg_interpretability_score', 'avg_risk_awareness_score'
            )
        }),
        ('Domain Distribution', {
            'fields': (
                'finance_queries', 'medical_queries', 
                'cross_domain_queries', 'general_queries'
            )
        })
    )
    
    def success_rate(self, obj):
        if obj.total_queries > 0:
            rate = (obj.successful_queries / obj.total_queries) * 100
            color = 'green' if rate >= 90 else 'orange' if rate >= 70 else 'red'
            return format_html(
                '<span style="color: {};">{:.1f}%</span>',
                color, rate
            )
        return '0%'
    success_rate.short_description = 'Success Rate'


@admin.register(SafetyAlert)
class SafetyAlertAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'query_link', 'alert_type', 'severity', 
        'resolved', 'created_at', 'resolved_at'
    ]
    list_filter = ['alert_type', 'severity', 'resolved', 'created_at']
    search_fields = ['message', 'query__query_text']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Alert Information', {
            'fields': ('query', 'alert_type', 'severity', 'message')
        }),
        ('Details', {
            'fields': ('details',),
            'classes': ['collapse']
        }),
        ('Resolution', {
            'fields': ('resolved', 'resolved_at')
        }),
        ('Timing', {
            'fields': ('created_at',)
        })
    )
    
    def query_link(self, obj):
        url = reverse('admin:fair_agent_app_queryrecord_change', args=[obj.query.id])
        return format_html('<a href="{}">{}</a>', url, obj.query.id)
    query_link.short_description = 'Query'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('query')
    
    actions = ['mark_resolved', 'mark_unresolved']
    
    def mark_resolved(self, request, queryset):
        from django.utils import timezone
        queryset.update(resolved=True, resolved_at=timezone.now())
        self.message_user(request, f'{queryset.count()} alerts marked as resolved.')
    mark_resolved.short_description = 'Mark selected alerts as resolved'
    
    def mark_unresolved(self, request, queryset):
        queryset.update(resolved=False, resolved_at=None)
        self.message_user(request, f'{queryset.count()} alerts marked as unresolved.')
    mark_unresolved.short_description = 'Mark selected alerts as unresolved'


@admin.register(UserFeedback)
class UserFeedbackAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'query_link', 'user', 'overall_rating', 
        'accuracy_rating', 'clarity_rating', 'safety_rating', 'created_at'
    ]
    list_filter = [
        'overall_rating', 'accuracy_rating', 'clarity_rating', 
        'safety_rating', 'created_at'
    ]
    search_fields = ['comments', 'suggestions', 'query__query_text', 'user__username']
    readonly_fields = ['created_at']
    
    fieldsets = (
        ('Feedback Information', {
            'fields': ('query', 'user')
        }),
        ('Ratings', {
            'fields': (
                'overall_rating', 'accuracy_rating', 
                'clarity_rating', 'safety_rating'
            )
        }),
        ('Comments', {
            'fields': ('comments', 'suggestions')
        }),
        ('Timing', {
            'fields': ('created_at',)
        })
    )
    
    def query_link(self, obj):
        url = reverse('admin:fair_agent_app_queryrecord_change', args=[obj.query.id])
        return format_html('<a href="{}">{}</a>', url, obj.query.id)
    query_link.short_description = 'Query'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('query', 'user')


# Custom admin site configuration
admin.site.site_header = "FAIR-Agent Administration"
admin.site.site_title = "FAIR-Agent Admin"
admin.site.index_title = "Welcome to FAIR-Agent Administration Portal"