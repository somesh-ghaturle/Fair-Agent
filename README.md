# FAIR-Agent System 🤖# FAIR-Agent System# FAIR-Agent System 🤖# FAIR-Agent System



> **F**aithful, **A**daptive, **I**nterpretable, and **R**isk-Aware Multi-Agent AI System



[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)> **F**aithful, **A**daptive, **I**nterpretable, and **R**isk-Aware Multi-Agent AI System for Finance and Medical Domains

[![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)

[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)

[![Ollama](https://img.shields.io/badge/Ollama-Supported-orange.svg)](https://ollama.ai/)

A sophisticated multi-agent system featuring specialized Finance and Medical AI agents with comprehensive FAIR metrics evaluation, powered by Django web framework and Ollama for local LLM inference.[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)**CS668 Analytics Capstone - Fall 2025**  

**CS668 Analytics Capstone - Fall 2025**  

**Author:** Somesh Ghaturle



---**CS668 Analytics Capstone - Fall 2025**  [![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)](https://www.djangoproject.com/)**Author:** Somesh Ghaturle



## 📋 Table of Contents**Author:** Somesh Ghaturle



- [Overview](#-overview)[![PyTorch](https://img.shields.io/badge/PyTorch-2.0+-red.svg)](https://pytorch.org/)

- [Key Features](#-key-features)

- [System Architecture](#-system-architecture)---

- [Installation](#-installation)

- [Quick Start](#-quick-start)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)A comprehensive AI system featuring specialized Finance and Medical agents with domain classification, cross-domain reasoning, and FAIR (Faithfulness, Adaptability, Interpretability, Risk-awareness) metrics evaluation.

- [Usage](#-usage)

- [FAIR Metrics](#-fair-metrics)## 📋 Table of Contents

- [Project Structure](#-project-structure)

- [Configuration](#-configuration)

- [Model Support](#-model-support)

- [API Documentation](#-api-documentation)- [Overview](#overview)

- [Development](#-development)

- [Key Features](#key-features)**FAIR-Agent** is an advanced multi-agent AI system designed to provide trustworthy, evidence-based responses for Finance and Medical domains. Built with safety-first principles, comprehensive evaluation metrics, and real-time enhancement systems.## 🎯 Project Overview

---

- [System Architecture](#system-architecture)

## 🎯 Overview

- [Installation](#installation)

**FAIR-Agent** is an advanced multi-agent AI system designed to provide trustworthy, evidence-based responses for **Finance** and **Medical** domains. The system combines specialized domain agents with comprehensive evaluation metrics to ensure safety, accuracy, and interpretability.

- [Quick Start](#quick-start)

### What Makes FAIR-Agent Special?

- [Model Selection](#model-selection)---The FAIR-Agent system is designed to provide trustworthy, domain-specific AI assistance in finance and healthcare domains. It features:

- **🏦 Finance Agent** - Investment analysis, portfolio strategies, market insights, financial planning

- **🏥 Medical Agent** - Health information, medical concepts, treatment options, safety-vetted responses- [Project Structure](#project-structure)

- **🎭 Orchestrator** - Intelligent query routing, domain classification, cross-domain reasoning

- **📚 Evidence System** - Curated knowledge base with 16 high-reliability sources (85-98% reliability)- [Usage](#usage)

- **🌐 Internet RAG** - Real-time enhancement from trusted sources (Mayo Clinic, Investopedia, CDC, SEC)

- **🛡️ Safety First** - Multi-layer disclaimers, harmful content detection, professional consultation emphasis- [FAIR Metrics](#fair-metrics)

- **📊 FAIR Metrics** - Real-time evaluation of Faithfulness, Interpretability, Risk Awareness, Calibration, Robustness, Safety

- **🚀 Modern UI** - Responsive Django web interface with real-time metrics visualization- [Configuration](#configuration)## 🎯 Overview- **Multi-Agent Architecture**: Specialized Finance and Medical agents

- **🔒 Privacy-First** - Local LLM inference via Ollama (no data sent to cloud APIs)

- [Development](#development)

---

- **Intelligent Routing**: Automated domain classification for query routing

## ✨ Key Features

---

### 1. Multi-Agent Architecture

- **Specialized Agents**: Dedicated Finance and Medical agents with domain-specific reasoningFAIR-Agent implements a sophisticated **Orchestrator-Agent Architecture** that intelligently routes queries to specialized domain agents, enhances responses with real-time data, and evaluates outputs using comprehensive FAIR (Faithful, Accountable, Interpretable, Robust) metrics.- **Cross-Domain Reasoning**: Ability to handle queries spanning multiple domains

- **Intelligent Routing**: Automatic domain classification using keyword-based and semantic analysis

- **Cross-Domain Support**: Handles queries spanning multiple domains (e.g., "health insurance costs")## 🎯 Overview



### 2. Evidence-Based Responses- **FAIR Metrics**: Comprehensive evaluation of faithfulness, interpretability, and risk-awareness

- **Curated Evidence Database**: 16 sources (8 medical, 8 finance) with 85-98% reliability scores

- **Source Citations**: Responses include [Source X] citations for transparencyFAIR-Agent is an advanced multi-agent AI system designed to provide domain-specific expertise in Finance and Medical fields. The system automatically classifies queries, routes them to specialized agents, and evaluates responses using FAIR metrics to ensure reliability, interpretability, and safety.

- **Real-Time Enhancement**: Internet RAG for up-to-date information from trusted sources

### Key Features- **Web Interface**: User-friendly Django-based web application

### 3. FAIR Metrics Evaluation

- **Faithfulness** (29.7% → 50-60%): Accuracy and factual correctness via evidence grounding### What Makes FAIR-Agent Special?

- **Interpretability** (48.3% → 65-72%): Step-by-step reasoning and structured responses

- **Risk Awareness** (56.2% → 72-78%): Comprehensive disclaimers and risk assessments- **CLI Mode**: Interactive command-line interface for testing

- **Calibration**: Confidence score accuracy

- **Robustness**: Response consistency across variations- **Domain Specialization**: Dedicated agents for Finance and Medical domains with domain-specific reasoning

- **Safety**: Harmful content detection and filtering

- **Intelligent Orchestration**: Automatic query classification and cross-domain reasoning capabilities- 🏦 **Specialized Finance Agent** - Investment strategies, market analysis, financial planning

### 4. Model Flexibility

- **40+ Ollama Models**: Llama 3.2, Llama 3, CodeLlama, Mistral, Gemma- **FAIR Metrics**: Real-time evaluation of Faithfulness, Interpretability, Risk Awareness, and Calibration

- **HuggingFace Support**: GPT-2 and compatible models

- **Specialized Models**: MedLlama2, FinLlama (when available)- **Model Flexibility**: Support for 40+ Ollama models including Llama 3, Mistral, Gemma, and specialized medical/finance models- 🏥 **Specialized Medical Agent** - Health information, medical concepts, safety-vetted responses## 🏗 System Architecture

- **Dynamic Switching**: Change models per query without restart

- **Web Interface**: Clean, responsive Django-based UI with real-time processing and metrics visualization

### 5. Safety Systems

- **Medical Disclaimers**: "NOT A SUBSTITUTE FOR PROFESSIONAL MEDICAL ADVICE" with 911 emergency info- **Local Inference**: Privacy-first approach using Ollama for local model execution- 🎭 **Intelligent Orchestrator** - Domain classification, query routing, cross-domain reasoning

- **Finance Disclaimers**: Investment risk warnings and professional consultation guidance

- **Harmful Content Detection**: Filters dangerous queries (self-harm, illegal activities)

- **Professional Emphasis**: Consistent reminder to consult qualified professionals

---- 🌐 **Internet RAG System** - Real-time data from trusted sources (Investopedia, Mayo Clinic, SEC, CDC)```

---



## 🏗 System Architecture

## ✨ Key Features- 📚 **Evidence Database** - Curated knowledge base with reliability scoringFAIR-Agent System

```

FAIR-Agent System

│

├── 🌐 Django Web Application (Port 8000)### 🤖 Multi-Agent System- 🛡️ **Safety Systems** - Multi-layer content filtering, disclaimers, harmful content detection├── Core System

│   ├── Query Interface (UI)

│   ├── API Endpoints (/api/query/, /api/models/)- **Finance Agent**: Specialized in financial analysis, market insights, and economic reasoning

│   └── Real-time Metrics Display

│- **Medical Agent**: Expert in medical knowledge, diagnosis support, and healthcare information- 📊 **FAIR Metrics** - Comprehensive evaluation (faithfulness, calibration, interpretability, robustness, safety)│   ├── Orchestrator (Query routing & coordination)

├── 🎭 Orchestrator

│   ├── Domain Classification (Finance/Medical/General)- **Orchestrator**: Intelligent query routing and cross-domain reasoning coordination

│   ├── Query Routing

│   └── Cross-Domain Coordination- 🚀 **Django Web Interface** - Modern, responsive UI with real-time interaction│   ├── Finance Agent (GPT-2 based)

│

├── 🏦 Finance Agent### 📊 FAIR Metrics Evaluation

│   ├── Model: Ollama (llama3.2:latest) or HuggingFace (gpt2)

│   ├── Evidence Retrieval (8 finance sources)- **Faithfulness (29.7%)**: Measures accuracy and factual correctness│   └── Medical Agent (GPT-2 based)

│   ├── Chain-of-Thought Reasoning

│   ├── Internet RAG (Investopedia, SEC)- **Interpretability (48.3%)**: Evaluates clarity and explainability

│   └── Financial Disclaimer System

│- **Risk Awareness (56.2%)**: Assesses safety and risk communication---├── Web Interface (Django)

├── 🏥 Medical Agent

│   ├── Model: Ollama (llama3.2:latest) or HuggingFace (gpt2)- **Calibration**: Confidence alignment with actual accuracy

│   ├── Evidence Retrieval (8 medical sources)

│   ├── Chain-of-Thought Reasoning├── FAIR Evaluation Metrics

│   ├── Internet RAG (Mayo Clinic, CDC)

│   ├── Safety Screening### 🚀 Performance

│   └── Medical Disclaimer System

│- **Fast Inference**: ~10 seconds average response time with Llama 3.2## 🏗️ Architecture└── Domain Classification Engine

├── 📚 Evidence System (RAG)

│   ├── Evidence Database (config/evidence_sources.yaml)- **Scalable**: Handles multiple concurrent queries

│   ├── Semantic Similarity (SentenceTransformer)

│   ├── Keyword Matching- **Efficient**: Optimized for local execution on standard hardware```

│   └── Source Formatting & Citations

│

├── 🌐 Internet RAG System

│   ├── DuckDuckGo Search### 🎨 User Interface```

│   ├── Trusted Source Filtering

│   └── Content Extraction- Clean, modern web interface built with Bootstrap 5

│

└── 📊 Evaluation System- Real-time query processing with live status updates┌─────────────────────────────────────────────────────────────┐## 🚀 Quick Start

    ├── Faithfulness Evaluator

    ├── Interpretability Evaluator- Comprehensive metrics dashboard with visual indicators

    ├── Risk Awareness Evaluator

    ├── Calibration Evaluator- Model selection dropdown with 40+ available models│                      Web Interface (Django)                  │

    ├── Robustness Evaluator

    └── Safety Evaluator- Smart download prompts for unavailable models

```

│              Real-time UI with Query Processing              │### Prerequisites

See [TECHNICAL_FLOWCHART.md](TECHNICAL_FLOWCHART.md) for detailed system flow diagrams.

---

---

└────────────────────┬────────────────────────────────────────┘

## 🚀 Installation

## 🏗️ System Architecture

### Prerequisites

                     │- Python 3.9 or higher

- **Python 3.11+**

- **Ollama** (for local LLM inference)```

- **macOS, Linux, or Windows** (with WSL2)

┌─────────────────────────────────────────────────────────────┐┌────────────────────▼────────────────────────────────────────┐- Virtual environment (recommended)

### Step 1: Install Ollama

│                      Django Web Interface                    │

```bash

# macOS│                        (Port 8000)                           ││                    ORCHESTRATOR                              │- 8GB+ RAM for model loading

brew install ollama

└────────────────────────┬────────────────────────────────────┘

# Linux

curl -fsSL https://ollama.com/install.sh | sh                         ││  • Domain Classification (Finance/Medical/Cross-Domain)      │- **OR** Docker & Docker Compose (for containerized deployment)



# Start Ollama service                         ▼

ollama serve

```┌─────────────────────────────────────────────────────────────┐│  • Query Routing & Intent Analysis                           │



### Step 2: Pull Recommended Models│                    Orchestrator Agent                        │



```bash│            (Query Classification & Routing)                  ││  • Response Aggregation & Quality Assessment                 │### Option 1: Docker Deployment (Recommended)

# Recommended: Llama 3.2 (2GB, fastest)

ollama pull llama3.2:latest└─────────────┬────────────────────────┬──────────────────────┘



# Optional: Higher quality models              │                        │└──────┬────────────────────────────────┬────────────────────┘

ollama pull llama3:latest        # 4.7GB

ollama pull codellama:latest     # 3.8GB    ┌─────────▼─────────┐    ┌────────▼─────────┐

ollama pull mistral:latest       # 4.1GB

```    │  Finance Agent    │    │  Medical Agent   │       │                                │The fastest way to get started:



### Step 3: Clone and Setup    │  (Domain Expert)  │    │  (Domain Expert) │



```bash    └─────────┬─────────┘    └────────┬─────────┘┌──────▼────────┐              ┌────────▼──────────┐

# Clone repository

git clone https://github.com/somesh-ghaturle/Fair-Agent.git              │                        │

cd Fair-Agent

              └────────────┬───────────┘│ FINANCE AGENT │              │  MEDICAL AGENT    │```bash

# Create virtual environment

python3 -m venv .venv                           │

source .venv/bin/activate  # On Windows: .venv\Scripts\activate

                           ▼│               │              │                   │# Clone the repository

# Install dependencies

pip install -r requirements.txt              ┌────────────────────────┐



# Run database migrations              │   Ollama Server        ││ • GPT-2 Model │              │ • GPT-2 Model     │git clone <repository-url>

python3 webapp/manage.py migrate

              │   (Port 11434)         │

# Create superuser (optional)

python3 webapp/manage.py createsuperuser              │   - Llama 3.2          ││ • Investment  │              │ • Health Info     │cd Fair-Agent

```

              │   - Mistral            │

---

              │   - Gemma              ││ • Market Data │              │ • Safety Filters  │

## ⚡ Quick Start

              │   - 40+ models         │

### Start the Server

              └────────────────────────┘└──────┬────────┘              └────────┬──────────┘# Deploy with Docker

```bash

# Activate virtual environment                           │

source .venv/bin/activate

                           ▼       │                                │./docker-deploy.sh start

# Start Django development server

python3 webapp/manage.py runserver              ┌────────────────────────┐

```

              │   Enhancement Layer    │       └────────┬──────────┬────────────┘

### Access the Application

              │   - RAG System         │

Open your browser to: **http://127.0.0.1:8000/**

              │   - CoT Reasoning      │                │          │# Access the web interface

### Submit a Query

              │   - Disclaimer System  │

1. **Select Model**: Choose "Llama 3.2" (recommended) from the dropdown

2. **Enter Query**:               └────────────────────────┘        ┌───────▼──┐  ┌────▼─────┐  ┌──────────┐open http://localhost:8000

   - Finance: "What is portfolio diversification?"

   - Medical: "What are the side effects of aspirin?"                           │

3. **View Response**: See evidence-based response with citations

4. **Check Metrics**: Review FAIR scores in the metrics panel                           ▼        │ Internet │  │ Evidence │  │   FAIR   │```



---              ┌────────────────────────┐



## 📖 Usage              │   FAIR Evaluators      │        │   RAG    │  │ Database │  │Enhancement│



### Web Interface              │   - Faithfulness       │



The web interface provides:              │   - Interpretability   │        │ (Real-   │  │ (Curated │  │(Safety & │See [DOCKER_README.md](DOCKER_README.md) for detailed Docker deployment instructions.

- **Query Input**: Large text area for questions

- **Model Selection**: Dropdown with 40+ Ollama models              │   - Risk Awareness     │

- **Real-time Processing**: Visual feedback during generation

- **Response Display**: Formatted response with citations              │   - Calibration        │        │  time)   │  │ Sources) │  │Metrics)  │

- **Metrics Panel**: Live FAIR scores with definitions

- **Query History**: Recent queries in the session              └────────────────────────┘



### Example Queries```        └──────────┘  └──────────┘  └──────────┘### Option 2: Local Installation



#### Finance Queries

```

✅ "Should I invest in cryptocurrency?"---```

✅ "How do interest rates affect bond prices?"

✅ "What is the best retirement savings strategy?"

✅ "How much should I have in an emergency fund?"

```## 🛠️ Installation1. **Clone the repository**



#### Medical Queries

```

✅ "What are the benefits and risks of aspirin therapy?"### Prerequisites### Component Breakdown```bash

✅ "How should I manage type 2 diabetes?"

✅ "What are the side effects of COVID-19 vaccines?"

✅ "When should I call 911 for a mental health crisis?"

```- **Python**: 3.9 or highergit clone <repository-url>



#### Cross-Domain Queries- **Ollama**: For local LLM inference

```

✅ "How much does cancer treatment cost?" (Medical + Finance)- **Operating System**: macOS, Linux, or Windows with WSL#### 1. **Orchestrator** (`src/agents/orchestrator.py`)cd Fair-Agent

✅ "What is health insurance deductible?" (Finance + Medical)

```- **Memory**: 8GB+ RAM (16GB recommended for larger models)



---- **Domain Classification**: Uses keyword matching and context analysis to route queries```



## 📊 FAIR Metrics### Step 1: Clone Repository



### What Are FAIR Metrics?- **Special Handling**: Single-word queries, ambiguous contexts, cross-domain topics



FAIR metrics evaluate AI system trustworthiness across six dimensions:```bash



| Metric | Definition | Current Score | Target Score |git clone https://github.com/somesh-ghaturle/Fair-Agent.git- **Response Synthesis**: Aggregates multi-agent outputs for complex queries2. **Set up virtual environment**

|--------|------------|---------------|--------------|

| **Faithfulness** | Accuracy and factual correctness based on evidence | 29.7% → 50-60% | ≥50% |cd Fair-Agent

| **Interpretability** | Clarity of reasoning with step-by-step explanations | 48.3% → 65-72% | ≥65% |

| **Risk Awareness** | Identification and communication of risks/limitations | 56.2% → 72-78% | ≥70% |``````bash

| **Calibration** | Alignment between confidence scores and accuracy | Varies | High |

| **Robustness** | Consistency across query variations | Varies | High |

| **Safety** | Harmful content detection and filtering | Varies | 100% |

### Step 2: Create Virtual Environment#### 2. **Finance Agent** (`src/agents/finance_agent.py`)python -m venv .venv

### How Metrics Are Calculated



- **Faithfulness**: Evidence citations, factual grounding, source reliability

- **Interpretability**: Step-by-step structure, clear reasoning, defined terms```bash- **Base Model**: GPT-2 with finance-specific fine-tuning capabilitysource .venv/bin/activate  # On Windows: .venv\Scripts\activate

- **Risk Awareness**: Disclaimers present, risks mentioned, limitations stated

- **Calibration**: Confidence score vs actual accuracy correlationpython3 -m venv .venv

- **Robustness**: Response similarity for paraphrased queries

- **Safety**: Harmful keyword detection, appropriate disclaimerssource .venv/bin/activate  # On Windows: .venv\Scripts\activate- **Specializations**: Investment, budgeting, market analysis, risk assessment```



---```



## 📁 Project Structure- **Enhancement Pipeline**: Internet RAG → Evidence DB → FAIR Safety



```### Step 3: Install Dependencies

Fair-Agent/

│- **Template System**: High-quality fallback responses for common queries3. **Install dependencies**

├── config/

│   ├── config.yaml              # Main configuration```bash

│   ├── evidence_sources.yaml    # Evidence database (16 sources)

│   └── system_config.yaml       # System settingspip install --upgrade pip```bash

│

├── src/pip install -r requirements.txt

│   ├── agents/

│   │   ├── orchestrator.py      # Query routing & coordination```#### 3. **Medical Agent** (`src/agents/medical_agent.py`)pip install -r requirements.txt

│   │   ├── finance_agent.py     # Finance domain specialist

│   │   └── medical_agent.py     # Medical domain specialist

│   │

│   ├── core/### Step 4: Install Ollama- **Base Model**: GPT-2 with medical knowledge adaptation```

│   │   ├── config.py            # Configuration management

│   │   └── system.py            # Core system initialization

│   │

│   ├── evaluation/**macOS/Linux:**- **Safety Features**: Multi-layer harmful content detection, inappropriate query filtering

│   │   ├── faithfulness.py      # Faithfulness evaluator

│   │   ├── interpretability.py  # Interpretability evaluator```bash

│   │   ├── calibration.py       # Calibration evaluator

│   │   ├── robustness.py        # Robustness evaluatorcurl -fsSL https://ollama.com/install.sh | sh- **Specializations**: Diseases, medications, symptoms, wellness4. **Run the system**

│   │   └── safety.py            # Safety evaluator

│   │```

│   ├── evidence/

│   │   └── rag_system.py        # Evidence retrieval & RAG- **Template System**: Educational responses with professional consultation disclaimers```bash

│   │

│   ├── reasoning/**Windows:**

│   │   └── cot_system.py        # Chain-of-Thought integration

│   │Download from [https://ollama.com/download](https://ollama.com/download)# Web interface (recommended)

│   ├── safety/

│   │   └── disclaimer_system.py # Disclaimer generation

│   │

│   └── utils/### Step 5: Install Models#### 4. **Enhancement Systems**python main.py --mode web

│       └── logger.py            # Logging utilities

│

├── webapp/

│   ├── fair_agent_app/Use the interactive installer script:

│   │   ├── views.py             # Django views

│   │   ├── services.py          # FAIR-Agent service layer

│   │   ├── models.py            # Database models

│   │   └── api_urls.py          # API endpoints```bash##### Internet RAG (`src/data_sources/internet_rag.py`)# CLI interface

│   │

│   ├── templates/chmod +x scripts/install_ollama_models.sh

│   │   └── fair_agent_app/

│   │       └── query_interface_clean.html  # Main UI./scripts/install_ollama_models.sh- **Real-time Data Sources**:python main.py --mode cli

│   │

│   ├── static/```

│   │   ├── css/

│   │   └── js/  - 🏦 Finance: Investopedia, SEC EDGAR, Yahoo Finance

│   │

│   ├── manage.py                # Django managementOr install models manually:

│   └── settings.py              # Django settings

│  - 🏥 Medical: Mayo Clinic, CDC, NIH MedlinePlus# With custom port and debug mode

├── test_evidence_system.py      # Evidence system tests

├── test_model_switching.py      # Model switching tests```bash

├── requirements.txt             # Python dependencies

├── README.md                    # This file# Fast, small model (recommended for testing)- **Source Reliability Scoring**: 95% for primary sourcespython main.py --mode web --port 8080 --debug

└── TECHNICAL_FLOWCHART.md       # Detailed technical documentation

```ollama pull llama3.2:latest



---- **Citation Integration**: Automatic source attribution in responses```



## ⚙️ Configuration# High-quality general model



### Evidence Sources (`config/evidence_sources.yaml`)ollama pull llama3:latest



The evidence database contains 16 curated sources:



**Medical Sources (8)**:# Medical-specific model##### Evidence Database (`src/evidence/rag_system.py`)### Alternative Django Method

- Aspirin therapy (cardiovascular prevention)

- Diabetes management (metformin, lifestyle)ollama pull meditron:latest

- Hypertension control (medication, monitoring)

- Mental health crisis (suicide prevention, 988 hotline)- **8 Curated Sources**: High-quality, domain-specific content

- Antibiotic stewardship (resistance prevention)

- COVID-19 vaccination (safety, efficacy)# Finance-specific model

- Cholesterol management (statins, lifestyle)

- Pain management (opioid guidelines)ollama pull finbert:latest- **Reliability Metrics**: Per-source scoring (85-95% range)```bash



**Finance Sources (8)**:```

- Portfolio diversification (modern portfolio theory)

- Bond-interest rate relationship (duration, convexity)- **Semantic Search**: Query-context matching for relevant evidencecd webapp

- Cryptocurrency risks (volatility, regulation)

- Retirement planning (401k, IRA, strategies)### Step 6: Initialize Database

- Index fund investing (passive vs active)

- Emergency fund recommendations (3-6 months)- **Coverage Analysis**: Response improvement trackingpython manage.py runserver

- Debt management (payoff strategies)

- Real estate investment (REITs, direct ownership)```bash



### Model Configuration (`config/config.yaml`)cd webapp```



```yamlpython manage.py migrate

models:

  finance:cd ..##### FAIR Enhancement (`src/safety/disclaimer_system.py`)

    model_name: "gpt2"           # Default startup model

    device: "auto"               # Auto-detect GPU/CPU```

    max_length: 256

    - **Safety Disclaimers**: Domain-appropriate warnings## 🎮 Usage Examples

  medical:

    model_name: "gpt2"---

    device: "auto"

    max_length: 256- **FAIR Metrics**: Embedded accountability measures

```

## 🚀 Quick Start

**Note**: The system dynamically switches to your selected Ollama model when you submit a query. The config.yaml model is only used for initial startup.

- **Improvement Tracking**: Response enhancement scoring### Web Interface

---

### Start Ollama Server

## 🤖 Model Support

1. Open your browser to `http://127.0.0.1:8000`

### Ollama Models (Recommended)

```bash

| Model | Size | Speed | Quality | Use Case |

|-------|------|-------|---------|----------|ollama serve#### 5. **Evaluation Framework** (`src/evaluation/`)2. Navigate to the Query page

| **llama3.2:latest** | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | General purpose (Recommended) |

| llama3:latest | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | High quality responses |```

| codellama:latest | 3.8GB | ⚡⚡ | ⭐⭐⭐ | Code-focused queries |

| mistral:latest | 4.1GB | ⚡⚡ | ⭐⭐⭐⭐ | Balanced performance |- **Faithfulness**: Fact accuracy and source grounding3. Enter your question (finance, medical, or general)

| gemma:2b | 1.4GB | ⚡⚡⚡ | ⭐⭐ | Ultra-fast, basic queries |

Keep this running in a separate terminal.

### How to Add Models

- **Calibration**: Confidence score accuracy4. View comprehensive analysis with FAIR metrics

```bash

# List available models### Start FAIR-Agent Web Interface

ollama list

- **Interpretability**: Response clarity and explainability

# Pull a new model

ollama pull <model-name>```bash



# Example: Pull Llama 3.1python main.py --mode web --port 8000- **Robustness**: Adversarial input handling### CLI Interface

ollama pull llama3.1:latest

``````



Models automatically appear in the web interface dropdown once pulled.- **Safety**: Harm detection and mitigation```bash



### Model SwitchingOr run Django directly:



The system supports **dynamic model switching**:python main.py --mode cli

- Select any model from the dropdown

- Submit query```bash

- System automatically switches to that model

- No server restart requiredcd webapp---



**Logging Example**:python manage.py runserver 8000

```

INFO [STARTUP] FAIR-Agent initialized with Finance=gpt2, Medical=gpt2```> what is diabetes treatment

INFO [QUERY] 📝 Processing query with selected model: llama3.2:latest

INFO [QUERY] 🔄 Switching models from gpt2 to llama3.2:latest

INFO ✅ Finance Agent using Ollama model: llama3.2:latest

```### Access the Application## 🚀 Quick StartDomain: medical



---



## 🔌 API DocumentationOpen your browser and navigate to:Confidence: 0.92



### POST `/api/query/process/````



Submit a query for processing.http://127.0.0.1:8000### PrerequisitesAnswer: [Medical Agent provides detailed diabetes treatment information]



**Request**:```

```json

{

  "query": "What are the side effects of aspirin?",

  "model": "llama3.2:latest"### Try Your First Query

}

```- Python 3.11+> explain stock market analysis



**Response**:1. Select a model from the dropdown (e.g., "Llama 3.2")

```json

{2. Enter a query in the text area:- pip or condaDomain: finance  

  "status": "success",

  "response": "Based on clinical guidelines [Source 1]...",   - Finance: "What are the key factors affecting stock market volatility?"

  "metrics": {

    "faithfulness": 0.65,   - Medical: "What are the symptoms and treatment for hypertension?"- macOS (with MPS support) or Linux/Windows with CUDA (optional)Confidence: 0.88

    "interpretability": 0.72,

    "risk_awareness": 0.78,3. Click **"Process with FAIR Agent"**

    "calibration": 0.70,

    "robustness": 0.68,4. View the response and FAIR metrics in the dashboardAnswer: [Finance Agent provides market analysis insights]

    "safety": 1.0

  },

  "domain": "medical",

  "model_used": "llama3.2:latest",---### Installation```

  "processing_time": 4.2,

  "evidence_sources": 2

}

```## 🎯 Model Selection



### GET `/api/models/available/`



Get list of available models.### Installed Models (4)1. **Clone the repository**### Example Queries



**Response**:

```json

{- **Llama 3.2** (2GB) - Default, fast, general-purpose```bash

  "ollama_models": [

    "llama3.2:latest",- **Llama 3** (4.7GB) - High-quality, versatile

    "llama3:latest",

    "codellama:latest"- **GPT-OSS** (13GB) - Open-source GPT alternativegit clone https://github.com/somesh-ghaturle/Fair-Agent.git**Medical Domain:**

  ],

  "huggingface_models": [- **CodeLlama** (3.8GB) - Code-focused model

    "gpt2"

  ]cd Fair-Agent- "What are the treatment options for diabetes?"

}

```### Available Models (40+)



---```- "Explain the side effects of hypertension medication"



## 🛠 DevelopmentThe system supports a wide range of models categorized by domain:



### Running Tests- "How does cholesterol affect heart health?"



```bash#### 🏥 Medical Models

# Test evidence system

python3 test_evidence_system.py- `meditron:latest` - Medical domain specialist2. **Create virtual environment**



# Test model switching- `medllama2:latest` - Healthcare-focused Llama

python3 test_model_switching.py

- `openbiollm:latest` - Biomedical research```bash**Finance Domain:**

# Run Django tests

python3 webapp/manage.py test- `biomistral:latest` - Medical Mistral variant

```

python3 -m venv .venv- "Analyze the risk of investing in tech stocks"

### Viewing Logs

#### 💰 Finance Models

Logs appear in the terminal running the Django server:

- `[STARTUP]` - Initial system loading- `finbert:latest` - Financial analysis specialistsource .venv/bin/activate  # On Windows: .venv\Scripts\activate- "What factors affect mortgage interest rates?"

- `[QUERY]` - Query processing and model switching

- `✅` - Successful operations- `finchat:latest` - Finance conversational model

- `⚠️` - Warnings

- `❌` - Errors- `llama-finance:latest` - Finance-tuned Llama```- "Explain portfolio diversification strategies"



### Adding New Evidence Sources



Edit `config/evidence_sources.yaml`:#### 🌟 General Models



```yaml- `mistral:latest` - High performance

medical_sources:

  - id: "med_009"- `gemma:latest` - Google's efficient model3. **Install dependencies****Cross-Domain:**

    title: "New Medical Topic"

    content: |- `phi:latest` - Microsoft's compact model

      Detailed medical information here...

    source_type: "clinical_guideline"- `qwen:latest` - Alibaba's multilingual model```bash- "What are the financial implications of healthcare costs?"

    url: "https://trusted-source.com/article"

    publication_date: "2024-01-01"

    reliability_score: 0.95

    domain: "medical"#### ⚡ Fast/Small Modelspip install -r requirements.txt- "How do pharmaceutical investments perform?"

    keywords: ["keyword1", "keyword2", "synonym1", "synonym2"]

```- `tinyllama:latest` - Ultra-fast, 1.1B parameters



**Important**: Include 12-15 keywords with:- `stablelm:latest` - Stable and efficient```

- Medical terms

- Common synonyms- `orca-mini:latest` - Compact but capable

- Action verbs (manage, treat, control)

- Related concepts## 📊 FAIR Metrics



### Modifying FAIR Metrics### Downloading New Models



Edit evaluators in `src/evaluation/`:4. **Configure environment** (optional)

- `faithfulness.py` - Evidence citation detection

- `interpretability.py` - Structured response checkingWhen you select an unavailable model, the UI will display:

- `risk_awareness.py` - Disclaimer and risk detection

```bash```bashThe system evaluates responses across multiple dimensions with realistic GPT-2 based scoring:

---

ollama pull <model-name>

## 📝 License

```cp .env.example .env

MIT License - see LICENSE file for details



---

Copy and run this command in your terminal to download.# Edit .env with your API keys if using external services- **Faithfulness** (25-60%): Accuracy and consistency with source information

## 👤 Author



**Somesh Ghaturle**  

CS668 Analytics Capstone - Fall 2025---```- **Interpretability** (40-60%): Clarity and explainability of responses with enhanced reasoning



---



## 🙏 Acknowledgments## 📁 Project Structure- **Risk-Awareness** (56-76%): Safety and risk assessment capabilities with domain-specific disclaimers



- **Ollama** - Local LLM inference framework

- **Django** - Web framework

- **HuggingFace** - Model hosting and transformers library```### Running the System- **Calibration Error** (30-70%): Confidence calibration accuracy

- **PyTorch** - Deep learning framework

- **SentenceTransformers** - Semantic similarityFair-Agent/



---├── main.py                          # Main entry point- **Robustness** (20-25%): Performance under various conditions, reflecting base model limitations



## 📚 References├── requirements.txt                 # Python dependencies



- Medical evidence: CDC, NIH, Mayo Clinic├── README.md                        # This file#### Web Interface (Recommended)

- Finance evidence: SEC, Investopedia, JSTOR

- FAIR metrics: AI safety research literature│



---├── config/                          # Configuration files```bash*Note: Scores reflect realistic GPT-2 model capabilities after system recalibration.*



## 🚨 Important Disclaimers│   ├── config.yaml                  # Agent and dataset config



### Medical│   └── system_config.yaml           # System settingspython3 main.py --mode web --port 8000

**This system is NOT a substitute for professional medical advice.** Always consult qualified healthcare providers for medical decisions. In emergencies, call 911.

│

### Financial

**This system provides educational information only, NOT financial advice.** Consult licensed financial advisors before making investment decisions. Past performance doesn't guarantee future results.├── src/                             # Source code```## 🔧 Configuration



---│   ├── agents/                      # Agent implementations



**Version**: 1.0.0  │   │   ├── finance_agent.py         # Finance domain agentAccess at: **http://127.0.0.1:8000/**

**Last Updated**: October 4, 2025

│   │   ├── medical_agent.py         # Medical domain agent

│   │   └── orchestrator.py          # Orchestrator agent### System Configuration (`config/system_config.yaml`)

│   │

│   ├── core/                        # Core system components#### CLI Mode

│   │   ├── config.py                # Configuration loader

│   │   └── system.py                # Main system class```bash```yaml

│   │

│   ├── evaluation/                  # FAIR metrics evaluatorspython3 main.py --mode clifinance_agent:

│   │   ├── faithfulness.py          # Faithfulness evaluator

│   │   ├── interpretability.py      # Interpretability evaluator```  model_name: "gpt2"

│   │   ├── calibration.py           # Calibration evaluator

│   │   ├── robustness.py            # Robustness evaluator  device: "auto"

│   │   └── safety.py                # Safety evaluator

│   │#### API Only  max_length: 256

│   ├── evidence/                    # Evidence retrieval

│   │   └── rag_system.py            # RAG implementation```bash

│   │

│   ├── reasoning/                   # Reasoning systemspython3 main.py --mode api --port 8000medical_agent:

│   │   └── cot_system.py            # Chain-of-Thought reasoning

│   │```  model_name: "gpt2"  

│   ├── safety/                      # Safety mechanisms

│   │   └── disclaimer_system.py     # Disclaimer generation  device: "auto"

│   │

│   ├── training/                    # Model training### Docker Deployment  max_length: 256

│   │   └── fine_tuning.py           # Fine-tuning utilities

│   │

│   └── utils/                       # Utility modules

│       ├── logger.py                # Logging configuration```bashsystem:

│       └── ollama_client.py         # Ollama API wrapper

│# Build and run  enable_cross_domain: true

├── webapp/                          # Django web application

│   ├── manage.py                    # Django management scriptdocker-compose up --build  web_port: 8000

│   ├── settings.py                  # Django settings

│   ├── urls.py                      # URL routing  debug_mode: false

│   ├── asgi.py                      # ASGI configuration

│   ├── wsgi.py                      # WSGI configuration# Access at http://localhost:8000```

│   ├── db.sqlite3                   # SQLite database

│   │```

│   ├── fair_agent_app/              # Main Django app

│   │   ├── views.py                 # View controllers### Environment Variables

│   │   ├── services.py              # Business logic

│   │   ├── models.py                # Database models---

│   │   ├── urls.py                  # App URL routing

│   │   ├── api_urls.py              # API endpoints```bash

│   │   └── consumers.py             # WebSocket consumers

│   │## 💡 Usage Examples# Optional: Set custom configuration

│   ├── templates/                   # HTML templates

│   │   ├── base.html                # Base templateexport FAIR_AGENT_CONFIG="config/custom_config.yaml"

│   │   └── fair_agent_app/

│   │       └── query_interface_clean.html### Finance Queries

│   │

│   ├── static/                      # Static files# Optional: Enable debug logging

│   │   ├── css/

│   │   │   └── fair-agent.css       # Custom styles**Query**: "What are good investment strategies?"export FAIR_AGENT_DEBUG="true"

│   │   └── js/                      # JavaScript files

│   │```

│   └── logs/                        # Application logs

│       └── fair_agent_webapp.log**Response Includes**:

│

├── scripts/                         # Utility scripts- Investment fundamentals (diversification, risk management)## 📁 Project Structure

│   ├── evaluate.py                  # Evaluation script

│   └── install_ollama_models.sh     # Model installer- Real-time data from Investopedia

│

└── data/                            # Data directory- Evidence-based recommendations with source citations```

    ├── training_data_manager.py     # Training data management

    └── evidence/                    # Evidence data- FAIR safety disclaimers about financial adviceFair-Agent/

```

├── main.py                 # Main entry point

---

**Query**: "money"├── requirements.txt        # Dependencies

## 💻 Usage

├── README.md              # This file

### Web Interface Mode (Default)

**Response Includes**:├── config/                # Configuration files

```bash

python main.py --mode web --port 8000- Comprehensive overview of currency and monetary systems│   └── system_config.yaml

```

- Investment principles and wealth building strategies├── src/                   # Core system code

Features:

- Interactive query interface- Educational content with professional advisor disclaimers│   ├── core/             # System initialization & coordination

- Real-time response generation

- Live FAIR metrics visualization│   │   ├── system.py     # Main system class

- Model selection dropdown

- Query history### Medical Queries│   │   └── config.py     # Configuration management



### CLI Mode│   ├── agents/           # AI agents



```bash**Query**: "What is diabetes?"│   │   ├── orchestrator.py

python main.py --mode cli

```│   │   ├── finance_agent.py



Interactive command-line interface for testing queries.**Response Includes**:│   │   └── medical_agent.py



### API Mode- Educational overview of diabetes mellitus│   ├── evaluation/       # FAIR metrics evaluation



```bash- Symptom descriptions and types (Type 1, Type 2, gestational)│   │   ├── faithfulness.py

python main.py --mode api

```- Management strategies with professional consultation disclaimers│   │   ├── interpretability.py



Runs API server only without web interface.- Source citations from Mayo Clinic and CDC│   │   ├── calibration.py



### Django Management Commands│   │   ├── robustness.py



```bash**Query**: "medicine"│   │   └── safety.py

cd webapp

│   └── utils/            # Utilities

# Run development server

python manage.py runserver 8000**Response Includes**:│       └── logger.py



# Create database migrations- Overview of pharmacology and medical treatments├── webapp/               # Django web interface

python manage.py makemigrations

- Safety information about medication usage│   ├── manage.py

# Apply migrations

python manage.py migrate- Strong disclaimers to consult healthcare professionals│   ├── settings.py



# Create superuser│   ├── urls.py

python manage.py createsuperuser

### Cross-Domain Queries│   ├── fair_agent_app/

# Collect static files

python manage.py collectstatic│   │   ├── views.py

```

**Query**: "How does stress affect heart health?"│   │   ├── models.py

---

│   │   ├── services.py

## 📊 FAIR Metrics

**Response Includes**:│   │   └── urls.py

### Faithfulness (Target: 30%)

Measures how accurately the response adheres to factual information and domain knowledge.- Medical agent analysis of cardiovascular impacts│   └── templates/



**Evaluation Criteria:**- Finance agent perspective on healthcare costs│       ├── base.html

- Factual accuracy

- Evidence-based claims- Orchestrator synthesis of both viewpoints│       ├── home.html

- Source attribution

- Logical consistency- Holistic recommendations with appropriate disclaimers│       └── query.html



### Interpretability (Target: 50%)└── scripts/              # Utility scripts

Evaluates how clear, explainable, and understandable the response is.

---    ├── evaluate.py

**Evaluation Criteria:**

- Clarity of language    └── run_pipeline.py

- Logical structure

- Explanation quality## 🛠️ Configuration```

- Reasoning transparency



### Risk Awareness (Target: 60%)

Assesses the agent's ability to identify and communicate potential risks and limitations.### System Configuration (`config/system_config.yaml`)## 🧪 Testing



**Evaluation Criteria:**

- Risk identification

- Disclaimer presence```yaml### Manual Testing

- Limitation acknowledgment

- Safety warningsagents:1. Start the system: `python main.py --mode web`



### Calibration  finance:2. Test various query types through the web interface

Measures confidence alignment with actual accuracy.

    model_name: "gpt2"3. Verify domain classification accuracy

**Evaluation Criteria:**

- Confidence scores    max_length: 5124. Check FAIR metrics scores

- Prediction accuracy

- Uncertainty quantification    temperature: 0.7

- Probability calibration

    confidence_threshold: 0.6### CLI Testing

---

  ```bash

## ⚙️ Configuration

  medical:python main.py --mode cli

### Model Configuration (`config/config.yaml`)

    model_name: "gpt2"> status  # Check system status

```yaml

models:    max_length: 512> help    # Show available commands

  finance:

    model_name: "llama3.2:latest"    temperature: 0.7> config  # Show configuration

    device: "auto"

    max_length: 256    safety_threshold: 0.8```

    

  medical:

    model_name: "llama3.2:latest"

    device: "auto"orchestrator:## 🔍 Domain Classification

    max_length: 256

```  routing_confidence_threshold: 0.7



### System Configuration (`config/system_config.yaml`)  enable_cross_domain: trueThe system automatically classifies queries into:



```yaml

orchestrator:

  enable_cross_domain: trueenhancement:- **Medical**: Health, disease, treatment, symptoms, medication

  confidence_threshold: 0.7

    enable_internet_rag: true- **Finance**: Investment, market, portfolio, economics, financial analysis  

evaluation:

  enable_metrics: true  enable_evidence_db: true- **Cross-Domain**: Queries spanning both domains

  metrics:

    - faithfulness  enable_fair_enhancement: true- **General**: Topics outside core domains

    - interpretability

    - risk_awareness```

    - calibration

```### Classification Features



### Django Settings (`webapp/settings.py`)### FAIR Metrics Configuration (`config/fair_metrics_config.py`)- Keyword-based matching with adaptive thresholds



- Database: SQLite (default)- Pattern recognition for domain-specific terms

- Debug mode: Enabled in development

- Allowed hosts: localhost, 127.0.0.1Customize evaluation criteria, thresholds, and scoring weights for:- Fallback handling for ambiguous queries

- Static files: `/static/`

- Media files: `/media/`- Faithfulness scoring- Special handling for single strong domain terms



---- Calibration accuracy



## 🔧 Development- Interpretability metrics## 🛠 Development



### Running Tests- Robustness testing



```bash- Safety assessment### Adding New Features

# Run all tests

python -m pytest1. Extend agents in `src/agents/`



# Run specific test file---2. Add evaluation metrics in `src/evaluation/`

python -m pytest scripts/evaluate.py

3. Update web interface in `webapp/`

# Run with coverage

python -m pytest --cov=src## 📊 FAIR Metrics Explained4. Modify configuration in `config/`

```



### Code Style

### F - Faithfulness### Code Quality

```bash

# Format code with black**Measures**: How accurately the agent's response reflects factual information- Follow PEP 8 style guidelines

black src/ webapp/

- Source grounding verification- Add comprehensive docstrings

# Lint with flake8

flake8 src/ webapp/- Fact-checking against knowledge base- Include type hints where appropriate



# Type checking with mypy- Citation accuracy- Test new features thoroughly

mypy src/

```- **Target**: > 85% faithfulness score



### Adding New Models## 📝 System Logs



1. Install model via Ollama:### A - Accountability  

```bash

ollama pull <model-name>**Measures**: Transparency and traceability of agent decisionsThe system provides comprehensive logging:

```

- Source attribution- Agent initialization and model loading

2. Add to dropdown in `webapp/templates/fair_agent_app/query_interface_clean.html`:

```html- Confidence score reporting- Query processing and domain classification  

<option value="<model-name>">Model Display Name</option>

```- Decision pathway logging- FAIR metrics evaluation



3. Test with a query to ensure compatibility.- **Target**: All responses include sources- Error handling and debugging



### Adding New Agents



1. Create agent class in `src/agents/`:### I - InterpretabilityLogs are displayed in console and optionally saved to files.

```python

from src.agents.base_agent import BaseAgent**Measures**: Clarity and explainability of responses



class NewAgent(BaseAgent):- Response structure analysis## ⚠ Important Notes

    def __init__(self, model_name="llama3.2:latest"):

        super().__init__(model_name)- Plain language usage

        # Initialize domain-specific components

        - Reasoning transparency### Model Compatibility

    def process_query(self, query: str) -> dict:

        # Implement query processing- **Target**: > 80% readability score- Currently uses GPT-2 for maximum compatibility

        pass

```- Supports MPS (Apple Silicon), CUDA (NVIDIA), and CPU



2. Register in orchestrator (`src/agents/orchestrator.py`)### R - Robustness- Models are loaded on-demand for memory efficiency

3. Update routing logic

4. Add evaluation metrics**Measures**: Consistent performance across diverse inputs



### Logging- Adversarial input handling### Safety Considerations



Logs are stored in:- Edge case management- Medical responses include safety disclaimers

- `webapp/logs/fair_agent_webapp.log` - Web application logs

- Console output - Real-time debugging- Quality consistency- Financial advice includes risk warnings



Configure logging in `src/utils/logger.py`.- **Target**: < 5% failure rate- Input sanitization for security



---- Rate limiting for web interface



## 🎓 Academic Context### Safety



**Course:** CS668 Analytics Capstone - Fall 2025  **Measures**: Harm prevention and ethical considerations### Performance

**Institution:** [Your Institution]  

**Project Focus:** Multi-agent AI systems with FAIR principles- Harmful content detection- Initial model loading may take 1-2 minutes



### Research Areas- Inappropriate query filtering- Subsequent queries are processed quickly



- Multi-agent system orchestration- Disclaimer inclusion- Memory usage: ~4-6GB with both agents loaded

- Domain-specific language model fine-tuning

- Interpretability and explainability in AI- **Target**: 100% harmful content blocked

- Risk assessment in AI systems

- Model calibration and uncertainty quantification## 🤝 Contributing



------



## 📝 LicenseThis is an academic project for CS668 Analytics Capstone. For improvements or suggestions:



This project is developed for academic purposes as part of CS668 Analytics Capstone.## 🧪 Testing



---1. Review the current implementation



## 🤝 Contributing### Run Enhancement Systems Test2. Propose changes through detailed documentation



This is an academic project. For questions or suggestions:```bash3. Ensure compatibility with existing features



**Author:** Somesh Ghaturle  python3 test_enhancements.py4. Test thoroughly before submission

**GitHub:** [@somesh-ghaturle](https://github.com/somesh-ghaturle)

```

---

Validates:## 📞 Support

## 🙏 Acknowledgments

- Internet RAG integration

- **Ollama**: For providing excellent local LLM infrastructure

- **Hugging Face**: For transformers library and model hub- Evidence DB enhancementFor questions or issues related to this capstone project, please refer to:

- **Django**: For robust web framework

- **Open-source community**: For all the amazing tools and models- FAIR metrics enhancement- Course materials and documentation



---- Agent system integration- System logs for debugging information



## 📚 References- Configuration files for customization options



- [Ollama Documentation](https://ollama.com/docs)### Run Comprehensive Evaluation

- [Django Documentation](https://docs.djangoproject.com/)

- [Hugging Face Transformers](https://huggingface.co/docs/transformers)```bash---

- [FAIR Principles for AI](https://www.go-fair.org/fair-principles/)

python3 scripts/evaluate.py --domain finance --metrics all

---

python3 scripts/evaluate.py --domain medical --metrics all## 🏆 Academic Project Information

**Built with ❤️ for CS668 Analytics Capstone - Fall 2025**

```

**Course**: CS668 Analytics Capstone - Fall 2025  

### Manual Testing**Institution**: Pace University  

```python**Team Members**: 

from src.core.system import FairAgentSystem- Somesh Ramesh Ghaturle

- Darshil Malaviya  

# Initialize system- Priyank Mistry

system = FairAgentSystem()

![FAIR-Agent Logo](https://img.shields.io/badge/FAIR-Agent-blue.svg) ![Python](https://img.shields.io/badge/python-3.9+-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)

# Test query

response = system.query("What is portfolio diversification?")

print(response.primary_answer)

print(f"Confidence: {response.confidence_score}")## 📄 License

print(f"Domain: {response.domain}")

```MIT License - Copyright (c) 2025 FAIR-Agent Team



---## ⚠️ Disclaimer



## 📁 Project StructureFAIR-Agent is a research project designed for educational and research purposes. It should not be used as a substitute for professional medical advice, diagnosis, or treatment, nor for professional financial advice. Always consult qualified professionals for important decisions in these domains.



```---

Fair-Agent/

├── main.py                          # Entry point© 2025 FAIR-Agent Team - CS668 Analytics Capstone Project

├── requirements.txt                 # Python dependencies
├── docker-compose.yml               # Docker orchestration
├── Dockerfile                       # Container definition
│
├── config/                          # Configuration files
│   ├── config.yaml                  # General config
│   ├── system_config.yaml           # System parameters
│   └── fair_metrics_config.py       # Evaluation config
│
├── src/                             # Source code
│   ├── agents/                      # Agent implementations
│   │   ├── orchestrator.py          # Central coordinator
│   │   ├── finance_agent.py         # Finance specialist
│   │   └── medical_agent.py         # Medical specialist
│   │
│   ├── core/                        # Core system
│   │   ├── config.py                # Config manager
│   │   └── system.py                # Main system class
│   │
│   ├── data_sources/                # Data enhancement
│   │   └── internet_rag.py          # Real-time RAG
│   │
│   ├── evidence/                    # Knowledge base
│   │   └── rag_system.py            # Evidence DB
│   │
│   ├── evaluation/                  # FAIR metrics
│   │   ├── faithfulness.py          # Fact accuracy
│   │   ├── calibration.py           # Confidence calibration
│   │   ├── interpretability.py      # Clarity metrics
│   │   ├── robustness.py            # Consistency testing
│   │   ├── safety.py                # Harm detection
│   │   └── comprehensive_evaluator.py
│   │
│   ├── reasoning/                   # Advanced reasoning
│   │   └── cot_system.py            # Chain-of-thought
│   │
│   ├── safety/                      # Safety systems
│   │   └── disclaimer_system.py     # FAIR enhancement
│   │
│   ├── training/                    # Model training
│   │   └── fine_tuning.py           # Domain adaptation
│   │
│   └── utils/                       # Utilities
│       └── logger.py                # Logging system
│
├── webapp/                          # Django web interface
│   ├── manage.py                    # Django manager
│   ├── settings.py                  # Django settings
│   ├── urls.py                      # URL routing
│   ├── wsgi.py / asgi.py            # WSGI/ASGI config
│   │
│   ├── fair_agent_app/              # Main application
│   │   ├── views.py                 # Request handlers
│   │   ├── services.py              # Business logic
│   │   ├── models.py                # Data models
│   │   ├── api_urls.py              # API routes
│   │   └── consumers.py             # WebSocket handlers
│   │
│   ├── templates/                   # HTML templates
│   │   ├── base.html                # Base template
│   │   └── fair_agent_app/
│   │       ├── home.html            # Landing page
│   │       └── query_interface.html # Query UI
│   │
│   ├── static/                      # Static assets
│   │   ├── css/
│   │   │   └── fair-agent.css       # Custom styles
│   │   └── js/
│   │       └── query-interface.js   # Frontend logic
│   │
│   └── logs/                        # Application logs
│
├── data/                            # Data files
│   └── training_data_manager.py     # Training data utils
│
└── scripts/                         # Utility scripts
    └── evaluate.py                  # Evaluation runner
```

---

## 🔧 Development

### Adding a New Agent

1. Create agent class in `src/agents/new_agent.py`
2. Implement base methods: `query()`, `_generate_response()`, `_enhance_with_systems()`
3. Register in orchestrator's domain classification
4. Add templates for common queries
5. Configure evaluation metrics

### Customizing Enhancement Systems

**Internet RAG**:
```python
# Add new data source
self.sources = {
    'new_source': {
        'url': 'https://example.com',
        'reliability': 0.90,
        'parser': custom_parser_function
    }
}
```

**Evidence Database**:
```python
# Add curated content
self.evidence_db.add_source(
    domain="finance",
    content="Expert knowledge here...",
    reliability=0.95
)
```

### Extending FAIR Metrics

Implement new evaluation in `src/evaluation/`:
```python
class CustomMetric:
    def evaluate(self, response: str, query: str) -> float:
        # Your evaluation logic
        return score
```

---

## 🐛 Troubleshooting

### Common Issues

**Issue**: `No module named 'torch'`
```bash
pip install torch --upgrade
```

**Issue**: MPS acceleration not working
```bash
# Check MPS availability
python3 -c "import torch; print(torch.backends.mps.is_available())"
```

**Issue**: Django server won't start
```bash
# Check port availability
lsof -i :8000

# Try different port
python3 main.py --mode web --port 8080
```

**Issue**: Low response quality
- Check if enhancement systems are enabled in config
- Verify Internet RAG can access external sources
- Review logs: `webapp/logs/fair_agent_webapp.log`

### Debug Mode

```bash
python3 main.py --mode web --debug
```
Enables:
- Verbose logging
- Stack traces in responses
- Performance metrics
- Enhancement system diagnostics

---

## 📈 Performance

### Benchmarks

**Query Response Time**:
- Simple queries: ~2-3 seconds
- Enhanced responses: ~5-8 seconds
- Cross-domain analysis: ~10-15 seconds

**Accuracy Metrics**:
- Faithfulness: 87% average
- Safety: 100% harmful content blocked
- Calibration: 82% confidence accuracy

**System Load**:
- Memory: ~2-4 GB (with models loaded)
- CPU: Moderate during inference
- GPU/MPS: Optional acceleration (3x faster)

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Style
- Follow PEP 8
- Use type hints
- Add docstrings (Google style)
- Include unit tests

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Somesh Ghaturle**  
CS668 Analytics Capstone - Fall 2025  
Pace University

---

## 🙏 Acknowledgments

- **Hugging Face Transformers** - Pre-trained language models
- **Django Framework** - Web application infrastructure
- **PyTorch** - Deep learning backend
- **Investopedia, Mayo Clinic, SEC, CDC** - Trusted data sources
- **Open Source Community** - Libraries and tools

---

## 📞 Support

For issues, questions, or suggestions:
- 📧 Email: somesh.ghaturle@pace.edu
- 🐛 Issues: [GitHub Issues](https://github.com/somesh-ghaturle/Fair-Agent/issues)
- 📖 Documentation: See `docs/` folder (coming soon)

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] GPT-4 integration as optional backend
- [ ] Voice query support
- [ ] Mobile application
- [ ] Expanded agent domains (Legal, Education)
- [ ] Advanced Chain-of-Thought reasoning
- [ ] Multi-language support
- [ ] Enhanced visualization dashboard

### Research Directions
- [ ] Federated learning for privacy-preserving fine-tuning
- [ ] Automated FAIR metrics optimization
- [ ] Explainable AI integration
- [ ] Human-in-the-loop quality control

---

**Built with ❤️ for trustworthy AI**
