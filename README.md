# FAIR-Agent System 🤖

> **F**aithful, **A**daptive, **I**nterpretable, and **R**isk-Aware Multi-Agent AI System

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)
[![Ollama](https://img.shields.io/badge/Ollama-Supported-orange.svg)](https://ollama.ai/)

**CS668 Analytics Capstone - Fall 2025**  
**Author:** Somesh Ghaturle

---

## 📋 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Model Selection](#model-selection)
- [FAIR Metrics](#fair-metrics)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)

---

## 🎯 Overview

**FAIR-Agent** is an advanced multi-agent AI system designed to provide trustworthy, evidence-based responses for **Finance** and **Medical** domains. The system combines specialized domain agents with comprehensive evaluation metrics to ensure safety, accuracy, and interpretability.

### What Makes FAIR-Agent Special?

- 🤖 **Multi-Agent Architecture** - Specialized agents for Finance and Medical domains
- 🧠 **Intelligent Orchestration** - Automatic domain classification and query routing
- 📚 **Evidence-Grounded** - 16 curated sources + real-time internet RAG enhancement
- 🛡️ **Safety-First Design** - Comprehensive disclaimers and risk awareness
- 📊 **Real-Time FAIR Metrics** - Transparent evaluation of response quality
- 🔒 **Privacy-Focused** - Local LLM inference via Ollama (no data sent to cloud)
- 🎨 **Modern Web Interface** - Responsive Django UI with live metrics visualization
- � **Flexible Model Support** - Multiple LLMs (Llama3.2, Mistral, Phi3) with dynamic switching

---

## ✨ Key Features

### 1. Multi-Domain Expertise
- **Finance Agent**: Investment queries, portfolio strategies, market analysis
- **Medical Agent**: Health information, medical concepts, treatment options
- **Cross-Domain Support**: Handles queries spanning both domains

### 2. Intelligent Query Processing
- Automatic domain classification
- Confidence scoring for all responses
- Context-aware dialogue

### 3. Evidence-Based Responses
- Curated knowledge base with 16 high-quality sources
- Semantic search for relevant evidence
- Source attribution and citation
- Real-time internet RAG enhancement

### 4. Safety & Compliance
- Medical disclaimers for health queries
- Financial disclaimers for investment advice
- Harmful content detection
- Professional consultation emphasis

### 5. Comprehensive FAIR Metrics
- **Faithfulness (35-75%)**: Accuracy and evidence alignment
- **Interpretability (40-72%)**: Response clarity and structure
- **Risk Awareness (60-100%)**: Safety disclaimers and warnings
- Real-time scoring and visualization

### 6. Model Flexibility
- Multiple LLM support: Ollama (llama3.2, mistral, phi3)
- Dynamic model switching
- Local inference for privacy
- Automatic fallback mechanisms

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────┐
│           Web Interface (Django)                │
│   Query Input │ Model Select │ FAIR Metrics    │
└─────────────────────┬───────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────┐
│              Orchestrator                       │
│   Domain Classification → Route to Agent       │
└─────────────────────┬───────────────────────────┘
                      │
      ┌───────────────┼───────────────┐
      ▼               ▼               ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ Finance  │  │ Medical  │  │ Evidence │
│  Agent   │  │  Agent   │  │  System  │
└──────────┘  └──────────┘  └──────────┘
      │               │               │
      └───────────────┼───────────────┘
                      ▼
┌─────────────────────────────────────────────────┐
│         Enhancement Systems                     │
│  Safety │ Reasoning │ Internet RAG              │
└─────────────────────┬───────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────┐
│            FAIR Evaluation                      │
│  Faithfulness │ Interpretability │ Risk         │
└─────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- Python 3.11+
- [Ollama](https://ollama.ai/)
- 8GB+ RAM
- macOS, Linux, or Windows with WSL

### Step 1: Install Ollama

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama
ollama serve

# Pull models
ollama pull llama3.2
ollama pull mistral
```

### Step 2: Clone Repository

```bash
git clone https://github.com/somesh-ghaturle/Fair-Agent.git
cd Fair-Agent
```

### Step 3: Setup Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Database Setup

```bash
cd webapp
python manage.py migrate
```

---

## 🎬 Quick Start

### Start the Server

```bash
cd webapp
python manage.py runserver
```

Access at: **http://127.0.0.1:8000/**

### Example Queries

**Finance:**
```
What are the best investment strategies for retirement?
How does diversification reduce portfolio risk?
```

**Medical:**
```
What medications help with diabetes?
Explain how vaccines work.
```

---

## 🔄 Model Selection

### Available Models

**Ollama Models (Recommended):**
- **llama3.2** (Default): Best overall performance
- **mistral**: Fast inference, good reasoning
- **phi3**: Lightweight, efficient

**Via Web UI:**
Click the "Model" dropdown and select your desired model.

**Via API:**
```bash
curl -X POST http://127.0.0.1:8000/api/query/process/ \
  -H "Content-Type: application/json" \
  -d '{"query": "What is diversification?", "model_name": "llama3.2"}'
```

---

## 📊 FAIR Metrics

### Metric Definitions

**1. Faithfulness (35-75%)**
- Measures evidence alignment
- Base Score: 35-50%
- Evidence Boost: +25-35%

**2. Interpretability (40-72%)**
- Evaluates response clarity
- Base Score: 40-50%
- Reasoning Boost: +32%

**3. Risk Awareness (60-100%)**
- Assesses safety disclaimers
- Base Score: 60-65%
- Safety Boost: +40%

### Enhancement Pipeline

```
Base Response → Safety (+40%) → Evidence (+0-35%) → 
                Reasoning (+32%) → Internet RAG (+5%) → Final Score
```

---

## 📁 Project Structure

```
Fair-Agent/
├── config/               # Configuration files
├── data/                 # Datasets and evidence
├── src/
│   ├── agents/          # Finance & Medical agents
│   ├── evaluation/      # FAIR metrics
│   ├── evidence/        # RAG system
│   ├── reasoning/       # Chain-of-thought
│   └── safety/          # Disclaimer system
├── webapp/
│   ├── fair_agent_app/  # Django application
│   ├── static/          # CSS, JavaScript
│   └── templates/       # HTML templates
├── scripts/             # Utility scripts
└── requirements.txt     # Dependencies
```

---

## ⚙️ Configuration

### Main Config (`config/config.yaml`)

```yaml
model:
  default: "llama3.2"
  backend: "ollama"

agents:
  finance:
    confidence_threshold: 0.7
  medical:
    confidence_threshold: 0.8

evidence:
  similarity_threshold: 0.3
  max_results: 3
```

---

## 📚 API Documentation

### Process Query

```bash
POST /api/query/process/
```

**Request:**
```json
{
  "query": "What is portfolio diversification?",
  "model_name": "llama3.2"
}
```

**Response:**
```json
{
  "answer": "Portfolio diversification is...",
  "domain": "finance",
  "confidence_score": 0.87,
  "fair_metrics": {
    "faithfulness": {"score": 0.75, "boost": 0.25},
    "interpretability": {"score": 0.72, "boost": 0.32},
    "risk_awareness": {"score": 1.00, "boost": 0.40}
  }
}
```

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📞 Contact

**Somesh Ghaturle**  
Email: someshghaturle@gmail.com  
GitHub: [@somesh-ghaturle](https://github.com/somesh-ghaturle)

**Project:** [https://github.com/somesh-ghaturle/Fair-Agent](https://github.com/somesh-ghaturle/Fair-Agent)

---

## 🔮 Future Enhancements

- [ ] Additional domain agents (Legal, Education)
- [ ] User authentication and personalization
- [ ] Conversation memory and context tracking
- [ ] Multimodal inputs (images, PDFs)
- [ ] Mobile app development
- [ ] Cloud deployment options

---

**Built with ❤️ for CS668 Analytics Capstone - Fall 2025**
