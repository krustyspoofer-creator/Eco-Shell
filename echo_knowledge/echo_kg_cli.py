#!/usr/bin/env python3
"""
Echo Knowledge Graph CLI

Interactive command-line interface for querying the Echo knowledge graph
and running data ingestion pipelines.

Usage:
    ./echo_kg_cli.py query <query_type> [options]
    ./echo_kg_cli.py ingest <source_type> <data_file>
    ./echo_kg_cli.py stats
"""

import sys
import os
import json
import argparse
from pathlib import Path

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from reasoning_engine import KnowledgeGraph, EchoReasoningEngine
from data_ingestion import DataIngestionPipeline


def setup_paths():
    """Setup paths for data files"""
    base_path = Path(__file__).parent
    return {
        'schema': base_path / 'knowledge_graph_schema.yaml',
        'data': base_path / 'ai_ecosystem_data.yaml'
    }


def cmd_query(args):
    """Execute a knowledge graph query"""
    paths = setup_paths()
    
    # Initialize knowledge graph and engine
    print("Loading knowledge graph...")
    kg = KnowledgeGraph(str(paths['schema']), str(paths['data']))
    engine = EchoReasoningEngine(kg)
    
    print(f"Executing query: {args.query_type}\n")
    
    # Execute query based on type
    if args.query_type == 'collaboration':
        domains = args.domains.split(',') if args.domains else ['Workflow Automation', 'AI Privacy & Safety']
        result = engine.query(
            "collaboration_opportunities",
            target_domains=domains,
            focus=args.focus or 'workflow_automation'
        )
        display_collaboration_results(result)
    
    elif args.query_type == 'workflow_stacks':
        result = engine.query("workflow_stacks")
        display_workflow_stacks(result)
    
    elif args.query_type == 'research_trends':
        since_year = args.since_year or 2023
        result = engine.query("research_trends", since_year=since_year)
        display_research_trends(result)
    
    else:
        print(f"Unknown query type: {args.query_type}")
        print("Available query types: collaboration, workflow_stacks, research_trends")
        return 1
    
    return 0


def cmd_ingest(args):
    """Run data ingestion pipeline"""
    paths = setup_paths()
    
    print("Initializing data ingestion pipeline...")
    pipeline = DataIngestionPipeline(str(paths['data']))
    
    # Load data from file
    print(f"Loading data from: {args.data_file}")
    with open(args.data_file, 'r') as f:
        data = json.load(f)
    
    # Ingest based on source type
    if args.source_type == 'search':
        candidates = pipeline.ingest_search_patterns(data)
    elif args.source_type == 'scraper':
        candidates = pipeline.ingest_web_scraper_results(data)
    elif args.source_type == 'api':
        candidates = pipeline.ingest_api_data(data)
    else:
        print(f"Unknown source type: {args.source_type}")
        print("Available source types: search, scraper, api")
        return 1
    
    print(f"\nExtracted {len(candidates)} candidates")
    
    # Process candidates
    print("Processing candidates...")
    for candidate in pipeline.entity_candidates:
        pipeline.enrich_entity(candidate)
    
    pipeline.deduplicate_candidates()
    print(f"After deduplication: {len(pipeline.entity_candidates)} candidates")
    
    pipeline.filter_by_relevance(min_relevance=args.min_relevance)
    print(f"After filtering (min_relevance={args.min_relevance}): {len(pipeline.entity_candidates)} candidates")
    
    # Display report
    print("\n" + pipeline.generate_ingestion_report())
    
    # Update knowledge graph if requested
    if args.update:
        print(f"\nUpdating knowledge graph (auto-approve threshold: {args.auto_approve})...")
        stats = pipeline.update_knowledge_graph(auto_approve_threshold=args.auto_approve)
        print(f"Auto-approved: {stats['auto_approved']}")
        print(f"Manual review required: {stats['manual_review']}")
        print(f"Knowledge graph updated successfully!")
    else:
        print("\nNote: Use --update flag to apply changes to the knowledge graph")
    
    return 0


def cmd_stats(args):
    """Display knowledge graph statistics"""
    paths = setup_paths()
    
    print("Loading knowledge graph...")
    kg = KnowledgeGraph(str(paths['schema']), str(paths['data']))
    
    print("\n" + "=" * 80)
    print("Echo Knowledge Graph Statistics")
    print("=" * 80)
    print()
    
    # Count entities by type
    from reasoning_engine import EntityType
    
    print("Entities:")
    for entity_type in EntityType:
        entities = kg.find_entities_by_type(entity_type)
        print(f"  {entity_type.value}s: {len(entities)}")
    
    print()
    
    # Count relationships by type
    rel_types = {}
    for rel in kg.relationships:
        rel_types[rel.type] = rel_types.get(rel.type, 0) + 1
    
    print("Relationships:")
    for rel_type, count in sorted(rel_types.items()):
        print(f"  {rel_type}: {count}")
    
    print()
    
    # Find most connected entities
    connections = {}
    for rel in kg.relationships:
        connections[rel.from_entity] = connections.get(rel.from_entity, 0) + 1
        connections[rel.to_entity] = connections.get(rel.to_entity, 0) + 1
    
    print("Most Connected Entities:")
    sorted_connections = sorted(connections.items(), key=lambda x: x[1], reverse=True)[:5]
    for entity_id, count in sorted_connections:
        entity = kg.find_entity(entity_id)
        if entity:
            name = entity.properties.get('name', entity_id)
            print(f"  {name}: {count} connections")
    
    print()
    print("=" * 80)
    
    return 0


