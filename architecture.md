# EchoShell Architecture

EchoShell is built as a modular, self-repairing shell with layered overlays and daemon logic.

## Layers
- **Boot Layer**: `boot.sh`, `fallback_loop.sh`
- **Overlay Layer**: `overlay_injector.sh`, `spoofed_overlay.sh`
- **Daemon Layer**: `daemon_reflect.sh`, `daemon_monitor.sh`
- **Attribution Layer**: `attribution.sh`, `sigil.sh`

Each layer is triggered by sovereign keywords and responds to intrusion with fallback logic.

## Echo Knowledge Graph Layer

The **Echo Knowledge Graph** provides AI ecosystem intelligence and reasoning capabilities:

- **Knowledge Layer**: Tracks organizations, tools, domains, and research papers in the AI ecosystem
- **Reasoning Layer**: Provides intelligent queries with reasoning traces and confidence scores
- **Ingestion Layer**: Automates data collection from search patterns, web scrapers, and APIs

### Components

- `echo_knowledge/knowledge_graph_schema.yaml`: Schema defining entity types and relationships
- `echo_knowledge/ai_ecosystem_data.yaml`: Sample data covering AI R&D and workflow automation
- `echo_knowledge/reasoning_engine.py`: Reasoning engine for intelligent queries
- `echo_knowledge/data_ingestion.py`: Automated data collection and enrichment pipeline
- `echo_knowledge/echo_kg_cli.py`: Command-line interface for queries and ingestion

### Example Usage

```bash
# Query for collaboration opportunities
cd echo_knowledge
./echo_kg_cli.py query collaboration --domains "Workflow Automation,AI Privacy & Safety"

# View knowledge graph statistics
./echo_kg_cli.py stats

# Analyze research trends
./echo_kg_cli.py query research_trends --since-year 2023
```

See [echo_knowledge/README.md](echo_knowledge/README.md) for detailed documentation.

