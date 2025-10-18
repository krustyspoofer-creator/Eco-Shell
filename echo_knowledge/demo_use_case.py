#!/usr/bin/env python3
"""
Echo Knowledge Graph - Use Case Example

This script demonstrates the complete use case from the problem statement:
1. Building a sample knowledge graph segment based on AI R&D and workflow automation
2. Demonstrating the reasoning capabilities with the example query:
   "Which AI labs specialize in workflow automation research that could enhance Balorg's capabilities?"
3. Showing the data ingestion pipeline in action

This addresses both Option 1 (concrete graph example) and Option 2 (automation pipeline blueprint)
from the problem statement.
"""

import sys
import os
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reasoning_engine import KnowledgeGraph, EchoReasoningEngine
from data_ingestion import DataIngestionPipeline


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80 + "\n")


def demo_knowledge_graph_structure():
    """Demonstrate the knowledge graph structure (Option 1)"""
    print_section("PHASE 1: Knowledge Graph Structure")
    
    print("The Echo Knowledge Graph consists of:")
    print("\n1. ENTITY TYPES:")
    print("   - Organizations: R&D hubs, AI labs, startups (8 in sample data)")
    print("   - Tools/Platforms: Jasper, Writesonic, Meta AI tools, etc. (8 in sample)")
    print("   - Domains: Workflow automation, AI creativity, NLP frameworks (5 in sample)")
    print("   - Research Papers: Publications and citations (3 in sample)")
    
    print("\n2. RELATIONSHIP TYPES:")
    print("   - USES: Which orgs use which tools")
    print("   - SPECIALIZES_IN: Org expertise in domains")
    print("   - PUBLISHED: Who published what research")
    print("   - FUNDS: Funding relationships")
    print("   - ENABLES: How tools enable domains")
    print("   - COLLABORATES_WITH: Research partnerships")
    
    print("\n3. SAMPLE KNOWLEDGE GRAPH SEGMENT (Neo4j/YAML format):")
    print("""
    (Meta AI Research:Organization)
        -[:SPECIALIZES_IN {expertise_level: 'expert', years_active: 6}]->
            (AI Privacy & Safety:Domain)
        -[:PUBLISHED {contribution_type: 'primary'}]->
            (LLaMA Paper:ResearchPaper {citations: 1200})
        -[:COLLABORATES_WITH {project_name: 'Open LLM Distribution', active: true}]->
            (Hugging Face:Organization)
    
    (Zapier:Organization)
        -[:SPECIALIZES_IN {expertise_level: 'leader', years_active: 12}]->
            (Workflow Automation:Domain)
        -[:USES {integration_level: 'custom'}]->
            (Zapier Platform:Tool {api_available: true})
    
    (GPT-4:Tool {api_available: true})
        -[:ENABLES {effectiveness: 0.95}]->
            (AI Content Creation:Domain)
    """)
    
    # Load actual knowledge graph
    base_path = Path(__file__).parent
    schema_path = base_path / 'knowledge_graph_schema.yaml'
    data_path = base_path / 'ai_ecosystem_data.yaml'
    
    kg = KnowledgeGraph(str(schema_path), str(data_path))
    
    print("\n4. CURRENT KNOWLEDGE GRAPH STATISTICS:")
    from reasoning_engine import EntityType
    for entity_type in EntityType:
        entities = kg.find_entities_by_type(entity_type)
        print(f"   - {entity_type.value}s: {len(entities)}")
    
    print(f"   - Total Relationships: {len(kg.relationships)}")
    
    return kg


