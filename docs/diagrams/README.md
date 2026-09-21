# FAIR-Agent Diagrams

Fifteen interactive diagrams generated with [Archify](https://github.com/tt-a1i/archify).
Each `.html` file is a self-contained artifact: inline SVG, no network calls, no build step.
Open one directly in a browser (or `open <file>.html` on macOS).

Every viewer supports pan/zoom, search, relationship tracing, node focus, semantic views,
light/dark themes, and PNG/JPEG/WebP/SVG export.

| Diagram | Type | Replaces |
|---|---|---|
| [System Architecture](system-architecture.html) | architecture | `README.md`, `TECHNICAL_DOCUMENTATION.md` (detailed architecture) |
| [Component Inventory](component-architecture.html) | architecture | `README.md` (system component architecture) |
| [Layer Stack](layered-architecture.html) | architecture | `TECHNICAL_DOCUMENTATION.md` (high-level architecture) |
| [Query Preprocessing](query-preprocessing.html) | workflow | `TECHNICAL_DOCUMENTATION.md` (spell checker) |
| [User Input Processing](user-input-processing.html) | workflow | `README.md` stage 1 |
| [Query Classification and Routing](query-classification-routing.html) | workflow | `README.md` stage 2 |
| [Domain Agent Processing](agent-processing.html) | workflow | `README.md` stage 3 |
| [RAG Evidence Retrieval](rag-evidence-retrieval.html) | workflow | `README.md` stage 4 |
| [RAG Retrieval Pipeline](rag-retrieval-pipeline.html) | dataflow | `TECHNICAL_DOCUMENTATION.md` (RAG system) |
| [LLM Response Generation](llm-generation.html) | workflow | `README.md` stage 5 |
| [Chain-of-Thought Reasoning](chain-of-thought-reasoning.html) | workflow | `TECHNICAL_DOCUMENTATION.md` (reasoning engine, both blocks) |
| [Response Enhancement](response-enhancement.html) | workflow | `README.md` stage 6 |
| [FAIR Evaluation Scoring](fair-evaluation.html) | workflow | `README.md` stage 7 |
| [Response Delivery and Analytics](response-delivery.html) | workflow | `README.md` stage 8 |
| [Memory and Learning Loop](memory-learning-loop.html) | workflow | `MEMORY_AND_LEARNING.md` |

## Editing

The typed JSON specs live in [`src/`](src/). Edit a spec, then re-render:

```bash
ARCHIFY=~/.claude/skills/archify/bin/archify.mjs
cd docs/diagrams/src
node $ARCHIFY validate workflow <name>.workflow.json --quality showcase --json
node $ARCHIFY deliver  workflow <name>.workflow.json ../<name>.html --quality showcase --json
node $ARCHIFY visual-check ../<name>.html --json
```

Use the type that matches the filename suffix (`architecture`, `workflow`, or `dataflow`).
All fifteen specs currently pass `--quality showcase` with 9/9 artifact checks and
zero composition errors, and every artifact is contained at 1440x900, 1600x1000,
1920x1080, and 2048x1320 in both themes.

`visual-check` writes PNG/JSON/HTML evidence sidecars next to the artifact; those are
build evidence, not deliverables, and are not committed.