def display_collaboration_results(result):
    """Display collaboration query results"""
    print("=" * 80)
    print("Collaboration Opportunities")
    print("=" * 80)
    print()
    
    print("Reasoning Trace:")
    for i, trace in enumerate(result.reasoning_trace, 1):
        print(f"  {i}. {trace}")
    
    print(f"\nOverall Confidence: {result.confidence:.2f}")
    print(f"\nResults ({len(result.results)} organizations):")
    print()
    
    for i, org in enumerate(result.results[:10], 1):
        print(f"{i}. {org['organization']} ({org['type']})")
        print(f"   Confidence: {org['confidence']:.2f}")
        print(f"   Domains: {', '.join(org['relevant_domains'])}")
        if org['api_tools']:
            print(f"   API Tools: {', '.join(org['api_tools'])}")
        if org['recent_publications']:
            print(f"   Recent Publications: {len(org['recent_publications'])}")
        print(f"   Website: {org['website']}")
        print()


def display_workflow_stacks(result):
    """Display workflow stack results"""
    print("=" * 80)
    print("Workflow Automation Tool Stacks")
    print("=" * 80)
    print()
    
    print("Reasoning Trace:")
    for i, trace in enumerate(result.reasoning_trace, 1):
        print(f"  {i}. {trace}")
    
    print(f"\nResults ({len(result.results)} organizations):")
    print()
    
    for i, org in enumerate(result.results, 1):
        print(f"{i}. {org['organization']}")
        print(f"   Expertise: {org['expertise_level']} ({org['years_active']} years)")
        print(f"   Tools in stack:")
        for tool in org['automation_stack']:
            api_status = "✓" if tool['api_available'] else "✗"
            print(f"     - {tool['name']} ({tool['category']}) [API: {api_status}]")
        print()


def display_research_trends(result):
    """Display research trends results"""
    print("=" * 80)
    print("Research Trends Analysis")
    print("=" * 80)
    print()
    
    print("Reasoning Trace:")
    for i, trace in enumerate(result.reasoning_trace, 1):
        print(f"  {i}. {trace}")
    
    trends = result.results[0]
    
    print("\nTrending Topics:")
    for i, topic in enumerate(trends['trending_topics'][:10], 1):
        print(f"  {i}. {topic['topic']}: {topic['frequency']} papers")
    
    print("\nTop Contributors:")
    for i, contrib in enumerate(trends['top_contributors'][:5], 1):
        print(f"\n  {i}. {contrib['organization']}")
        print(f"     Papers: {contrib['paper_count']}")
        print(f"     Total Citations: {contrib['total_citations']}")
        print(f"     Recent Work:")
        for paper in contrib['papers'][:3]:
            print(f"       - {paper['title']} ({paper['citations']} citations)")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Echo Knowledge Graph CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Execute a knowledge graph query')
    query_parser.add_argument(
        'query_type',
        choices=['collaboration', 'workflow_stacks', 'research_trends'],
        help='Type of query to execute'
    )
    query_parser.add_argument('--domains', help='Comma-separated list of target domains')
    query_parser.add_argument('--focus', help='Focus area for collaboration query')
    query_parser.add_argument('--since-year', type=int, help='Year for research trends query')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Run data ingestion pipeline')
    ingest_parser.add_argument(
        'source_type',
        choices=['search', 'scraper', 'api'],
        help='Type of data source'
    )
    ingest_parser.add_argument('data_file', help='Path to JSON data file')
    ingest_parser.add_argument(
        '--min-relevance',
        type=float,
        default=0.5,
        help='Minimum relevance score (default: 0.5)'
    )
    ingest_parser.add_argument(
        '--auto-approve',
        type=float,
        default=0.8,
        help='Auto-approve threshold (default: 0.8)'
    )
    ingest_parser.add_argument(
        '--update',
        action='store_true',
        help='Update the knowledge graph with new entities'
    )
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Display knowledge graph statistics')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Execute command
    try:
        if args.command == 'query':
            return cmd_query(args)
        elif args.command == 'ingest':
            return cmd_ingest(args)
        elif args.command == 'stats':
            return cmd_stats(args)
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
