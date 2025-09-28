# FAIR-Agent System

**CS668 Analytics Capstone - Fall 2025**  
**Author:** Somesh Ghaturle

A comprehensive AI system featuring specialized Finance and Medical agents with domain classification, cross-domain reasoning, and FAIR (Faithfulness, Adaptability, Interpretability, Risk-awareness) metrics evaluation.

## 🎯 Project Overview

The FAIR-Agent system is designed to provide trustworthy, domain-specific AI assistance in finance and healthcare domains. It features:

- **Multi-Agent Architecture**: Specialized Finance and Medical agents
- **Intelligent Routing**: Automated domain classification for query routing
- **Cross-Domain Reasoning**: Ability to handle queries spanning multiple domains
- **FAIR Metrics**: Comprehensive evaluation of faithfulness, interpretability, and risk-awareness
- **Web Interface**: User-friendly Django-based web application
- **CLI Mode**: Interactive command-line interface for testing

## 🏗 System Architecture

```
FAIR-Agent System
├── Core System
│   ├── Orchestrator (Query routing & coordination)
│   ├── Finance Agent (GPT-2 based)
│   └── Medical Agent (GPT-2 based)
├── Web Interface (Django)
├── FAIR Evaluation Metrics
└── Domain Classification Engine
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Virtual environment (recommended)
- 8GB+ RAM for model loading
- **OR** Docker & Docker Compose (for containerized deployment)

### Option 1: Docker Deployment (Recommended)

The fastest way to get started:

```bash
# Clone the repository
git clone <repository-url>
cd Fair-Agent

# Deploy with Docker
./docker-deploy.sh start

# Access the web interface
open http://localhost:8000
```

See [DOCKER_README.md](DOCKER_README.md) for detailed Docker deployment instructions.

### Option 2: Local Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd Fair-Agent
```

2. **Set up virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the system**
```bash
# Web interface (recommended)
python main.py --mode web

# CLI interface
python main.py --mode cli

# With custom port and debug mode
python main.py --mode web --port 8080 --debug
```

### Alternative Django Method

```bash
cd webapp
python manage.py runserver
```

## 🎮 Usage Examples

### Web Interface
1. Open your browser to `http://127.0.0.1:8000`
2. Navigate to the Query page
3. Enter your question (finance, medical, or general)
4. View comprehensive analysis with FAIR metrics

### CLI Interface
```bash
python main.py --mode cli

> what is diabetes treatment
Domain: medical
Confidence: 0.92
Answer: [Medical Agent provides detailed diabetes treatment information]

> explain stock market analysis
Domain: finance  
Confidence: 0.88
Answer: [Finance Agent provides market analysis insights]
```

### Example Queries

**Medical Domain:**
- "What are the treatment options for diabetes?"
- "Explain the side effects of hypertension medication"
- "How does cholesterol affect heart health?"

**Finance Domain:**
- "Analyze the risk of investing in tech stocks"
- "What factors affect mortgage interest rates?"
- "Explain portfolio diversification strategies"

**Cross-Domain:**
- "What are the financial implications of healthcare costs?"
- "How do pharmaceutical investments perform?"

## 📊 FAIR Metrics

The system evaluates responses across multiple dimensions with realistic GPT-2 based scoring:

- **Faithfulness** (25-60%): Accuracy and consistency with source information
- **Interpretability** (40-60%): Clarity and explainability of responses with enhanced reasoning
- **Risk-Awareness** (56-76%): Safety and risk assessment capabilities with domain-specific disclaimers
- **Calibration Error** (30-70%): Confidence calibration accuracy
- **Robustness** (20-25%): Performance under various conditions, reflecting base model limitations

*Note: Scores reflect realistic GPT-2 model capabilities after system recalibration.*

## 🔧 Configuration

### System Configuration (`config/system_config.yaml`)

```yaml
finance_agent:
  model_name: "gpt2"
  device: "auto"
  max_length: 256

medical_agent:
  model_name: "gpt2"  
  device: "auto"
  max_length: 256

system:
  enable_cross_domain: true
  web_port: 8000
  debug_mode: false
```

### Environment Variables

```bash
# Optional: Set custom configuration
export FAIR_AGENT_CONFIG="config/custom_config.yaml"

# Optional: Enable debug logging
export FAIR_AGENT_DEBUG="true"
```

## 📁 Project Structure

