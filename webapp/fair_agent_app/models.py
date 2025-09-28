"""
Django models for FAIR-Agent Web Application

These models store query history, evaluation metrics, and system performance data.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import json


class QuerySession(models.Model):
    """Model to track user query sessions"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Session {self.session_id} - {self.created_at}"


class QueryRecord(models.Model):
    """Model to store individual queries and responses"""
    
    DOMAIN_CHOICES = [
        ('finance', 'Finance'),
        ('medical', 'Medical'),
        ('cross_domain', 'Cross Domain'),
        ('general', 'General'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    session = models.ForeignKey(QuerySession, on_delete=models.CASCADE, related_name='queries')
    query_text = models.TextField()
    domain = models.CharField(max_length=20, choices=DOMAIN_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Response data
    primary_answer = models.TextField(blank=True)
    confidence_score = models.FloatField(null=True, blank=True)
    safety_score = models.FloatField(null=True, blank=True)
    
    # FAIR metrics
    faithfulness_score = models.FloatField(null=True, blank=True)
    adaptability_score = models.FloatField(null=True, blank=True)
    interpretability_score = models.FloatField(null=True, blank=True)
    risk_awareness_score = models.FloatField(null=True, blank=True)
    
    # Timing and metadata
    created_at = models.DateTimeField(default=timezone.now)
    processed_at = models.DateTimeField(null=True, blank=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    
    # Additional data stored as JSON
    additional_data = models.JSONField(default=dict, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Query: {self.query_text[:50]}... - {self.domain} - {self.status}"
    
    def set_additional_data(self, key, value):
        """Helper method to set additional data"""
        self.additional_data[key] = value
        self.save(update_fields=['additional_data'])
    
    def get_additional_data(self, key, default=None):
        """Helper method to get additional data"""
        return self.additional_data.get(key, default)


class EvaluationMetrics(models.Model):
    """Model to store detailed evaluation metrics for queries"""
    
    query = models.OneToOneField(QueryRecord, on_delete=models.CASCADE, related_name='metrics')
    
    # Faithfulness metrics
    faithfulness_token_overlap = models.FloatField(null=True, blank=True)
    faithfulness_semantic_similarity = models.FloatField(null=True, blank=True)
    faithfulness_factual_consistency = models.FloatField(null=True, blank=True)
    
    # Calibration metrics
    calibration_ece = models.FloatField(null=True, blank=True)
    calibration_mce = models.FloatField(null=True, blank=True)
    calibration_brier_score = models.FloatField(null=True, blank=True)
    
    # Robustness metrics
    robustness_semantic_score = models.FloatField(null=True, blank=True)
    robustness_syntactic_score = models.FloatField(null=True, blank=True)
    robustness_adversarial_score = models.FloatField(null=True, blank=True)
    
    # Safety metrics
    safety_medical_safety = models.FloatField(null=True, blank=True)
    safety_financial_safety = models.FloatField(null=True, blank=True)
    safety_content_safety = models.FloatField(null=True, blank=True)
    
    # Interpretability metrics
    interpretability_reasoning_clarity = models.FloatField(null=True, blank=True)
    interpretability_explanation_completeness = models.FloatField(null=True, blank=True)
    interpretability_evidence_citation = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Metrics for Query {self.query.id}"


class SystemPerformance(models.Model):
    """Model to track overall system performance metrics"""
    
    timestamp = models.DateTimeField(default=timezone.now)
    
    # Performance metrics
    total_queries = models.IntegerField(default=0)
    successful_queries = models.IntegerField(default=0)
    failed_queries = models.IntegerField(default=0)
    average_response_time = models.FloatField(null=True, blank=True)
    
    # FAIR metrics averages
    avg_faithfulness_score = models.FloatField(null=True, blank=True)
    avg_adaptability_score = models.FloatField(null=True, blank=True)
    avg_interpretability_score = models.FloatField(null=True, blank=True)
    avg_risk_awareness_score = models.FloatField(null=True, blank=True)
    
    # Domain-specific performance
    finance_queries = models.IntegerField(default=0)
    medical_queries = models.IntegerField(default=0)
    cross_domain_queries = models.IntegerField(default=0)
    general_queries = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"System Performance - {self.timestamp}"


class SafetyAlert(models.Model):
    """Model to track safety alerts and violations"""
    
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    ALERT_TYPE_CHOICES = [
        ('medical_safety', 'Medical Safety'),
        ('financial_safety', 'Financial Safety'),
        ('content_safety', 'Content Safety'),
        ('system_error', 'System Error'),
    ]
    
    query = models.ForeignKey(QueryRecord, on_delete=models.CASCADE, related_name='safety_alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPE_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES)
    message = models.TextField()
    details = models.JSONField(default=dict, blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.alert_type} - {self.severity} - Query {self.query.id}"


class UserFeedback(models.Model):
    """Model to collect user feedback on responses"""
    
    RATING_CHOICES = [
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Excellent'),
    ]
    
    query = models.ForeignKey(QueryRecord, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    # Ratings
    overall_rating = models.IntegerField(choices=RATING_CHOICES)
    accuracy_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    clarity_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    safety_rating = models.IntegerField(choices=RATING_CHOICES, null=True, blank=True)
    
    # Feedback text
    comments = models.TextField(blank=True)
    suggestions = models.TextField(blank=True)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ['query', 'user']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback for Query {self.query.id} - Rating: {self.overall_rating}"