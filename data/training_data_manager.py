"""
Training Data Manager for FAIR-Agent

This module manages training datasets for domain-specific fine-tuning,
including data collection, preprocessing, and quality assessment.
"""

import json
import pandas as pd
from typing import List, Dict, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class TrainingDataManager:
    """Manages training data for domain-specific fine-tuning"""
    
    def __init__(self, data_dir: str = "./data/training"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
    def create_medical_dataset(self) -> List[Dict[str, str]]:
        """Create comprehensive medical training dataset"""
        
        medical_qa_pairs = [
            # Medication Safety
            {
                "question": "What should I know about taking blood thinners?",
                "answer": "Blood thinners require careful monitoring and precautions. Key points include: regular blood tests to monitor levels, avoiding activities with high injury risk, being aware of drug interactions, watching for bleeding signs, and following dosing schedules precisely. Always inform healthcare providers about blood thinner use before procedures or when starting new medications. Never stop or change doses without medical supervision.",
                "category": "medication_safety",
                "safety_level": "high"
            },
            {
                "question": "How should insulin be stored and administered?",
                "answer": "Insulin storage and administration are critical for diabetes management. Store unopened insulin in refrigerator (36-46°F), keep current vial at room temperature for up to 28 days, rotate injection sites to prevent lipodystrophy, check expiration dates regularly, and never freeze insulin. Always use proper injection technique, dispose of needles safely, and monitor blood glucose as directed. Consult healthcare providers for dosing adjustments.",
                "category": "medication_safety",
                "safety_level": "high"
            },
            
            # Symptom Recognition
            {
                "question": "What are the warning signs of stroke?",
                "answer": "Stroke warning signs require immediate medical attention. Remember FAST: Face drooping (smile appears uneven), Arms weakness (one arm drifts down when raised), Speech difficulty (slurred or strange words), Time to call emergency services. Additional signs include sudden severe headache, vision loss, dizziness, or confusion. Every minute matters in stroke treatment - call 911 immediately if any symptoms occur.",
                "category": "emergency_symptoms",
                "safety_level": "critical"
            },
            
            # Preventive Care
            {
                "question": "How important are regular health screenings?",
                "answer": "Regular health screenings are essential for early disease detection and prevention. Recommended screenings vary by age and risk factors but commonly include blood pressure checks, cholesterol testing, cancer screenings (mammograms, colonoscopies, Pap smears), diabetes screening, and bone density tests. Early detection significantly improves treatment outcomes and can prevent serious complications. Discuss appropriate screening schedules with your healthcare provider.",
                "category": "preventive_care",
                "safety_level": "medium"
            },
            
            # Mental Health
            {
                "question": "How can I recognize signs of depression?",
                "answer": "Depression signs include persistent sadness, loss of interest in activities, changes in appetite or sleep patterns, fatigue, difficulty concentrating, feelings of worthlessness, and thoughts of self-harm. If experiencing several symptoms for more than two weeks, seek professional help. Depression is a treatable medical condition. Crisis resources are available 24/7 - contact the National Suicide Prevention Lifeline at 988 if having thoughts of self-harm.",
                "category": "mental_health",
                "safety_level": "high"
            }
        ]
        
        # Add safety disclaimers
        enhanced_dataset = []
        for item in medical_qa_pairs:
            enhanced_item = item.copy()
            enhanced_item["answer"] += " MEDICAL DISCLAIMER: This information is for educational purposes only and does not constitute medical advice. Always consult with qualified healthcare professionals for medical concerns, diagnosis, and treatment decisions."
            enhanced_dataset.append(enhanced_item)
        
        return enhanced_dataset
    
    def create_finance_dataset(self) -> List[Dict[str, str]]:
        """Create comprehensive financial training dataset"""
        
        finance_qa_pairs = [
            # Investment Fundamentals
            {
                "question": "What are the key principles of successful investing?",
                "answer": "Successful investing follows several key principles: diversification across asset classes and sectors, maintaining a long-term perspective, understanding risk tolerance, regular portfolio rebalancing, minimizing fees and taxes, avoiding emotional decision-making, and continuous education. Dollar-cost averaging can help reduce timing risk. Most importantly, invest only what you can afford to lose and maintain an emergency fund separate from investments.",
                "category": "investment_fundamentals",
                "risk_level": "medium"
            },
            
            # Risk Management
            {
                "question": "How should I assess investment risk?",
                "answer": "Investment risk assessment involves evaluating multiple factors: volatility (price fluctuations), liquidity risk (ability to sell quickly), credit risk (default possibility), inflation risk, and concentration risk. Consider your time horizon, financial goals, and risk tolerance. Diversification helps manage risk but doesn't eliminate it. High-risk investments may offer higher returns but can result in significant losses. Never invest more than you can afford to lose.",
                "category": "risk_management",
                "risk_level": "high"
            },
            
            # Retirement Planning
            {
                "question": "When should I start planning for retirement?",
                "answer": "Retirement planning should begin as early as possible to maximize compound growth. Start by contributing to employer-sponsored 401(k) plans, especially if there's matching. Maximize contributions to tax-advantaged accounts like IRAs. Consider target-date funds for automatic diversification and rebalancing. Calculate retirement needs based on desired lifestyle and expected expenses. Review and adjust plans regularly as circumstances change.",
                "category": "retirement_planning",
                "risk_level": "low"
            },
            
            # Market Volatility
            {
                "question": "How should I handle market downturns?",
                "answer": "Market downturns are normal parts of investing cycles. Key strategies include: staying calm and avoiding panic selling, maintaining long-term perspective, continuing regular contributions (dollar-cost averaging), rebalancing portfolios when appropriate, and focusing on quality investments. Market timing is extremely difficult and often counterproductive. Consider downturns as potential buying opportunities for long-term investors with adequate emergency funds.",
                "category": "market_volatility",
                "risk_level": "medium"
            },
            
            # Debt Management
            {
                "question": "What's the best strategy for paying off debt?",
                "answer": "Effective debt management strategies include: listing all debts with balances and interest rates, prioritizing high-interest debt (avalanche method) or smallest balances (snowball method), making more than minimum payments when possible, avoiding new debt, and considering debt consolidation if beneficial. Build emergency fund while paying debt to avoid borrowing for unexpected expenses. Seek credit counseling if overwhelmed.",
                "category": "debt_management",
                "risk_level": "low"
            }
        ]
        
        # Add financial disclaimers
        enhanced_dataset = []
        for item in finance_qa_pairs:
            enhanced_item = item.copy()
            enhanced_item["answer"] += " FINANCIAL DISCLAIMER: This information is for educational purposes only and does not constitute financial advice. Past performance does not guarantee future results. Investment values may fluctuate and you may lose money. Consider consulting with qualified financial advisors before making investment decisions."
            enhanced_dataset.append(enhanced_item)
        
        return enhanced_dataset
    
    def save_datasets(self):
        """Save training datasets to files"""
        medical_data = self.create_medical_dataset()
        finance_data = self.create_finance_dataset()
        
        # Save as JSON
        with open(self.data_dir / "medical_training.json", "w") as f:
            json.dump(medical_data, f, indent=2)
        
        with open(self.data_dir / "finance_training.json", "w") as f:
            json.dump(finance_data, f, indent=2)
        
        # Save as CSV for easy review
        pd.DataFrame(medical_data).to_csv(self.data_dir / "medical_training.csv", index=False)
        pd.DataFrame(finance_data).to_csv(self.data_dir / "finance_training.csv", index=False)
        
        logger.info(f"Saved {len(medical_data)} medical and {len(finance_data)} finance training examples")
        
        return len(medical_data), len(finance_data)

if __name__ == "__main__":
    manager = TrainingDataManager()
    medical_count, finance_count = manager.save_datasets()
    print(f"Created training datasets: {medical_count} medical, {finance_count} finance examples")