def demo_reasoning_example(kg):
    """Demonstrate the reasoning example from the problem statement (Phase 2)"""
    print_section("PHASE 2: Reasoning Example - AI Collaboration Insight")
    
    print("QUERY:")
    print('"Which AI labs specialize in workflow automation research')
    print(' that could enhance Balorg\'s capabilities?"')
    
    print("\nBALORG CONTEXT:")
    print("  Domain: Privacy-protected AI automation")
    print("  Needs: Workflow automation + AI privacy capabilities")
    
    engine = EchoReasoningEngine(kg)
    
    # Execute the reasoning query
    result = engine.find_collaboration_opportunities(
        target_domains=['Workflow Automation', 'AI Privacy & Safety'],
        focus='workflow_automation'
    )
    
    print("\nREASONING TRACE:")
    for i, trace in enumerate(result.reasoning_trace, 1):
        print(f"  {i}. {trace}")
    
    print(f"\nOVERALL CONFIDENCE: {result.confidence:.2f}")
    
    print("\nTOP COLLABORATION OPPORTUNITIES:")
    print("-" * 80)
    
    for i, org in enumerate(result.results[:5], 1):
        print(f"\n{i}. {org['organization']} ({org['type']})")
        print(f"   Confidence Score: {org['confidence']:.2f}")
        print(f"   Relevant Domains: {', '.join(org['relevant_domains'])}")
        
        if org['api_tools']:
            print(f"   ✓ Has API Tools: {', '.join(org['api_tools'])}")
        
        if org['recent_publications']:
            print(f"   ✓ Recent Publications: {len(org['recent_publications'])}")
            for pub in org['recent_publications'][:2]:
                print(f"      - {pub}")
        
        print(f"   Website: {org['website']}")
        print(f"   Location: {org['location']}")
        
        # Why this is relevant for Balorg
        relevance_reasons = []
        if 'AI Privacy & Safety' in org['relevant_domains']:
            relevance_reasons.append("Privacy-preserving AI expertise")
        if 'Workflow Automation' in org['relevant_domains']:
            relevance_reasons.append("Workflow automation capabilities")
        if org['api_tools']:
            relevance_reasons.append("API integration ready")
        if org['recent_publications']:
            relevance_reasons.append("Active research output")
        
        if relevance_reasons:
            print(f"   → Relevance to Balorg: {', '.join(relevance_reasons)}")


