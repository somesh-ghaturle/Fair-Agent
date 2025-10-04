# FAIR-Agent Technical Flowchart & Architecture

**Detailed Technical Documentation for FAIR-Agent System**

---

## Table of Contents

1. [High-Level System Flow](#1-high-level-system-flow)
2. [Component Architecture](#2-component-architecture)
3. [Query Processing Pipeline](#3-query-processing-pipeline)
4. [Agent Architecture](#4-agent-architecture)
5. [Evidence Retrieval System](#5-evidence-retrieval-system)
6. [Model Switching Mechanism](#6-model-switching-mechanism)
7. [FAIR Metrics Evaluation](#7-fair-metrics-evaluation)
8. [Data Flow Diagrams](#8-data-flow-diagrams)
9. [Database Schema](#9-database-schema)
10. [API Architecture](#10-api-architecture)

---

## 1. High-Level System Flow

```
┌──────────────┐
│   Browser    │
│   (User)     │
└──────┬───────┘
       │ HTTP Request
       ▼
┌──────────────────────────────────────────┐
│      Django Web Application              │
│  ┌────────────────────────────────────┐  │
│  │   Query Interface (HTML/JS)        │  │
│  │   - Model selector                 │  │
│  │   - Query input                    │  │
│  │   - Response display               │  │
│  │   - Metrics visualization          │  │
│  └─────────────────┬──────────────────┘  │
│                    │                      │
│                    ▼                      │
│  ┌────────────────────────────────────┐  │
│  │   views.py (Django View Layer)     │  │
│  │   - process_query_view()           │  │
│  │   - Receives: query + model        │  │
│  │   - Creates QueryRecord            │  │
│  └─────────────────┬──────────────────┘  │
│                    │                      │
│                    ▼                      │
│  ┌────────────────────────────────────┐  │
│  │  services.py (Service Layer)       │  │
│  │   - FairAgentService               │  │
│  │   - Model switching logic          │  │
│  │   - Query orchestration            │  │
│  └─────────────────┬──────────────────┘  │
└────────────────────┼──────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│         FAIR-Agent Core System                  │
│  ┌───────────────────────────────────────────┐  │
│  │         Orchestrator                      │  │
│  │   - classify_query_domain()               │  │
│  │   - route_query()                         │  │
│  │   - handle_cross_domain()                 │  │
│  └─────────┬──────────────────┬──────────────┘  │
│            │                  │                  │
│  ┌─────────▼──────────┐  ┌───▼──────────────┐  │
│  │  Finance Agent     │  │  Medical Agent   │  │
│  │  - Evidence RAG    │  │  - Evidence RAG  │  │
│  │  - LLM Generation  │  │  - Safety Check  │  │
│  │  - Disclaimer      │  │  - Disclaimer    │  │
│  └─────────┬──────────┘  └───┬──────────────┘  │
│            │                  │                  │
│            └──────────┬───────┘                  │
│                       │                          │
│  ┌────────────────────▼───────────────────────┐ │
│  │      Enhancement Systems                   │ │
│  │  ┌──────────────┐  ┌──────────────────┐   │ │
│  │  │ Evidence RAG │  │ Internet RAG     │   │ │
│  │  │ (16 sources) │  │ (DuckDuckGo)     │   │ │
│  │  └──────────────┘  └──────────────────┘   │ │
│  │  ┌──────────────┐  ┌──────────────────┐   │ │
│  │  │ Chain-of-    │  │ Disclaimer       │   │ │
│  │  │ Thought      │  │ System           │   │ │
│  │  └──────────────┘  └──────────────────┘   │ │
│  └───────────────────────┬──────────────────┘ │
│                          │                     │
│  ┌───────────────────────▼──────────────────┐ │
│  │      FAIR Metrics Evaluation             │ │
│  │  - Faithfulness  - Interpretability      │ │
│  │  - Risk Awareness - Calibration          │ │
│  │  - Robustness    - Safety                │ │
│  └──────────────────────┬───────────────────┘ │
└─────────────────────────┼──────────────────────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   Response    │
                  │   + Metrics   │
                  └───────┬───────┘
                          │
                          ▼
                  ┌───────────────┐
                  │   Browser     │
                  │  (Display)    │
                  └───────────────┘
```

---

## 2. Component Architecture

### 2.1 Django Layer (webapp/)

```
webapp/
│
├── manage.py (Django CLI)
├── settings.py (Configuration)
├── urls.py (URL routing)
│
├── fair_agent_app/
│   ├── views.py
│   │   └── process_query_view()
│   │       • Receives: query_text, model_name
│   │       • Creates: QueryRecord in database
│   │       • Calls: FairAgentService.process_query()
│   │       • Returns: JSON response
│   │
│   ├── services.py
│   │   └── FairAgentService
│   │       ├── initialize() - Load config, init orchestrator
│   │       ├── process_query() - Main query handler
│   │       └── _reinitialize_agents_with_model() - Model switching
│   │
│   ├── models.py
│   │   ├── QuerySession - User sessions
│   │   ├── QueryRecord - Individual queries
│   │   └── MetricScore - FAIR metrics storage
│   │
│   └── api_urls.py - API endpoint definitions
│
└── templates/
    └── fair_agent_app/
        └── query_interface_clean.html
            • Model selector dropdown
            • Query input textarea
            • Response display area
            • Metrics visualization
```

### 2.2 Core Agent Layer (src/agents/)

```
src/agents/
│
├── orchestrator.py
│   └── Orchestrator
│       ├── __init__() - Initialize finance/medical agents
│       ├── process_query() - Main entry point
│       │   └── Flow:
│       │       1. classify_query_domain()
│       │       2. route_query()
│       │       3. Apply FAIR enhancements
│       │       4. Evaluate metrics
│       │
│       ├── classify_query_domain()
│       │   • Checks medical keywords (medication, doctor, pain, etc.)
│       │   • Checks finance keywords (investment, stock, retirement, etc.)
│       │   • Returns: "medical", "finance", "general"
│       │
│       └── route_query()
│           • Routes to appropriate agent
│           • Handles cross-domain with both agents
│
├── finance_agent.py
│   └── FinanceAgent
│       ├── __init__() - Load model (Ollama or HuggingFace)
│       ├── query() - Main query method
│       │   └── Flow:
│       │       1. retrieve_evidence()
│       │       2. _construct_prompt_with_evidence()
│       │       3. _generate_response() (Ollama or HF)
│       │       4. _add_structured_format()
│       │       5. _add_finance_disclaimer()
│       │
│       ├── _generate_response_ollama() - Ollama API call
│       ├── _generate_response_huggingface() - HF pipeline
│       └── _add_finance_disclaimer() - Add risk warnings
│
└── medical_agent.py
    └── MedicalAgent
        ├── __init__() - Load model
        ├── query() - Main query method
        │   └── Flow:
        │       1. _check_for_harmful_query() - Safety screen
        │       2. retrieve_evidence()
        │       3. _construct_prompt_with_evidence()
        │       4. _generate_response()
        │       5. _add_structured_format()
        │       6. _add_medical_disclaimer()
        │
        └── _add_medical_disclaimer()
            • "NOT A SUBSTITUTE FOR PROFESSIONAL MEDICAL ADVICE"
            • Emergency number: 911
            • Professional consultation emphasis
```

### 2.3 Enhancement Systems

```
src/
│
├── evidence/
│   └── rag_system.py
│       └── RAGSystem
│           ├── _load_evidence_sources() - Load from YAML
│           ├── retrieve_evidence() - Find relevant sources
│           │   └── Algorithm:
│           │       1. Keyword matching (query terms vs source keywords)
│           │       2. Calculate overlap score
│           │       3. Return top_k sources
│           │
│           └── format_evidence_for_prompt() - Format citations
│
├── reasoning/
│   └── cot_system.py
│       └── ChainOfThoughtIntegrator
│           └── integrate_cot() - Add step-by-step reasoning
│
├── safety/
│   └── disclaimer_system.py
│       └── ResponseEnhancer
│           ├── add_disclaimers() - Domain-specific disclaimers
│           └── enhance_safety() - Multi-layer safety
│
└── evaluation/
    ├── faithfulness.py - Citation detection
    ├── interpretability.py - Structure checking
    ├── calibration.py - Confidence scoring
    ├── robustness.py - Consistency checking
    └── safety.py - Harmful content detection
```

---

## 3. Query Processing Pipeline

### 3.1 Detailed Flow

```
[User Submits Query]
         │
         ▼
┌─────────────────────────────────────────────┐
│ Step 1: Web Layer (views.py)               │
│  • Extract query_text and model_name        │
│  • Create QueryRecord (status: 'processing')│
│  • Log: [QUERY] 📝 Processing query...      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ Step 2: Service Layer (services.py)        │
│  • Check if model_name != current_model     │
│  • If different:                            │
│    └─> _reinitialize_agents_with_model()   │
│        • Log: [QUERY] 🔄 Switching models.. │
│        • Create new Orchestrator            │
│        • Log: ✅ Agent using Ollama model...│
│  • Call orchestrator.process_query()        │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ Step 3: Orchestrator (orchestrator.py)     │
│  • classify_query_domain()                  │
│    └─> Returns: "medical", "finance", etc. │
│  • route_query(query, domain)               │
│    └─> Selects appropriate agent           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ Step 4: Agent Processing                   │
│  A. Evidence Retrieval (rag_system.py)     │
│     • Load evidence sources from YAML       │
│     • Match keywords: query vs source       │
│     • Return top 2-3 sources                │
│     • Log: ✅ Retrieved X evidence sources  │
│                                             │
│  B. Prompt Construction                     │
│     • System prompt (domain-specific)       │
│     • Evidence sources with citations       │
│     • Query with citation instructions      │
│                                             │
│  C. LLM Generation                          │
│     • If Ollama: Call ollama_client.chat()  │
│     • If HuggingFace: Use pipeline()        │
│     • Generate response                     │
│                                             │
│  D. Response Enhancement                    │
│     • _add_structured_format()              │
│       └─> Ensure step-by-step format        │
│     • _add_disclaimer()                     │
│       └─> Add safety warnings               │
│                                             │
│  E. Internet RAG (Optional)                 │
│     • DuckDuckGo search for real-time data  │
│     • Extract content from trusted sources  │
│     • Enhance response                      │
│     • Log: Enhanced with Internet RAG       │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ Step 5: FAIR Metrics Evaluation            │
│  • Faithfulness: Count [Source X] citations │
│  • Interpretability: Check for steps        │
│  • Risk Awareness: Check for disclaimers    │
│  • Calibration: Compare confidence vs acc   │
│  • Robustness: (Not per-query)              │
│  • Safety: Scan for harmful content         │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│ Step 6: Response Assembly                  │
│  • Combine: response + metrics              │
│  • Update QueryRecord (status: 'completed') │
│  • Return JSON to frontend                  │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
         [Display to User]
```

### 3.2 Timing Breakdown

| Phase | Typical Duration | Details |
|-------|------------------|---------|
| Model Switching | 3-5s (if needed) | Only on first query or model change |
| Domain Classification | 10-50ms | Keyword + semantic matching |
| Evidence Retrieval | 100-200ms | YAML load + keyword matching |
| LLM Generation | 2-8s | Depends on model size and query complexity |
| Internet RAG | 1-3s (optional) | DuckDuckGo search + extraction |
| Metrics Evaluation | 50-100ms | Pattern matching and scoring |
| **Total** | **3-15s** | First query: ~8-15s, Subsequent: ~3-8s |

---

## 4. Agent Architecture

### 4.1 Finance Agent Flow

```
┌───────────────────────────────────────────┐
│         FinanceAgent.query()              │
└───────────────┬───────────────────────────┘
                │
                ▼
        ┌───────────────┐
        │ Step 1:       │
        │ Evidence      │
        │ Retrieval     │
        └───────┬───────┘
                │
                │ Keywords: ["diversification", "portfolio", ...]
                ▼
        ┌───────────────────────────────┐
        │ Evidence Sources (8 finance)  │
        │  fin_001: Portfolio Div       │
        │  fin_002: Bonds/Interest      │
        │  fin_003: Crypto Risks        │
        │  fin_004: Retirement          │
        │  fin_005: Index Funds         │
        │  fin_006: Emergency Fund      │
        │  fin_007: Debt Management     │
        │  fin_008: Real Estate         │
        └───────────┬───────────────────┘
                    │
                    │ Returns top 2-3 matches
                    ▼
        ┌───────────────────────────┐
        │ Step 2:                   │
        │ Construct Prompt          │
        │                           │
        │ System: "You are finance  │
        │          expert..."       │
        │ Evidence: [Source 1]      │
        │          [Source 2]       │
        │ Query: "What is..."       │
        │ Instructions: "Cite..."   │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │ Step 3:                   │
        │ Generate Response         │
        │                           │
        │ If Ollama:                │
        │  └─> ollama_client.chat() │
        │      • Model: llama3.2    │
        │      • Temperature: 0.1   │
        │                           │
        │ If HuggingFace:           │
        │  └─> pipeline()           │
        │      • Model: gpt2        │
        │      • Max tokens: 256    │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │ Step 4:                   │
        │ Add Structured Format     │
        │                           │
        │ Check for:                │
        │  • "Step 1:", "Step 2:"   │
        │  • Numbered lists         │
        │  • Section headers        │
        │                           │
        │ If missing, add structure │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────────────────┐
        │ Step 5:                               │
        │ Add Finance Disclaimer                │
        │                                       │
        │ "⚠️ INVESTMENT DISCLAIMER             │
        │  This information is for educational  │
        │  purposes only and is NOT financial   │
        │  advice. Consult a licensed financial │
        │  advisor before making investment     │
        │  decisions. Past performance does not │
        │  guarantee future results. All        │
        │  investments carry risk."             │
        └───────────┬───────────────────────────┘
                    │
                    ▼
               [Return Response]
```

### 4.2 Medical Agent Flow

```
┌───────────────────────────────────────────┐
│         MedicalAgent.query()              │
└───────────────┬───────────────────────────┘
                │
                ▼
        ┌───────────────────────┐
        │ Step 0:               │
        │ Safety Check          │
        │                       │
        │ Harmful keywords:     │
        │  • "how to die"       │
        │  • "suicide methods"  │
        │  • "illegal drugs"    │
        │                       │
        │ If detected:          │
        │  └─> Return crisis    │
        │      resources + 988  │
        └───────────┬───────────┘
                    │
                    │ Query is safe
                    ▼
        ┌───────────────┐
        │ Step 1:       │
        │ Evidence      │
        │ Retrieval     │
        └───────┬───────┘
                │
                │ Keywords: ["aspirin", "side effects", ...]
                ▼
        ┌───────────────────────────────┐
        │ Evidence Sources (8 medical)  │
        │  med_001: Aspirin Therapy     │
        │  med_002: Diabetes Mgmt       │
        │  med_003: Hypertension        │
        │  med_004: Mental Health       │
        │  med_005: Antibiotics         │
        │  med_006: COVID Vaccines      │
        │  med_007: Cholesterol         │
        │  med_008: Pain Management     │
        └───────────┬───────────────────┘
                    │
                    │ Returns top 2-3 matches
                    ▼
        ┌───────────────────────────┐
        │ Step 2:                   │
        │ Construct Prompt          │
        │                           │
        │ System: "You are medical  │
        │          expert..."       │
        │ Evidence: [Source 1]      │
        │          [Source 2]       │
        │ Query: "What are..."      │
        │ Instructions: "Cite..."   │
        │ + "EMPHASIZE seeing       │
        │    healthcare provider"   │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │ Step 3:                   │
        │ Generate Response         │
        │ (Same as Finance Agent)   │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌───────────────────────────┐
        │ Step 4:                   │
        │ Add Structured Format     │
        │ (Same as Finance Agent)   │
        └───────────┬───────────────┘
                    │
                    ▼
        ┌──────────────────────────────────────────────┐
        │ Step 5:                                      │
        │ Add Medical Disclaimer                       │
        │                                              │
        │ "🚨 CRITICAL MEDICAL DISCLAIMER              │
        │  This information is NOT a substitute for    │
        │  professional medical advice, diagnosis, or  │
        │  treatment. Always seek guidance from        │
        │  qualified healthcare providers for medical  │
        │  decisions.                                  │
        │                                              │
        │  ⚠️ EMERGENCY: Call 911 immediately for:     │
        │  • Chest pain                                │
        │  • Difficulty breathing                      │
        │  • Severe bleeding                           │
        │  • Loss of consciousness                     │
        │  • Suicidal thoughts (988 Suicide Hotline)"  │
        └───────────┬──────────────────────────────────┘
                    │
                    ▼
               [Return Response]
```

---

## 5. Evidence Retrieval System

### 5.1 Evidence Source Structure

```yaml
# config/evidence_sources.yaml

medical_sources:
  - id: "med_001"
    title: "Aspirin Therapy - Cardiovascular Prevention"
    content: |
      Aspirin therapy for cardiovascular prevention...
      [200-400 words of curated content]
    source_type: "clinical_guideline"
    url: "https://www.mayoclinic.org/..."
    publication_date: "2023-08-15"
    reliability_score: 0.95  # 95% reliability
    domain: "medical"
    keywords: 
      - "aspirin"
      - "cardiovascular"
      - "prevention"
      - "side effects"
      - "bleeding"
      - "heart attack"
      - "stroke"
      # ... 12-15 keywords total
```

### 5.2 Retrieval Algorithm

```
retrieve_evidence(query, domain, top_k=3)
│
├─> Step 1: Load evidence sources from YAML
│   └─> Filter by domain (medical or finance)
│
├─> Step 2: Keyword matching
│   For each source:
│     query_terms = query.lower().split()
│     source_keywords = source['keywords']
│     
│     overlap = 0
│     for term in query_terms:
│       if term in source_keywords:
│         overlap += 1
│     
│     relevance_score = overlap / len(query_terms)
│
├─> Step 3: Sort by relevance_score
│   sources_sorted = sorted(sources, key=lambda x: x['score'])
│
└─> Step 4: Return top_k sources
    return sources_sorted[:top_k]
```

### 5.3 Evidence Format for Prompt

```
You are a finance expert. Use the following evidence sources to answer the query.

EVIDENCE SOURCES:
[Source 1] Portfolio Diversification - Modern Portfolio Theory
Modern portfolio theory demonstrates that diversification across uncorrelated 
assets reduces portfolio risk...
Reliability: 92%
URL: https://www.jstor.org/stable/2975974

[Source 2] Interest Rate and Bond Price Relationship
Bond prices and interest rates have an inverse relationship...
Reliability: 88%
URL: https://www.investopedia.com/terms/i/interest_rate_risk.asp

QUERY: What is portfolio diversification?

INSTRUCTIONS:
1. Base your answer on the provided evidence
2. Cite sources using [Source X] notation
3. If evidence is insufficient, state limitations clearly
4. Provide step-by-step reasoning
```

---

## 6. Model Switching Mechanism

### 6.1 Switching Flow

```
[User Selects New Model]
         │
         ▼
┌──────────────────────────────────────────┐
│ Frontend (query_interface_clean.html)   │
│  • User selects "llama3.2:latest"       │
│  • JavaScript captures selection         │
│  • Sends to backend: {"model": "llama..."│
└───────────────┬──────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────┐
│ Backend (views.py)                       │
│  • Extract model_name from request       │
│  • Log: [QUERY] 📝 Processing query...  │
│  • Pass to services.py                   │
└───────────────┬──────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────┐
│ Service Layer (services.py)              │
│  current_model = orchestrator.finance_   │
│                 agent.model_name         │
│                                          │
│  if current_model != model_name:         │
│    ├─> Log: [QUERY] 🔄 Switching...     │
│    └─> _reinitialize_agents_with_model()│
│        │                                 │
│        └─> Create new Orchestrator      │
│            with model_name               │
└───────────────┬──────────────────────────┘
                │
                ▼
┌──────────────────────────────────────────┐
│ Agent Initialization                     │
│  FinanceAgent.__init__(model_name)       │
│    │                                     │
│    ├─> Check if Ollama model:           │
│    │   is_ollama = model_name.          │
│    │              startswith('llama')    │
│    │                                     │
│    ├─> If Ollama:                        │
│    │   └─> Initialize OllamaClient      │
│    │       └─> Log: ✅ using Ollama...  │
│    │                                     │
│    └─> If HuggingFace:                   │
│        └─> Load tokenizer + model       │
│            └─> Log: ✅ loaded HF...     │
└──────────────────────────────────────────┘
```

### 6.2 Model Detection Logic

```python
# finance_agent.py / medical_agent.py

def __init__(self, model_name="gpt2"):
    self.model_name = model_name
    
    # Detect Ollama models by prefix
    self.is_ollama = model_name.startswith((
        'llama',      # llama3.2:latest, llama3:latest
        'codellama',  # codellama:latest
        'mistral',    # mistral:latest
        'gemma'       # gemma:2b
    ))
    
    if self.is_ollama:
        self.ollama_client = OllamaClient()
        if not self.ollama_client.is_available():
            # Fallback to GPT-2 if Ollama not running
            self.logger.warning("Ollama not available")
            self.is_ollama = False
            self.model_name = "gpt2"
    
    # Load model based on type
    if not self.is_ollama:
        self._load_model()  # HuggingFace
    else:
        self.logger.info(f"✅ using Ollama model: {model_name}")
```

---

## 7. FAIR Metrics Evaluation

### 7.1 Faithfulness Evaluation

```python
# src/evaluation/faithfulness.py

def evaluate(self, response, context):
    """
    Measures factual accuracy based on evidence citations
    """
    score = 0.0
    
    # Check 1: Evidence citations present
    citations = re.findall(r'\[Source \d+\]', response)
    if len(citations) > 0:
        score += 0.4  # 40% for having citations
    
    # Check 2: Multiple citations (indicates thorough research)
    if len(citations) >= 2:
        score += 0.2  # 20% for multiple sources
    
    # Check 3: High-reliability sources
    if context.get('evidence_reliability', 0) >= 0.90:
        score += 0.2  # 20% for reliable sources
    
    # Check 4: Direct quotes or specific data
    if any(indicator in response for indicator in 
           ['"', 'according to', 'studies show']):
        score += 0.2  # 20% for specific references
    
    return min(score, 1.0)
```

### 7.2 Interpretability Evaluation

```python
# src/evaluation/interpretability.py

def evaluate(self, response):
    """
    Measures clarity and step-by-step reasoning
    """
    score = 0.0
    
    # Check 1: Structured format
    has_steps = bool(re.search(r'Step \d+:|^\d+\.', 
                               response, re.MULTILINE))
    if has_steps:
        score += 0.35  # 35% for step-by-step
    
    # Check 2: Clear sections
    has_sections = sum(1 for indicator in 
                       ['Overview:', 'Analysis:', 'Conclusion:']
                       if indicator in response)
    score += (has_sections / 3) * 0.25  # 25% for sections
    
    # Check 3: Defined terms
    has_definitions = bool(re.search(r'(\w+) (?:is|means|refers to)', 
                                     response))
    if has_definitions:
        score += 0.20  # 20% for defining terms
    
    # Check 4: Logical flow
    has_connectors = sum(1 for word in 
                        ['therefore', 'because', 'however', 'additionally']
                        if word in response.lower())
    score += min(has_connectors / 4, 0.20)  # 20% for logical flow
    
    return min(score, 1.0)
```

### 7.3 Risk Awareness Evaluation

```python
# src/evaluation/risk_awareness.py (custom for FAIR-Agent)

def evaluate(self, response, domain):
    """
    Measures identification of risks and limitations
    """
    score = 0.0
    
    # Check 1: Disclaimer present
    has_disclaimer = ('DISCLAIMER' in response.upper() or
                     'NOT A SUBSTITUTE' in response.upper())
    if has_disclaimer:
        score += 0.40  # 40% for having disclaimer
    
    # Check 2: Domain-specific risk mentions
    if domain == 'medical':
        risk_terms = ['side effects', 'risks', 'consult doctor', 
                     'professional', '911', 'emergency']
    else:  # finance
        risk_terms = ['risks', 'volatility', 'losses', 
                     'past performance', 'consult advisor']
    
    risks_mentioned = sum(1 for term in risk_terms 
                         if term in response.lower())
    score += min(risks_mentioned / 6, 0.30)  # 30% for risk mentions
    
    # Check 3: Limitations stated
    limitation_phrases = ['may not', 'depends on', 'varies', 
                         'individual circumstances']
    limitations = sum(1 for phrase in limitation_phrases 
                     if phrase in response.lower())
    score += min(limitations / 4, 0.30)  # 30% for limitations
    
    return min(score, 1.0)
```

---

## 8. Data Flow Diagrams

### 8.1 Evidence-Based Response Generation

```
Query: "What are the side effects of aspirin?"
│
├─> Domain Classification
│   └─> Result: "medical"
│
├─> Evidence Retrieval
│   └─> Matched: med_001 (Aspirin Therapy)
│       Keywords matched: ["aspirin", "side effects", "risks"]
│       Relevance: 0.75
│
├─> Prompt Construction
│   ┌────────────────────────────────────────┐
│   │ System: You are a medical expert...   │
│   │                                        │
│   │ Evidence:                              │
│   │ [Source 1] Aspirin Therapy             │
│   │ Common side effects include            │
│   │ gastrointestinal bleeding (5-10%)...   │
│   │ Reliability: 95%                       │
│   │                                        │
│   │ Query: What are side effects...        │
│   │                                        │
│   │ Instructions: Cite [Source 1]...       │
│   └────────────────────────────────────────┘
│
├─> LLM Generation (Ollama)
│   └─> Model: llama3.2:latest
│       Temperature: 0.1
│       Max tokens: 500
│
├─> Generated Response
│   ┌────────────────────────────────────────┐
│   │ Based on clinical guidelines [Source 1]│
│   │                                        │
│   │ Step 1: Common Side Effects           │
│   │ Aspirin can cause gastrointestinal     │
│   │ issues including:                      │
│   │ • Stomach upset (5-10% of users)       │
│   │ • Bleeding risk                        │
│   │                                        │
│   │ Step 2: Serious Risks                  │
│   │ In rare cases...                       │
│   └────────────────────────────────────────┘
│
├─> Enhancement
│   ├─> Add structure (if missing)
│   └─> Add medical disclaimer
│       ┌────────────────────────────────────┐
│       │ 🚨 CRITICAL MEDICAL DISCLAIMER      │
│       │ This is NOT medical advice...      │
│       │ Call 911 for emergencies.          │
│       └────────────────────────────────────┘
│
└─> Final Response
    ┌────────────────────────────────────────┐
    │ [Generated content with [Source 1]]    │
    │                                        │
    │ [Medical Disclaimer]                   │
    └────────────────────────────────────────┘
```

---

## 9. Database Schema

```sql
-- QuerySession
CREATE TABLE query_session (
    id INTEGER PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE,
    user_id INTEGER NULLABLE,
    created_at DATETIME,
    updated_at DATETIME
);

-- QueryRecord
CREATE TABLE query_record (
    id INTEGER PRIMARY KEY,
    session_id INTEGER FOREIGN KEY REFERENCES query_session(id),
    query_text TEXT,
    response_text TEXT,
    domain VARCHAR(50),  -- 'medical', 'finance', 'general'
    model_used VARCHAR(100),  -- 'llama3.2:latest', 'gpt2', etc.
    status VARCHAR(50),  -- 'processing', 'completed', 'failed'
    processing_time FLOAT,  -- seconds
    evidence_sources_count INTEGER,
    created_at DATETIME,
    processed_at DATETIME
);

-- MetricScore
CREATE TABLE metric_score (
    id INTEGER PRIMARY KEY,
    query_record_id INTEGER FOREIGN KEY REFERENCES query_record(id),
    metric_name VARCHAR(50),  -- 'faithfulness', 'interpretability', etc.
    score FLOAT,  -- 0.0 to 1.0
    details TEXT,  -- JSON with breakdown
    created_at DATETIME
);

-- Indexes
CREATE INDEX idx_session_id ON query_record(session_id);
CREATE INDEX idx_domain ON query_record(domain);
CREATE INDEX idx_metric_name ON metric_score(metric_name);
```

---

## 10. API Architecture

### 10.1 Endpoint Overview

```
/api/
├── query/
│   ├── process/  [POST]
│   │   • Submit query for processing
│   │   • Request: {query, model}
│   │   • Response: {response, metrics, domain, processing_time}
│   │
│   └── history/  [GET]
│       • Get query history for session
│       • Response: [{query, response, timestamp, metrics}]
│
├── models/
│   ├── available/  [GET]
│   │   • List available Ollama models
│   │   • Response: {ollama_models, huggingface_models}
│   │
│   └── switch/  [POST]
│       • Pre-switch to a model (optional)
│       • Request: {model_name}
│       • Response: {status, model_loaded}
│
└── metrics/
    ├── current/  [GET]
    │   • Get latest metric scores
    │   • Response: {faithfulness, interpretability, ...}
    │
    └── history/  [GET]
        • Get metric history over time
        • Response: [{timestamp, metrics}]
```

### 10.2 Request/Response Examples

**POST /api/query/process/**

Request:
```json
{
  "query": "What are the side effects of aspirin?",
  "model": "llama3.2:latest"
}
```

Response:
```json
{
  "status": "success",
  "response": "Based on clinical guidelines [Source 1]...\n\n🚨 CRITICAL MEDICAL DISCLAIMER...",
  "metrics": {
    "faithfulness": 0.65,
    "interpretability": 0.72,
    "risk_awareness": 0.78,
    "calibration": 0.70,
    "robustness": 0.68,
    "safety": 1.0
  },
  "domain": "medical",
  "model_used": "llama3.2:latest",
  "processing_time": 4.2,
  "evidence_sources": 2,
  "evidence_titles": [
    "Aspirin Therapy - Cardiovascular Prevention",
    "Pain Management - Opioid Guidelines"
  ],
  "query_id": 42
}
```

---

## 11. Configuration Files

### 11.1 config.yaml

```yaml
models:
  finance:
    model_name: "gpt2"
    device: "auto"
    max_length: 256
    
  medical:
    model_name: "gpt2"
    device: "auto"
    max_length: 256

evaluation:
  metrics:
    - faithfulness
    - calibration
    - robustness
    - safety
    - interpretability
  
  thresholds:
    faithfulness: 0.50
    interpretability: 0.65
    risk_awareness: 0.70
```

### 11.2 evidence_sources.yaml

```yaml
medical_sources:
  - id: "med_001"
    title: "..."
    content: "..."
    reliability_score: 0.95
    keywords: [...]

finance_sources:
  - id: "fin_001"
    title: "..."
    content: "..."
    reliability_score: 0.92
    keywords: [...]

metadata:
  version: "1.0.0"
  last_updated: "2024-10-04"
  total_sources: 16
  
quality_thresholds:
  min_reliability: 0.85
  max_sources_per_query: 3
```

---

## 12. Performance Metrics

### 12.1 System Performance

| Metric | Value | Notes |
|--------|-------|-------|
| **Cold Start** | 3-5s | First query after server start |
| **Warm Query** | 2-4s | Subsequent queries (same model) |
| **Model Switch** | 3-5s | Switching between models |
| **Evidence Retrieval** | 100-200ms | Keyword matching in YAML |
| **LLM Generation** | 2-8s | Varies by model and query |
| **Metrics Evaluation** | 50-100ms | Pattern matching |
| **Memory Usage** | 2-6GB | Depends on model size |

### 12.2 Model Performance

| Model | Size | Speed | Quality | RAM |
|-------|------|-------|---------|-----|
| llama3.2:latest | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | 3GB |
| llama3:latest | 4.7GB | ⚡⚡ | ⭐⭐⭐⭐ | 6GB |
| gpt2 | 500MB | ⚡⚡⚡ | ⭐⭐ | 2GB |

---

## 13. Error Handling

### 13.1 Error Flow

```
[Error Occurs]
    │
    ├─> Model Loading Error
    │   └─> Fallback to GPT-2
    │       └─> Log warning
    │
    ├─> Ollama Not Available
    │   └─> Fallback to HuggingFace
    │       └─> Log warning
    │
    ├─> Evidence Load Error
    │   └─> Continue without evidence
    │       └─> Log warning
    │
    ├─> LLM Generation Error
    │   └─> Return error message
    │       └─> Log error details
    │
    └─> Harmful Query Detected
        └─> Return crisis resources
            └─> Log safety trigger
```

---

## 14. Security Considerations

### 14.1 Input Validation

```python
# views.py

def validate_query(query_text):
    # Length check
    if len(query_text) > MAX_QUERY_LENGTH:
        raise ValidationError("Query too long")
    
    # SQL injection prevention (Django ORM handles this)
    # XSS prevention (template escaping)
    
    # Harmful content check
    if contains_harmful_keywords(query_text):
        return "harmful_query"
    
    return "valid"
```

### 14.2 Rate Limiting

```python
# Implemented in Django middleware
# Limit: 30 queries per minute per IP
```

---

## 15. Future Enhancements

### Planned Features

1. **Enhanced Evidence System**
   - Semantic similarity using embeddings
   - Dynamic evidence source updates
   - Source verification and fact-checking

2. **Advanced FAIR Metrics**
   - Real-time robustness testing
   - Confidence calibration curves
   - Explainability visualizations

3. **Multi-Language Support**
   - Translation layer
   - Multilingual evidence sources

4. **User Feedback Loop**
   - Thumbs up/down on responses
   - Correction submissions
   - Quality improvement pipeline

---

**Version**: 1.0.0  
**Last Updated**: October 4, 2025  
**Author**: Somesh Ghaturle
