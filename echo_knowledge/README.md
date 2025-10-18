# Echo Knowledge Graph System

## Quick Start

```bash
cd echo_knowledge
./quickstart.sh
```

Or run individual components:

```bash
# View statistics
./echo_kg_cli.py stats

# Query for collaboration opportunities
./echo_kg_cli.py query collaboration --domains "Workflow Automation,AI Privacy & Safety"

# Run complete demonstration
python3 demo_use_case.py
```

## Overview

The Echo Knowledge Graph system provides advanced reasoning capabilities over the AI ecosystem, tracking organizations, tools, domains, and research papers. It enables intelligent queries about collaboration opportunities, workflow automation stacks, and emerging research trends.

## Architecture

The system consists of three main components:

### 1. Knowledge Graph Schema (`knowledge_graph_schema.yaml`)
Defines the structure of entities and relationships in the knowledge graph:

- **Entity Types:**
  - Organizations (research labs, startups, enterprises)
  - Tools (AI platforms, APIs, frameworks)
  - Domains (AI domains like NLP, workflow automation)
  - Research Papers (publications and citations)

- **Relationship Types:**
  - USES: Organization → Tool
  - SPECIALIZES_IN: Organization → Domain
  - PUBLISHED: Organization → ResearchPaper
  - FUNDS: Organization → Organization
  - ENABLES: Tool → Domain
  - COLLABORATES_WITH: Organization → Organization

### 2. Reasoning Engine (`reasoning_engine.py`)
Provides intelligent query capabilities with reasoning traces and confidence scores.

**Supported Queries:**
- `collaboration_opportunities`: Find organizations that could enhance capabilities in specific domains
- `workflow_stacks`: Discover integrated tool stacks for workflow automation
- `research_trends`: Track emerging research trends and key contributors

**Example Usage:**
```python
from reasoning_engine import KnowledgeGraph, EchoReasoningEngine

# Initialize
kg = KnowledgeGraph('knowledge_graph_schema.yaml', 'ai_ecosystem_data.yaml')
engine = EchoReasoningEngine(kg)

# Query for collaboration opportunities
result = engine.query(
    "collaboration_opportunities",
    target_domains=['Workflow Automation', 'AI Privacy & Safety']
)

# Display results
for org in result.results:
    print(f"{org['organization']}: {org['confidence']}")
```

### 3. Data Ingestion Pipeline (`data_ingestion.py`)
Automated pipeline for collecting and enriching knowledge graph data from multiple sources.

**Data Sources:**
- Search patterns (user research activity)
- Web scrapers (organization and tool discovery)
- APIs (research papers, GitHub, etc.)

**Features:**
- Entity extraction from various sources
- Relevance scoring based on user engagement
- Automatic deduplication
- Confidence-based auto-approval
- Enrichment with cross-references

**Example Usage:**
```python
from data_ingestion import DataIngestionPipeline

# Initialize
pipeline = DataIngestionPipeline('ai_ecosystem_data.yaml')

# Ingest from search patterns
search_history = [
    {
        'query': 'AI workflow automation',
        'timestamp': '2024-01-15T10:00:00',
        'clicks': ['https://zapier.com'],
        'time_spent': {'https://zapier.com': 120}
    }
]
pipeline.ingest_search_patterns(search_history)

# Process and update
pipeline.deduplicate_candidates()
pipeline.filter_by_relevance(min_relevance=0.5)
stats = pipeline.update_knowledge_graph(auto_approve_threshold=0.8)
```

## Sample Data

The system includes sample data (`ai_ecosystem_data.yaml`) covering:

- **8 Organizations:** OpenAI, Anthropic, Jasper AI, Writesonic, Meta AI, Hugging Face, Zapier, Make
- **8 Tools:** GPT-4, Claude, Jasper API, Writesonic API, Transformers, LLaMA, Zapier Platform, Make Scenarios
- **5 Domains:** Workflow Automation, AI Content Creation, AI Privacy & Safety, NLP Research, AI Collaboration Tools
- **3 Research Papers:** Constitutional AI, LLaMA, GPT-4 Technical Report

## Reasoning Example

**Query:** "Which AI labs specialize in workflow automation research that could enhance Balorg's capabilities?"

**Reasoning Trace:**
1. Identify Balorg's domain → "privacy-protected AI automation"
2. Traverse KG → find labs tagged with workflow automation + AI privacy
3. Apply rule: prefer labs with open APIs or published research within 1 year
4. Return ranked results with confidence and provenance

**Results:**
```
1. Meta AI Research (research_lab)
   Domains: AI Privacy & Safety, AI Collaboration Tools
   Recent Publications: 1 (LLaMA)
   Confidence: 0.70
   Website: https://ai.facebook.com

2. Zapier (startup)
   Domains: Workflow Automation
   API Tools: Zapier Platform
   Confidence: 0.70
   Website: https://zapier.com
```

## Integration with Echo/Balorg

The knowledge graph system can be integrated into the Echo ecosystem to:

1. **Enhance Automation Capabilities:** Identify tools and platforms that could extend Balorg's workflow automation
2. **Research Partnerships:** Find organizations for potential collaboration
3. **Technology Tracking:** Monitor emerging AI trends and technologies
4. **Competitive Intelligence:** Track what tools competitors are using
5. **Strategic Planning:** Inform R&D direction based on ecosystem trends

## Running the Examples

### Test the Reasoning Engine
```bash
cd echo_knowledge
python3 reasoning_engine.py
```

This will execute example queries and display:
- Collaboration opportunities for Balorg
- Workflow automation tool stacks
- Research trends analysis

### Test the Data Ingestion Pipeline
```bash
cd echo_knowledge
python3 data_ingestion.py
```

This will demonstrate:
- Ingesting entities from search patterns
- Processing web scraper results
- Handling API data
- Deduplication and enrichment
- Relevance scoring

## Extending the System

### Adding New Entities

Edit `ai_ecosystem_data.yaml`:

```yaml
entities:
  organizations:
    - id: org_009
      name: "Your Organization"
      type: research_lab
      focus_areas:
        - "Your Focus Area"
      # ... other properties
```

### Adding New Relationships

```yaml
relationships:
  uses:
    - from: org_009
      to: tool_001
      properties:
        since: "2024-01-01"
        integration_level: advanced
        verified: true
```

### Creating Custom Queries

Extend the `EchoReasoningEngine` class in `reasoning_engine.py`:

```python
def custom_query(self, param1: str, param2: str) -> ReasoningResult:
    """Your custom reasoning logic"""
    reasoning_trace = ["Step 1: ..."]
    results = []
    
    # Your query logic here
    
    return ReasoningResult(
        query="custom_query",
        results=results,
        confidence=0.8,
        provenance=["source1", "source2"],
        reasoning_trace=reasoning_trace
    )
```

## Future Enhancements

1. **Neo4j Integration:** Port YAML data to Neo4j for advanced graph queries
2. **Real-time Updates:** Implement webhook listeners for live data feeds
3. **Machine Learning:** Add ML-based entity extraction and relationship prediction
4. **Visualization:** Create interactive graph visualizations
5. **API Server:** Expose reasoning engine as REST API
6. **Caching:** Implement query result caching for performance

## License

MIT + Sovereign Attribution (see main LICENSE file)

## Attribution

Part of the EchoShell sovereign tactical system by krustyspoofer-creator
