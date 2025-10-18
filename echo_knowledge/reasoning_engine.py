#!/usr/bin/env python3
"""
Echo Knowledge Graph Reasoning Engine

This module provides reasoning capabilities over the AI ecosystem knowledge graph.
It can answer queries about organizations, tools, domains, and their relationships.
"""

import yaml
import json
from datetime import datetime
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum


class EntityType(Enum):
    """Entity types in the knowledge graph"""
    ORGANIZATION = "Organization"
    TOOL = "Tool"
    DOMAIN = "Domain"
    RESEARCH_PAPER = "ResearchPaper"


@dataclass
class Entity:
    """Base entity in the knowledge graph"""
    id: str
    type: EntityType
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Relationship:
    """Relationship between entities"""
    type: str
    from_entity: str
    to_entity: str
    properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ReasoningResult:
    """Result of a reasoning query"""
    query: str
    results: List[Dict[str, Any]]
    confidence: float
    provenance: List[str]
    reasoning_trace: List[str]


class KnowledgeGraph:
    """Knowledge graph for AI ecosystem tracking"""
    
    def __init__(self, schema_path: str, data_path: str):
        """Initialize knowledge graph with schema and data"""
        self.entities: Dict[str, Entity] = {}
        self.relationships: List[Relationship] = []
        self.schema = self._load_yaml(schema_path)
        self.data = self._load_yaml(data_path)
        self._build_graph()
    
    def _load_yaml(self, path: str) -> Dict:
        """Load YAML file"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def _build_graph(self):
        """Build graph from data"""
        # Load entities
        data_entities = self.data.get('entities', {})
        
        # Organizations
        for org in data_entities.get('organizations', []):
            entity = Entity(
                id=org['id'],
                type=EntityType.ORGANIZATION,
                properties=org
            )
            self.entities[org['id']] = entity
        
        # Tools
        for tool in data_entities.get('tools', []):
            entity = Entity(
                id=tool['id'],
                type=EntityType.TOOL,
                properties=tool
            )
            self.entities[tool['id']] = entity
        
        # Domains
        for domain in data_entities.get('domains', []):
            entity = Entity(
                id=domain['id'],
                type=EntityType.DOMAIN,
                properties=domain
            )
            self.entities[domain['id']] = entity
        
        # Research papers
        for paper in data_entities.get('research_papers', []):
            entity = Entity(
                id=paper['id'],
                type=EntityType.RESEARCH_PAPER,
                properties=paper
            )
            self.entities[paper['id']] = entity
        
        # Load relationships
        data_rels = self.data.get('relationships', {})
        
        for rel_type, rels in data_rels.items():
            for rel in rels:
                relationship = Relationship(
                    type=rel_type.upper(),
                    from_entity=rel['from'],
                    to_entity=rel['to'],
                    properties=rel.get('properties', {})
                )
                self.relationships.append(relationship)
    
    def find_entity(self, entity_id: str) -> Optional[Entity]:
        """Find entity by ID"""
        return self.entities.get(entity_id)
    
    def find_entities_by_type(self, entity_type: EntityType) -> List[Entity]:
        """Find all entities of a given type"""
        return [e for e in self.entities.values() if e.type == entity_type]
    
    def find_relationships(self, from_id: str = None, to_id: str = None, 
                          rel_type: str = None) -> List[Relationship]:
        """Find relationships matching criteria"""
        results = self.relationships
        
        if from_id:
            results = [r for r in results if r.from_entity == from_id]
        if to_id:
            results = [r for r in results if r.to_entity == to_id]
        if rel_type:
            results = [r for r in results if r.type == rel_type.upper()]
        
        return results
    
    def get_related_entities(self, entity_id: str, rel_type: str = None) -> List[Entity]:
        """Get entities related to a given entity"""
        relationships = self.find_relationships(from_id=entity_id, rel_type=rel_type)
        related_ids = [r.to_entity for r in relationships]
        return [self.entities[eid] for eid in related_ids if eid in self.entities]


class EchoReasoningEngine:
    """Reasoning engine for Echo knowledge graph queries"""
    
    def __init__(self, knowledge_graph: KnowledgeGraph):
        self.kg = knowledge_graph
    
    def find_collaboration_opportunities(self, target_domains: List[str], 
                                        focus: str = "workflow_automation") -> ReasoningResult:
        """
        Find AI labs/organizations that could enhance Balorg's capabilities
        
        This implements the reasoning example from the problem statement:
        "Which AI labs specialize in workflow automation research that could enhance Balorg's capabilities?"
        """
        reasoning_trace = []
        provenance = []
        results = []
        
        # Step 1: Identify Balorg's domain
        reasoning_trace.append("Step 1: Identify Balorg's domain → 'privacy-protected AI automation'")
        
        # Step 2: Traverse KG to find relevant organizations
        reasoning_trace.append(f"Step 2: Traverse KG → find labs tagged with {focus}")
        
        # Find all organizations
        orgs = self.kg.find_entities_by_type(EntityType.ORGANIZATION)
        
        for org in orgs:
            # Check if org specializes in target domains
            specializations = self.kg.find_relationships(
                from_id=org.id,
                rel_type="SPECIALIZES_IN"
            )
            
            relevant_domains = []
            for spec in specializations:
                domain = self.kg.find_entity(spec.to_entity)
                if domain and domain.properties.get('name') in target_domains:
                    relevant_domains.append(domain.properties.get('name'))
            
            if not relevant_domains:
                continue
            
            # Step 3: Apply rule - prefer labs with open APIs or recent research
            reasoning_trace.append(f"Step 3: Evaluating {org.properties.get('name')}")
            
            # Check for tools with APIs
            tools_used = self.kg.find_relationships(from_id=org.id, rel_type="USES")
            api_tools = []
            for tool_rel in tools_used:
                tool = self.kg.find_entity(tool_rel.to_entity)
                if tool and tool.properties.get('api_available'):
                    api_tools.append(tool.properties.get('name'))
            
            # Check for recent publications
            publications = self.kg.find_relationships(from_id=org.id, rel_type="PUBLISHED")
            recent_papers = []
            for pub_rel in publications:
                paper = self.kg.find_entity(pub_rel.to_entity)
                if paper:
                    pub_date_str = paper.properties.get('published_date', '')
                    try:
                        pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d')
                        if pub_date.year >= 2023:
                            recent_papers.append(paper.properties.get('title'))
                    except:
                        pass
            
            # Calculate confidence score
            confidence = 0.0
            if relevant_domains:
                confidence += 0.4
            if api_tools:
                confidence += 0.3
            if recent_papers:
                confidence += 0.3
            
            # Step 4: Return ranked results
            result = {
                'organization': org.properties.get('name'),
                'type': org.properties.get('type'),
                'relevant_domains': relevant_domains,
                'api_tools': api_tools,
                'recent_publications': recent_papers,
                'confidence': confidence,
                'website': org.properties.get('website'),
                'location': org.properties.get('location')
            }
            
            results.append(result)
            provenance.append(f"Data from entity: {org.id}")
        
        # Sort by confidence
        results.sort(key=lambda x: x['confidence'], reverse=True)
        
        reasoning_trace.append(f"Step 4: Ranked {len(results)} organizations by confidence")
        
        overall_confidence = sum(r['confidence'] for r in results) / len(results) if results else 0.0
        
        return ReasoningResult(
            query=f"Find organizations specializing in {target_domains} with focus on {focus}",
            results=results,
            confidence=overall_confidence,
            provenance=provenance,
            reasoning_trace=reasoning_trace
        )
    
    def discover_workflow_automation_stacks(self) -> ReasoningResult:
        """
        Find integrated tool stacks for workflow automation
        """
        reasoning_trace = ["Discovering workflow automation tool stacks"]
        provenance = []
        results = []
        
        # Find workflow automation domain
        domains = self.kg.find_entities_by_type(EntityType.DOMAIN)
        workflow_domain = None
        for domain in domains:
            if domain.properties.get('name') == 'Workflow Automation':
                workflow_domain = domain
                break
        
        if not workflow_domain:
            return ReasoningResult(
                query="Discover workflow automation stacks",
                results=[],
                confidence=0.0,
                provenance=[],
                reasoning_trace=["Domain 'Workflow Automation' not found"]
            )
        
        reasoning_trace.append(f"Found domain: {workflow_domain.properties.get('name')}")
        
        # Find organizations specializing in this domain
        specializations = self.kg.find_relationships(
            to_id=workflow_domain.id,
            rel_type="SPECIALIZES_IN"
        )
        
        for spec in specializations:
            org = self.kg.find_entity(spec.from_entity)
            if not org:
                continue
            
            # Find tools this org uses
            tools_used = self.kg.find_relationships(from_id=org.id, rel_type="USES")
            tool_names = []
            for tool_rel in tools_used:
                tool = self.kg.find_entity(tool_rel.to_entity)
                if tool:
                    tool_names.append({
                        'name': tool.properties.get('name'),
                        'category': tool.properties.get('category'),
                        'api_available': tool.properties.get('api_available')
                    })
            
            results.append({
                'organization': org.properties.get('name'),
                'automation_stack': tool_names,
                'expertise_level': spec.properties.get('expertise_level'),
                'years_active': spec.properties.get('years_active')
            })
            
            provenance.append(f"Organization: {org.id}, Domain: {workflow_domain.id}")
        
        reasoning_trace.append(f"Found {len(results)} organizations with automation stacks")
        
        return ReasoningResult(
            query="Discover workflow automation stacks",
            results=results,
            confidence=0.85,
            provenance=provenance,
            reasoning_trace=reasoning_trace
        )
    
    def analyze_research_trends(self, since_year: int = 2023) -> ReasoningResult:
        """
        Track emerging research trends and key players
        """
        reasoning_trace = [f"Analyzing research trends since {since_year}"]
        provenance = []
        topic_counts = {}
        org_contributions = {}
        
        # Find all research papers since specified year
        papers = self.kg.find_entities_by_type(EntityType.RESEARCH_PAPER)
        
        for paper in papers:
            pub_date_str = paper.properties.get('published_date', '')
            try:
                pub_date = datetime.strptime(pub_date_str, '%Y-%m-%d')
                if pub_date.year < since_year:
                    continue
            except:
                continue
            
            # Count topics
            topics = paper.properties.get('topics', [])
            for topic in topics:
                topic_counts[topic] = topic_counts.get(topic, 0) + 1
            
            # Find publishing organization
            publishers = self.kg.find_relationships(to_id=paper.id, rel_type="PUBLISHED")
            for pub_rel in publishers:
                org = self.kg.find_entity(pub_rel.from_entity)
                if org:
                    org_name = org.properties.get('name')
                    if org_name not in org_contributions:
                        org_contributions[org_name] = []
                    org_contributions[org_name].append({
                        'title': paper.properties.get('title'),
                        'citations': paper.properties.get('citations', 0),
                        'relevance_score': paper.properties.get('relevance_score', 0.0)
                    })
        
        # Sort topics by frequency
        sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
        
        results = {
            'trending_topics': [
                {'topic': topic, 'frequency': count}
                for topic, count in sorted_topics
            ],
            'top_contributors': [
                {
                    'organization': org,
                    'paper_count': len(papers),
                    'total_citations': sum(p['citations'] for p in papers),
                    'papers': papers
                }
                for org, papers in sorted(
                    org_contributions.items(),
                    key=lambda x: len(x[1]),
                    reverse=True
                )
            ]
        }
        
        reasoning_trace.append(f"Analyzed {len(papers)} papers")
        reasoning_trace.append(f"Identified {len(sorted_topics)} trending topics")
        reasoning_trace.append(f"Found {len(org_contributions)} contributing organizations")
        
        return ReasoningResult(
            query=f"Analyze research trends since {since_year}",
            results=[results],
            confidence=0.90,
            provenance=[f"Analyzed {len(papers)} papers"],
            reasoning_trace=reasoning_trace
        )
    
    def query(self, query_type: str, **kwargs) -> ReasoningResult:
        """
        Execute a reasoning query
        
        Supported query types:
        - collaboration_opportunities: Find potential collaboration partners
        - workflow_stacks: Discover workflow automation tool stacks
        - research_trends: Analyze research trends and contributors
        """
        if query_type == "collaboration_opportunities":
            target_domains = kwargs.get('target_domains', ['Workflow Automation', 'AI Privacy & Safety'])
            focus = kwargs.get('focus', 'workflow_automation')
            return self.find_collaboration_opportunities(target_domains, focus)
        
        elif query_type == "workflow_stacks":
            return self.discover_workflow_automation_stacks()
        
        elif query_type == "research_trends":
            since_year = kwargs.get('since_year', 2023)
            return self.analyze_research_trends(since_year)
        
        else:
            return ReasoningResult(
                query=query_type,
                results=[],
                confidence=0.0,
                provenance=[],
                reasoning_trace=[f"Unknown query type: {query_type}"]
            )


def main():
    """Example usage of the reasoning engine"""
    import os
    
    # Get paths
    base_path = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_path, 'knowledge_graph_schema.yaml')
    data_path = os.path.join(base_path, 'ai_ecosystem_data.yaml')
    
    # Initialize knowledge graph and reasoning engine
    kg = KnowledgeGraph(schema_path, data_path)
    engine = EchoReasoningEngine(kg)
    
    print("=" * 80)
    print("Echo Knowledge Graph Reasoning Engine")
    print("=" * 80)
    print()
    
    # Query 1: Find collaboration opportunities
    print("Query 1: Which AI labs specialize in workflow automation research")
    print("         that could enhance Balorg's capabilities?")
    print("-" * 80)
    result1 = engine.query(
        "collaboration_opportunities",
        target_domains=['Workflow Automation', 'AI Privacy & Safety'],
        focus='workflow_automation'
    )
    
    print("\nReasoning Trace:")
    for i, trace in enumerate(result1.reasoning_trace, 1):
        print(f"  {i}. {trace}")
    
    print(f"\nConfidence: {result1.confidence:.2f}")
    print(f"\nTop Results:")
    for i, result in enumerate(result1.results[:3], 1):
        print(f"\n  {i}. {result['organization']} ({result['type']})")
        print(f"     Domains: {', '.join(result['relevant_domains'])}")
        print(f"     API Tools: {', '.join(result['api_tools']) if result['api_tools'] else 'None'}")
        print(f"     Recent Publications: {len(result['recent_publications'])}")
        print(f"     Confidence: {result['confidence']:.2f}")
        print(f"     Website: {result['website']}")
    
    print("\n" + "=" * 80)
    
    # Query 2: Workflow automation stacks
    print("\nQuery 2: Discover workflow automation tool stacks")
    print("-" * 80)
    result2 = engine.query("workflow_stacks")
    
    print("\nReasoning Trace:")
    for i, trace in enumerate(result2.reasoning_trace, 1):
        print(f"  {i}. {trace}")
    
    print(f"\nResults:")
    for i, result in enumerate(result2.results, 1):
        print(f"\n  {i}. {result['organization']}")
        print(f"     Expertise: {result['expertise_level']} ({result['years_active']} years)")
        print(f"     Tools in stack:")
        for tool in result['automation_stack']:
            print(f"       - {tool['name']} ({tool['category']}) - API: {tool['api_available']}")
    
    print("\n" + "=" * 80)
    
    # Query 3: Research trends
    print("\nQuery 3: Analyze research trends since 2023")
    print("-" * 80)
    result3 = engine.query("research_trends", since_year=2023)
    
    print("\nReasoning Trace:")
    for i, trace in enumerate(result3.reasoning_trace, 1):
        print(f"  {i}. {trace}")
    
    trends = result3.results[0]
    print(f"\nTrending Topics:")
    for i, topic in enumerate(trends['trending_topics'][:5], 1):
        print(f"  {i}. {topic['topic']}: {topic['frequency']} papers")
    
    print(f"\nTop Contributors:")
    for i, contrib in enumerate(trends['top_contributors'][:3], 1):
        print(f"\n  {i}. {contrib['organization']}")
        print(f"     Papers: {contrib['paper_count']}")
        print(f"     Total Citations: {contrib['total_citations']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()
