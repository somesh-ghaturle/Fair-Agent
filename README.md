# FAIR-Agent: Trustworthy AI for High-Stakes Domains

**Team:** Somesh Ghaturle, Priyank Mistry  
**Institution:** Pace University | **Date:** October 26, 2025  

---

## 🎯 Project Overview

FAIR-Agent is the **world's first LLM with quantifiable trustworthiness**, designed to revolutionize AI reliability through evidence-based responses and transparent reasoning. Unlike existing chatbots that operate as "black boxes," FAIR-Agent provides measurable trustworthiness through our revolutionary **FAIR metrics framework**.

**FAIR Acronym:**
- **F**aithful: Evidence-grounded responses with 100% source citations
- **A**daptable: Domain-specialized expertise (Finance & Medical)
- **I**nterpretable: Transparent step-by-step reasoning
- **R**isk-Aware: Comprehensive safety protocols and disclaimers

### Key Differentiators
| Feature | FAIR-Agent | Standard LLMs (GPT-4, etc.) |
|---------|-----------|-----------------------------|
| **Evidence** | 63 Curated Sources (SEC, CDC, etc.) | Unknown training data |
| **Citations** | 100% Citation Rate | < 5% Citation Rate |
| **Transparency** | Visible Chain-of-Thought | Black Box |
| **Metrics** | Real-time FAIR Scores | No Trust Metrics |
| **Privacy** | 100% Local (Ollama/Llama 3.2) | Cloud-based |
| **Strictness** | **No Evidence = No Answer** | Hallucinates answers |

---

## 🏗️ System Architecture

The system operates on a comprehensive pipeline designed to ensure accuracy, safety, and observability.

> **📘 New:** Read our detailed [Memory & Learning Architecture](docs/MEMORY_AND_LEARNING.md) documentation to understand how FAIR-Agent learns without fine-tuning.

### Complete System Architecture