def demo_data_ingestion_pipeline():
    """Demonstrate the data ingestion pipeline (Phase 3 / Option 2)"""
    print_section("PHASE 3: Data Ingestion & Enrichment Pipeline")
    
    print("The pipeline automates knowledge graph updates from:")
    print("  1. User search patterns (relevance scoring)")
    print("  2. Web scrapers (entity discovery)")
    print("  3. External APIs (research papers, GitHub, etc.)")
    
    base_path = Path(__file__).parent
    data_path = base_path / 'ai_ecosystem_data.yaml'
    
    pipeline = DataIngestionPipeline(str(data_path))
    
    print("\n" + "-" * 80)
    print("EXAMPLE 1: Search Pattern Analysis")
    print("-" * 80)
    
    # Simulate user's search activity from the problem statement
    search_history = [
        {
            'query': 'AI workflow automation platforms',
            'timestamp': '2024-10-15T10:00:00',
            'clicks': [
                'https://zapier.com/features',
                'https://make.com/automation'
            ],
            'time_spent': {
                'https://zapier.com/features': 180,  # High engagement
                'https://make.com/automation': 120
            }
        },
        {
            'query': 'AI research and development hubs expand balorg echo',
            'timestamp': '2024-10-16T14:30:00',
            'clicks': [
                'https://openai.com/research',
                'https://ai.facebook.com'
            ],
            'time_spent': {
                'https://openai.com/research': 150,
                'https://ai.facebook.com': 200  # Very high engagement
            }
        },
        {
            'query': 'AI content creation blogging tools jasper writesonic',
            'timestamp': '2024-10-17T09:15:00',
            'clicks': [
                'https://jasper.ai',
                'https://writesonic.com'
            ],
            'time_spent': {
                'https://jasper.ai': 240,  # Very high engagement
                'https://writesonic.com': 90
            }
        },
        {
            'query': 'Meta Facebook AI talent collaboration opportunities',
            'timestamp': '2024-10-18T11:00:00',
            'clicks': [
                'https://ai.facebook.com/careers',
                'https://ai.facebook.com/research'
            ],
            'time_spent': {
                'https://ai.facebook.com/careers': 160,
                'https://ai.facebook.com/research': 95
            }
        }
    ]
    
    print("\nProcessing search history...")
    print(f"  Total searches: {len(search_history)}")
    print(f"  Date range: 2024-10-15 to 2024-10-18")
    
    candidates = pipeline.ingest_search_patterns(search_history)
    print(f"  ✓ Extracted {len(candidates)} entity candidates")
    
    print("\n" + "-" * 80)
    print("EXAMPLE 2: Web Scraper Results")
    print("-" * 80)
    
    scraper_results = [
        {
            'type': 'organization',
            'name': 'Anthropic',
            'description': 'AI safety and research company',
            'focus_areas': ['Constitutional AI', 'AI Safety', 'Large Language Models'],
            'source_url': 'https://anthropic.com/about',
            'scraped_at': '2024-10-18T06:00:00',
            'location': 'San Francisco, CA'
        }
    ]
    
    print("\nProcessing web scraper results...")
    candidates2 = pipeline.ingest_web_scraper_results(scraper_results)
    print(f"  ✓ Extracted {len(candidates2)} entity candidates")
    
    print("\n" + "-" * 80)
    print("EXAMPLE 3: External API Data")
    print("-" * 80)
    
    api_results = [
        {
            'type': 'research_paper',
            'title': 'Privacy-Preserving Workflow Automation with Federated Learning',
            'authors': ['Dr. Jane Smith', 'Prof. John Doe'],
            'published_date': '2024-09-15',
            'topics': ['Workflow Automation', 'Privacy', 'Federated Learning'],
            'citations': 12,
            'api_source': 'arxiv'
        }
    ]
    
    print("\nProcessing API data...")
    candidates3 = pipeline.ingest_api_data(api_results)
    print(f"  ✓ Extracted {len(candidates3)} entity candidates")
    
    # Process and enrich
    print("\n" + "-" * 80)
    print("PIPELINE PROCESSING")
    print("-" * 80)
    
    print("\n1. Enriching entities...")
    for candidate in pipeline.entity_candidates:
        pipeline.enrich_entity(candidate)
    print(f"   ✓ Enriched {len(pipeline.entity_candidates)} candidates")
    
    print("\n2. Deduplicating entities...")
    before_dedup = len(pipeline.entity_candidates)
    pipeline.deduplicate_candidates()
    after_dedup = len(pipeline.entity_candidates)
    print(f"   ✓ Removed {before_dedup - after_dedup} duplicates")
    
    print("\n3. Filtering by relevance (threshold: 0.4)...")
    before_filter = len(pipeline.entity_candidates)
    pipeline.filter_by_relevance(min_relevance=0.4)
    after_filter = len(pipeline.entity_candidates)
    print(f"   ✓ Filtered out {before_filter - after_filter} low-relevance candidates")
    
    # Display top candidates
    print("\n" + "-" * 80)
    print("TOP CANDIDATES FOR INGESTION")
    print("-" * 80)
    
    sorted_candidates = sorted(
        pipeline.entity_candidates,
        key=lambda c: c.relevance_score,
        reverse=True
    )
    
    for i, candidate in enumerate(sorted_candidates[:8], 1):
        print(f"\n{i}. {candidate.name} ({candidate.entity_type})")
        print(f"   Relevance Score: {candidate.relevance_score:.2f}")
        print(f"   Sources: {', '.join(set(s.source_type for s in candidate.sources))}")
        
        # Show why it's relevant
        if hasattr(candidate, 'properties'):
            if 'user_engagement' in candidate.properties:
                print(f"   User Engagement: {candidate.properties['user_engagement']}s")
            if 'discovered_from' in candidate.properties:
                print(f"   Discovered From: {candidate.properties['discovered_from']}")
    
    print("\n" + "-" * 80)
    print("AUTOMATED UPDATE DECISION")
    print("-" * 80)
    
    print("\nApplying auto-approval rules:")
    print("  - Threshold for auto-approval: 0.8")
    print("  - Manual review required for: < 0.8")
    
    auto_approve = [c for c in pipeline.entity_candidates if c.relevance_score >= 0.8]
    manual_review = [c for c in pipeline.entity_candidates if c.relevance_score < 0.8]
    
    print(f"\n  ✓ Would auto-approve: {len(auto_approve)} entities")
    print(f"  ℹ Require manual review: {len(manual_review)} entities")
    
    print("\nNote: This is a dry-run. Use --update flag to apply changes.")