```
Fair-Agent/
├── main.py                 # Main entry point
├── requirements.txt        # Dependencies
├── README.md              # This file
├── config/                # Configuration files
│   └── system_config.yaml
├── src/                   # Core system code
│   ├── core/             # System initialization & coordination
│   │   ├── system.py     # Main system class
│   │   └── config.py     # Configuration management
│   ├── agents/           # AI agents
│   │   ├── orchestrator.py
│   │   ├── finance_agent.py
│   │   └── medical_agent.py
│   ├── evaluation/       # FAIR metrics evaluation
│   │   ├── faithfulness.py
│   │   ├── interpretability.py
│   │   ├── calibration.py
│   │   ├── robustness.py
│   │   └── safety.py
│   └── utils/            # Utilities
│       └── logger.py
├── webapp/               # Django web interface
│   ├── manage.py
│   ├── settings.py
│   ├── urls.py
│   ├── fair_agent_app/
│   │   ├── views.py
│   │   ├── models.py
│   │   ├── services.py
│   │   └── urls.py
│   └── templates/
│       ├── base.html
│       ├── home.html
│       └── query.html
└── scripts/              # Utility scripts
    ├── evaluate.py
    └── run_pipeline.py
```

## 🧪 Testing

### Manual Testing
1. Start the system: `python main.py --mode web`
2. Test various query types through the web interface
3. Verify domain classification accuracy
4. Check FAIR metrics scores

### CLI Testing
```bash
python main.py --mode cli
> status  # Check system status
> help    # Show available commands
> config  # Show configuration
```

## 🔍 Domain Classification

The system automatically classifies queries into:

- **Medical**: Health, disease, treatment, symptoms, medication
- **Finance**: Investment, market, portfolio, economics, financial analysis  
- **Cross-Domain**: Queries spanning both domains
- **General**: Topics outside core domains

### Classification Features
- Keyword-based matching with adaptive thresholds
- Pattern recognition for domain-specific terms
- Fallback handling for ambiguous queries
- Special handling for single strong domain terms

## 🛠 Development

### Adding New Features
1. Extend agents in `src/agents/`
2. Add evaluation metrics in `src/evaluation/`
3. Update web interface in `webapp/`
4. Modify configuration in `config/`

### Code Quality
- Follow PEP 8 style guidelines
- Add comprehensive docstrings
- Include type hints where appropriate
- Test new features thoroughly

## 📝 System Logs

The system provides comprehensive logging:
- Agent initialization and model loading
- Query processing and domain classification  
- FAIR metrics evaluation
- Error handling and debugging

Logs are displayed in console and optionally saved to files.

## ⚠ Important Notes

### Model Compatibility
- Currently uses GPT-2 for maximum compatibility
- Supports MPS (Apple Silicon), CUDA (NVIDIA), and CPU
- Models are loaded on-demand for memory efficiency

### Safety Considerations
- Medical responses include safety disclaimers
- Financial advice includes risk warnings
- Input sanitization for security
- Rate limiting for web interface

### Performance
- Initial model loading may take 1-2 minutes
- Subsequent queries are processed quickly
- Memory usage: ~4-6GB with both agents loaded

## 🤝 Contributing

This is an academic project for CS668 Analytics Capstone. For improvements or suggestions:

1. Review the current implementation
2. Propose changes through detailed documentation
3. Ensure compatibility with existing features
4. Test thoroughly before submission

## 📞 Support

For questions or issues related to this capstone project, please refer to:
- Course materials and documentation
- System logs for debugging information
- Configuration files for customization options

---

## 🏆 Academic Project Information

**Course**: CS668 Analytics Capstone - Fall 2025  
**Institution**: Pace University  
**Team Members**: 
- Somesh Ramesh Ghaturle
- Darshil Malaviya  
- Priyank Mistry

![FAIR-Agent Logo](https://img.shields.io/badge/FAIR-Agent-blue.svg) ![Python](https://img.shields.io/badge/python-3.9+-blue.svg) ![License](https://img.shields.io/badge/license-MIT-green.svg)



## 📄 License

MIT License - Copyright (c) 2025 FAIR-Agent Team

## ⚠️ Disclaimer

FAIR-Agent is a research project designed for educational and research purposes. It should not be used as a substitute for professional medical advice, diagnosis, or treatment, nor for professional financial advice. Always consult qualified professionals for important decisions in these domains.

---

© 2025 FAIR-Agent Team - CS668 Analytics Capstone Project