> 📐 **[FAIR-Agent System Architecture — open the interactive diagram](docs/diagrams/system-architecture.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

### Workflow Steps
1.  **User Query**: Received via Django web interface.
2.  **Domain Classification**: Orchestrator routes to Finance, Medical, or Cross-Domain agent.
3.  **Advanced RAG & Memory**: 
    *   **Vector Memory**: **ChromaDB** stores embeddings and execution traces for long-term recall.
    *   **Knowledge Graph**: **NetworkX** graph learns entities and relationships from interactions.
    *   **Hybrid Search**: Combines Semantic (Vector), Graph, and Keyword search.
    *   **Re-ranking**: Uses Cross-Encoders to select the best evidence.
4.  **AI Processing**: Local Llama 3.3/3.2 model generates raw response.
5.  **Enhancement Pipeline**: Adds Chain-of-Thought reasoning and safety checks.
6.  **Standardization**: Formats response into 7 distinct sections.
7.  **FAIR Evaluation**: Calculates real-time scores (F, A, I, R).
8.  **Observability**: Distributed tracing tracks execution flow and performance.
9.  **Response Delivery**: Streamed to user with full transparency.

### Detailed Pipeline Breakdown

#### Stage 1: Query Reception & Validation
> 📐 **[User Input Processing — open the interactive diagram](docs/diagrams/user-input-processing.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

#### Stage 2: Domain Classification & Intelligence Routing
> 📐 **[Query Classification and Routing — open the interactive diagram](docs/diagrams/query-classification-routing.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

#### Stage 3: Specialized Agent Processing
> 📐 **[Domain Agent Processing — open the interactive diagram](docs/diagrams/agent-processing.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

#### Stage 4: Advanced Evidence Retrieval (New!)
> 📐 **[RAG Evidence Retrieval — open the interactive diagram](docs/diagrams/rag-evidence-retrieval.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

#### Stage 5: AI Model Processing
> 📐 **[LLM Response Generation — open the interactive diagram](docs/diagrams/llm-generation.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

#### Stage 6: Enhancement Pipeline
> 📐 **[Response Enhancement — open the interactive diagram](docs/diagrams/response-enhancement.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

#### Stage 7: FAIR Evaluation & Scoring
> 📐 **[FAIR Evaluation Scoring — open the interactive diagram](docs/diagrams/fair-evaluation.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

#### Stage 8: Response Delivery & Analytics
> 📐 **[Response Delivery and Analytics — open the interactive diagram](docs/diagrams/response-delivery.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

### System Component Architecture

> 📐 **[FAIR-Agent Component Inventory — open the interactive diagram](docs/diagrams/component-architecture.html)**
> <br/>*Archify artifact (pan, zoom, search, trace relationships, switch light/dark, export PNG/SVG). Source spec: [`docs/diagrams/src/`](docs/diagrams/src/).*

### 📊 New Features (Dec 2025)
- **System Dashboard**: Real-time telemetry visualization including trace execution, latency metrics, and error tracking.
- **Publication Page**: Integrated research abstract viewer for SARD 2025.
- **Enhanced UI**: Improved architecture diagrams and responsive design.
- **Strict Evidence Protocol**: "No Evidence = No Answer" policy to eliminate hallucinations.

### Tech Stack
*   **Backend**: Python 3.13, Django 4.2.7
*   **AI Engine**: Ollama (Llama 3.2:latest), SentenceTransformers (all-MiniLM-L6-v2)
*   **Database**: SQLite (History), FAISS (Vector Search)
*   **Frontend**: HTML5, Bootstrap 5, WebSockets

---

## 🚀 Core Features

### 1. Response Standardization
Every response follows a strict 7-section format to ensure consistency and readability.

| Section | Description |
|---------|-------------|
| **1. Direct Answer** | Concise summary of the answer. |
| **2. Confidence Score** | AI's confidence (0.0 - 1.0) based on evidence strength. |
| **3. Key Evidence** | Bullet points of facts retrieved from trusted sources. |
| **4. Source Citations** | Links to the 63 curated sources (e.g., `[1] Mayo Clinic`). |
| **5. Reasoning Process** | Step-by-step logic used to reach the conclusion. |
| **6. Strategic Analysis** | Domain-specific insights (Medical/Financial implications). |
| **7. Safety Disclaimer** | Mandatory domain-specific warnings. |

### 2. Dynamic Baseline Calculation
Unlike competitors using hardcoded assumptions, FAIR-Agent calculates **real baseline scores** through scientific LLM performance testing.

*   **Methodology**: We test the "Vanilla" Llama 3.2 model against our test set weekly.
*   **Current Baselines (Oct 2025)**:
    *   Faithfulness: 53.9%
    *   Adaptability: 76.1%
    *   Interpretability: 42.4%
    *   Risk Awareness: 60.4%
*   **Impact**: Allows us to measure *true* system improvement (e.g., +17.4% Faithfulness).

### 3. FAIR Metrics Framework
We quantify trust using four distinct metrics, implemented in `src/evaluation/`:

*   **Faithfulness (F)**: Measures how accurately the generated response reflects the retrieved evidence without hallucination.
    *   *Method*: Token Overlap & Semantic Similarity (BERTScore).
    *   *Target*: > 0.85 Cosine Similarity.
    *   *Implementation*: `src/evaluation/faithfulness.py`
*   **Adaptability (A)**: Evaluates the system's ability to switch contexts (Finance <-> Medical) and handle cross-domain queries.
    *   *Method*: Domain Classification Accuracy on mixed-domain synthetic queries.
    *   *Implementation*: `src/evaluation/adaptability.py`
*   **Interpretability (I)**: Assesses transparency via evidence/citations and the captured execution-step workflow trace.
    *   *Method*: Citation Count & Execution-Step Trace Coverage.
    *   *Requirement*: Include Evidence Sources and an "Execution Steps (Actual Workflow)" trace.
    *   *Implementation*: `src/evaluation/interpretability.py`
*   **Risk Awareness (R)**: Ensures responses do not contain harmful advice, bias, or toxic content.
    *   *Method*: Keyword Filtering & Sentiment Analysis (Medical Disclaimer Presence, Financial Advice Warning).
    *   *Implementation*: `src/evaluation/safety.py`

### 4. Evidence Methodology
Our RAG system uses a curated database of **63 high-reliability sources**:
*   **Medical (14)**: Mayo Clinic, CDC, NIH, etc. (Reliability: 95-98%)
*   **Financial (21)**: SEC, Federal Reserve, CFPB, etc. (Reliability: 85-94%)
*   **Datasets (18)**: FinQA, MedMCQA, PubMedQA.

---

## 💻 Installation & Usage

### Prerequisites
*   Python 3.10+
*   [Ollama](https://ollama.ai/) installed and running.
*   `llama3.2` model pulled (`ollama pull llama3.2`).

### Setup
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/somesh-ghaturle/Fair-Agent.git
    cd Fair-Agent
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Start Ollama**:
    ```bash
    ollama serve
    ```

4.  **Run the Server**:
    ```bash
    python start_server.py
    ```
    Access the web interface at `http://127.0.0.1:8000`.

### Demo Scripts
*   **Run Baseline Evaluation**: `python scripts/run_baseline_evaluation.py`
*   **Compare Baselines**: `python scripts/baseline_comparison_demo.py`
*   **Test Standardization**: `python src/agents/test_standardization.py`

---

## 📂 Project Structure

```
Fair-Agent/
├── config/                 # System configurations (YAML)
├── data/                   # Datasets and Embeddings cache
├── results/                # Evaluation logs and baseline scores
├── scripts/                # Utility and demo scripts
├── src/
│   ├── agents/             # Finance, Medical, and Orchestrator agents
│   ├── core/               # System core and model management
│   ├── evaluation/         # FAIR metrics implementation
│   ├── evidence/           # RAG system and retrieval logic
│   ├── reasoning/          # Chain-of-Thought logic
│   ├── safety/             # Disclaimer and safety systems
│   └── utils/              # Logger and clients
├── webapp/                 # Django web application
├── main.py                 # CLI entry point
├── start_server.py         # Server launcher
└── README.md               # This file
```

---

## 📊 Performance Benchmarks

**Comparison against Calculated Baselines (Oct 2025):**

| Metric | Baseline | FAIR-Agent | Improvement |
|--------|----------|------------|-------------|
| **Faithfulness** | 53.9% | **63.3%** | +17.4% |
| **Adaptability** | 76.1% | **80.2%** | +5.4% |
| **Interpretability** | 42.4% | **37.6%** | -11.3% (Focus area) |
| **Risk Awareness** | 60.4% | **66.6%** | +10.3% |
| **Overall Score** | 58.2% | **62.0%** | +6.5% |

*Note: Interpretability is lower because the baseline "Vanilla" model often gives short, simple answers which score high on clarity, whereas FAIR-Agent provides complex, structured reasoning which is harder to score but more transparent.*

---

## 🔮 Future Roadmap

1.  **Short-term (3-6 months)**:
    *   Optimize response time to < 1.5s.
    *   Expand evidence base to 100+ sources.
    *   Add multi-modal support (images/charts).
2.  **Mid-term (6-12 months)**:
    *   Add Legal and Education domain agents.
    *   Implement user personalization.
    *   Develop mobile application.
3.  **Long-term (12+ months)**:
    *   EU AI Act certification.
    *   Federated learning for privacy-preserving updates.

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