def demo_integration_blueprint():
    """Show how this integrates with Echo/Balorg ecosystem"""
    print_section("INTEGRATION WITH ECHO/BALORG ECOSYSTEM")
    
    print("The Echo Knowledge Graph enhances Balorg capabilities through:")
    
    print("\n1. STRATEGIC INTELLIGENCE")
    print("   - Identify tools that could extend Balorg's automation")
    print("   - Find research partners for privacy-preserving AI")
    print("   - Track competitor technologies and approaches")
    
    print("\n2. TECHNOLOGY DISCOVERY")
    print("   - Monitor emerging workflow automation tools")
    print("   - Discover APIs ready for integration")
    print("   - Track open-source alternatives")
    
    print("\n3. RESEARCH COLLABORATION")
    print("   - Find labs with compatible research focus")
    print("   - Identify potential funding opportunities")
    print("   - Track key researchers in target domains")
    
    print("\n4. COMPETITIVE ANALYSIS")
    print("   - See which tools organizations are adopting")
    print("   - Monitor research trends and citations")
    print("   - Identify capability gaps")
    
    print("\n5. CONTINUOUS LEARNING")
    print("   - Auto-update from user search patterns")
    print("   - Ingest new research papers automatically")
    print("   - Track ecosystem changes in real-time")
    
    print("\nEXAMPLE INTEGRATION WORKFLOW:")
    print("""
    User Research Activity (Search Patterns)
              ↓
    Data Ingestion Pipeline
              ↓
    Entity Extraction & Enrichment
              ↓
    Relevance Scoring (based on engagement)
              ↓
    Knowledge Graph Update
              ↓
    Reasoning Engine Queries
              ↓
    Actionable Insights for Balorg
              ↓
    Strategic Decisions (partnerships, integrations, R&D focus)
    """)


def main():
    """Run the complete use case demonstration"""
    print("=" * 80)
    print(" " * 20 + "ECHO KNOWLEDGE GRAPH")
    print(" " * 15 + "Complete Use Case Demonstration")
    print("=" * 80)
    
    print("\nThis demonstration addresses the problem statement by providing:")
    print("  ✓ Option 1: Concrete knowledge graph example (PHASE 1)")
    print("  ✓ Option 2: Data ingestion & enrichment pipeline (PHASE 3)")
    print("  ✓ Reasoning capabilities (PHASE 2)")
    
    # Phase 1: Show the knowledge graph structure
    kg = demo_knowledge_graph_structure()
    
    input("\nPress Enter to continue to PHASE 2 (Reasoning Example)...")
    
    # Phase 2: Demonstrate reasoning
    demo_reasoning_example(kg)
    
    input("\nPress Enter to continue to PHASE 3 (Data Ingestion Pipeline)...")
    
    # Phase 3: Demonstrate data ingestion
    demo_data_ingestion_pipeline()
    
    input("\nPress Enter to see integration blueprint...")
    
    # Integration blueprint
    demo_integration_blueprint()
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    
    print("\nNext Steps:")
    print("  1. Review the sample data in ai_ecosystem_data.yaml")
    print("  2. Try the CLI: ./echo_kg_cli.py query collaboration")
    print("  3. Add your own entities and relationships")
    print("  4. Integrate with external APIs for live data")
    print("  5. Build Neo4j integration for advanced graph queries")
    
    print("\nFor detailed documentation, see: echo_knowledge/README.md")


if __name__ == "__main__":
    main()
