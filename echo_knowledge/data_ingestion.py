#!/usr/bin/env python3
"""
Echo Knowledge Graph Data Ingestion Pipeline

This module provides automated data collection and enrichment capabilities
for the AI ecosystem knowledge graph. It can:
1. Extract entity information from various sources
2. Score relevance based on search patterns and activity
3. Continuously update the knowledge graph with new R&D results
"""

import yaml
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict
from enum import Enum


@dataclass
class SourceData:
    """Raw data from an external source"""
    source_type: str  # web_scraper, api, search_pattern, manual
    timestamp: datetime
    data: Dict[str, Any]
    confidence: float = 0.5


@dataclass
class EntityCandidate:
    """Candidate entity for ingestion"""
    entity_type: str
    name: str
    properties: Dict[str, Any]
    sources: List[SourceData]
    relevance_score: float = 0.0


class DataIngestionPipeline:
    """Pipeline for ingesting and enriching knowledge graph data"""
    
    def __init__(self, kg_data_path: str):
        self.kg_data_path = kg_data_path
        self.kg_data = self._load_yaml(kg_data_path)
        self.entity_candidates: List[EntityCandidate] = []
    
    def _load_yaml(self, path: str) -> Dict:
        """Load YAML file"""
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    
    def _save_yaml(self, data: Dict, path: str):
        """Save data to YAML file"""
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False, sort_keys=False)
    
    def ingest_search_patterns(self, search_history: List[Dict[str, Any]]) -> List[EntityCandidate]:
        """
        Extract entities from user search patterns
        
        Args:
            search_history: List of search queries with metadata
                Example: [
                    {
                        'query': 'AI workflow automation platforms',
                        'timestamp': '2024-01-15',
                        'clicks': ['jasper.ai', 'writesonic.com'],
                        'time_spent': {'jasper.ai': 120, 'writesonic.com': 85}
                    }
                ]
        """
        candidates = []
        
        # Keywords for different entity types
        org_keywords = ['lab', 'company', 'startup', 'research', 'institute', 'university']
        tool_keywords = ['tool', 'platform', 'api', 'framework', 'library', 'software']
        domain_keywords = ['automation', 'nlp', 'ai', 'machine learning', 'research', 'workflow']
        
        for search in search_history:
            query = search.get('query', '').lower()
            timestamp = datetime.fromisoformat(search.get('timestamp', datetime.now().isoformat()))
            clicks = search.get('clicks', [])
            time_spent = search.get('time_spent', {})
            
            # Calculate relevance based on user engagement
            base_relevance = 0.3
            
            # Identify entity type from query
            entity_type = None
            if any(kw in query for kw in org_keywords):
                entity_type = 'organization'
            elif any(kw in query for kw in tool_keywords):
                entity_type = 'tool'
            elif any(kw in query for kw in domain_keywords):
                entity_type = 'domain'
            
            # Extract entities from clicks
            for url in clicks:
                # Extract domain name as potential entity
                domain = self._extract_domain(url)
                if not domain:
                    continue
                
                # Calculate relevance score
                relevance = base_relevance
                
                # Boost if user spent significant time
                if url in time_spent and time_spent[url] > 60:
                    relevance += 0.3
                
                # Boost if recently searched
                days_ago = (datetime.now() - timestamp).days
                if days_ago < 7:
                    relevance += 0.2
                elif days_ago < 30:
                    relevance += 0.1
                
                # Create candidate
                source_data = SourceData(
                    source_type='search_pattern',
                    timestamp=timestamp,
                    data={'query': query, 'url': url, 'time_spent': time_spent.get(url, 0)},
                    confidence=0.6
                )
                
                candidate = EntityCandidate(
                    entity_type=entity_type or 'tool',
                    name=domain.replace('.', ' ').title(),
                    properties={
                        'website': url,
                        'discovered_from': query,
                        'user_engagement': time_spent.get(url, 0)
                    },
                    sources=[source_data],
                    relevance_score=min(relevance, 1.0)
                )
                
                candidates.append(candidate)
        
        self.entity_candidates.extend(candidates)
        return candidates
    
    def _extract_domain(self, url: str) -> Optional[str]:
        """Extract domain name from URL"""
        # Simple regex to extract domain
        match = re.search(r'(?:https?://)?(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})', url)
        return match.group(1) if match else None
    
    def ingest_web_scraper_results(self, scraper_results: List[Dict[str, Any]]) -> List[EntityCandidate]:
        """
        Ingest data from web scrapers
        
        Args:
            scraper_results: List of scraped entity data
                Example: [
                    {
                        'type': 'organization',
                        'name': 'Example AI Lab',
                        'description': '...',
                        'focus_areas': ['AI Safety', 'NLP'],
                        'source_url': 'https://example.com/about',
                        'scraped_at': '2024-01-15T10:00:00'
                    }
                ]
        """
        candidates = []
        
        for result in scraper_results:
            timestamp = datetime.fromisoformat(result.get('scraped_at', datetime.now().isoformat()))
            
            source_data = SourceData(
                source_type='web_scraper',
                timestamp=timestamp,
                data=result,
                confidence=0.7
            )
            
            # Extract properties based on entity type
            properties = {
                k: v for k, v in result.items()
                if k not in ['type', 'name', 'scraped_at']
            }
            
            candidate = EntityCandidate(
                entity_type=result.get('type', 'organization'),
                name=result.get('name', 'Unknown'),
                properties=properties,
                sources=[source_data],
                relevance_score=0.6  # Medium relevance for scraped data
            )
            
            candidates.append(candidate)
        
        self.entity_candidates.extend(candidates)
        return candidates
    
    def ingest_api_data(self, api_responses: List[Dict[str, Any]]) -> List[EntityCandidate]:
        """
        Ingest data from external APIs (e.g., research paper APIs, GitHub, etc.)
        
        Args:
            api_responses: List of API response data
                Example: [
                    {
                        'type': 'research_paper',
                        'title': 'Novel AI Approach',
                        'authors': ['John Doe', 'Jane Smith'],
                        'published_date': '2024-01-15',
                        'topics': ['AI', 'ML'],
                        'citations': 10,
                        'api_source': 'arxiv'
                    }
                ]
        """
        candidates = []
        
        for response in api_responses:
            timestamp = datetime.now()
            
            source_data = SourceData(
                source_type='api',
                timestamp=timestamp,
                data=response,
                confidence=0.8  # Higher confidence for API data
            )
            
            properties = {
                k: v for k, v in response.items()
                if k not in ['type', 'title', 'name']
            }
            
            entity_name = response.get('title') or response.get('name', 'Unknown')
            
            candidate = EntityCandidate(
                entity_type=response.get('type', 'research_paper'),
                name=entity_name,
                properties=properties,
                sources=[source_data],
                relevance_score=0.7
            )
            
            candidates.append(candidate)
        
        self.entity_candidates.extend(candidates)
        return candidates
    
    def enrich_entity(self, candidate: EntityCandidate) -> EntityCandidate:
        """
        Enrich an entity candidate with additional information
        """
        # Boost relevance based on multiple sources
        if len(candidate.sources) > 1:
            candidate.relevance_score = min(
                candidate.relevance_score + (len(candidate.sources) * 0.1),
                1.0
            )
        
        # Boost relevance for entities with API availability
        if candidate.properties.get('api_available'):
            candidate.relevance_score = min(candidate.relevance_score + 0.15, 1.0)
        
        # Boost relevance for recent activity
        if candidate.entity_type == 'research_paper':
            pub_date = candidate.properties.get('published_date')
            if pub_date:
                try:
                    pub_datetime = datetime.strptime(pub_date, '%Y-%m-%d')
                    days_ago = (datetime.now() - pub_datetime).days
                    if days_ago < 180:  # Within 6 months
                        candidate.relevance_score = min(candidate.relevance_score + 0.2, 1.0)
                except:
                    pass
        
        return candidate
    
    def deduplicate_candidates(self) -> List[EntityCandidate]:
        """
        Deduplicate entity candidates by merging similar entities
        """
        # Group by entity type and similar names
        grouped: Dict[Tuple[str, str], List[EntityCandidate]] = {}
        
        for candidate in self.entity_candidates:
            key = (candidate.entity_type, candidate.name.lower().strip())
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(candidate)
        
        # Merge duplicates
        deduplicated = []
        for (entity_type, name), candidates in grouped.items():
            if len(candidates) == 1:
                deduplicated.append(candidates[0])
            else:
                # Merge multiple candidates
                merged = candidates[0]
                all_sources = []
                all_properties = {}
                
                for cand in candidates:
                    all_sources.extend(cand.sources)
                    all_properties.update(cand.properties)
                
                merged.sources = all_sources
                merged.properties = all_properties
                merged.relevance_score = max(c.relevance_score for c in candidates)
                
                deduplicated.append(merged)
        
        self.entity_candidates = deduplicated
        return deduplicated
    
    def filter_by_relevance(self, min_relevance: float = 0.5) -> List[EntityCandidate]:
        """
        Filter candidates by minimum relevance score
        """
        filtered = [
            c for c in self.entity_candidates
            if c.relevance_score >= min_relevance
        ]
        self.entity_candidates = filtered
        return filtered
    
    def update_knowledge_graph(self, auto_approve_threshold: float = 0.8) -> Dict[str, int]:
        """
        Update the knowledge graph with approved candidates
        
        Args:
            auto_approve_threshold: Automatically add candidates above this relevance score
        
        Returns:
            Statistics about the update
        """
        stats = {
            'auto_approved': 0,
            'manual_review': 0,
            'total_candidates': len(self.entity_candidates)
        }
        
        entities = self.kg_data.get('entities', {})
        
        for candidate in self.entity_candidates:
            if candidate.relevance_score >= auto_approve_threshold:
                # Auto-approve and add to knowledge graph
                entity_list_key = f"{candidate.entity_type}s"
                if entity_list_key not in entities:
                    entities[entity_list_key] = []
                
                # Generate ID
                existing_ids = [e.get('id', '') for e in entities.get(entity_list_key, [])]
                new_id = self._generate_id(candidate.entity_type, len(existing_ids))
                
                # Create entity entry
                entity_entry = {
                    'id': new_id,
                    'name': candidate.name,
                    **candidate.properties,
                    'relevance_score': candidate.relevance_score,
                    'sources': [s.source_type for s in candidate.sources],
                    'ingested_at': datetime.now().isoformat()
                }
                
                entities[entity_list_key].append(entity_entry)
                stats['auto_approved'] += 1
            else:
                stats['manual_review'] += 1
        
        # Save updated knowledge graph
        self.kg_data['entities'] = entities
        self._save_yaml(self.kg_data, self.kg_data_path)
        
        return stats
    
    def _generate_id(self, entity_type: str, count: int) -> str:
        """Generate a unique ID for an entity"""
        prefix = entity_type[:3]
        return f"{prefix}_{str(count + 1).zfill(3)}"
    
    def generate_ingestion_report(self) -> str:
        """
        Generate a report of the ingestion pipeline results
        """
        report = []
        report.append("=" * 80)
        report.append("Echo Knowledge Graph Data Ingestion Report")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().isoformat()}")
        report.append("")
        
        # Summary statistics
        report.append("Summary:")
        report.append(f"  Total Candidates: {len(self.entity_candidates)}")
        
        # Group by entity type
        by_type = {}
        for candidate in self.entity_candidates:
            if candidate.entity_type not in by_type:
                by_type[candidate.entity_type] = []
            by_type[candidate.entity_type].append(candidate)
        
        report.append("")
        report.append("By Entity Type:")
        for entity_type, candidates in sorted(by_type.items()):
            avg_relevance = sum(c.relevance_score for c in candidates) / len(candidates)
            report.append(f"  {entity_type}: {len(candidates)} candidates (avg relevance: {avg_relevance:.2f})")
        
        # Top candidates
        report.append("")
        report.append("Top 10 Candidates by Relevance:")
        sorted_candidates = sorted(
            self.entity_candidates,
            key=lambda c: c.relevance_score,
            reverse=True
        )
        for i, candidate in enumerate(sorted_candidates[:10], 1):
            report.append(f"  {i}. {candidate.name} ({candidate.entity_type})")
            report.append(f"     Relevance: {candidate.relevance_score:.2f}")
            report.append(f"     Sources: {', '.join(set(s.source_type for s in candidate.sources))}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)


def main():
    """Example usage of the data ingestion pipeline"""
    import os
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(base_path, 'ai_ecosystem_data.yaml')
    
    # Initialize pipeline
    pipeline = DataIngestionPipeline(data_path)
    
    print("Echo Knowledge Graph Data Ingestion Pipeline")
    print("=" * 80)
    print()
    
    # Example 1: Ingest from search patterns
    print("Example 1: Ingesting from search patterns...")
    search_history = [
        {
            'query': 'AI workflow automation platforms',
            'timestamp': '2024-01-15T10:00:00',
            'clicks': ['https://zapier.com', 'https://make.com'],
            'time_spent': {'https://zapier.com': 120, 'https://make.com': 95}
        },
        {
            'query': 'AI research labs privacy',
            'timestamp': '2024-01-16T14:30:00',
            'clicks': ['https://anthropic.com', 'https://ai.facebook.com'],
            'time_spent': {'https://anthropic.com': 180, 'https://ai.facebook.com': 75}
        }
    ]
    
    candidates1 = pipeline.ingest_search_patterns(search_history)
    print(f"  Extracted {len(candidates1)} candidates from search patterns")
    print()
    
    # Example 2: Ingest from web scraper
    print("Example 2: Ingesting from web scraper...")
    scraper_results = [
        {
            'type': 'organization',
            'name': 'Cohere',
            'description': 'Enterprise AI platform for NLP',
            'focus_areas': ['NLP', 'Enterprise AI', 'API Services'],
            'source_url': 'https://cohere.ai/about',
            'scraped_at': '2024-01-17T09:00:00',
            'location': 'Toronto, Canada',
            'founded': '2019-01-01'
        }
    ]
    
    candidates2 = pipeline.ingest_web_scraper_results(scraper_results)
    print(f"  Extracted {len(candidates2)} candidates from web scraper")
    print()
    
    # Example 3: Ingest from API
    print("Example 3: Ingesting from API...")
    api_responses = [
        {
            'type': 'research_paper',
            'title': 'Advances in Workflow Automation with LLMs',
            'authors': ['Alice Johnson', 'Bob Smith'],
            'published_date': '2024-01-10',
            'topics': ['Workflow Automation', 'LLMs', 'AI Agents'],
            'citations': 5,
            'api_source': 'arxiv'
        }
    ]
    
    candidates3 = pipeline.ingest_api_data(api_responses)
    print(f"  Extracted {len(candidates3)} candidates from API")
    print()
    
    # Enrich and process
    print("Processing candidates...")
    for candidate in pipeline.entity_candidates:
        pipeline.enrich_entity(candidate)
    
    pipeline.deduplicate_candidates()
    pipeline.filter_by_relevance(min_relevance=0.4)
    print(f"  After deduplication and filtering: {len(pipeline.entity_candidates)} candidates")
    print()
    
    # Generate report
    print(pipeline.generate_ingestion_report())
    
    # Note: Commenting out the actual update to preserve the original data file
    # In production, you would call:
    # stats = pipeline.update_knowledge_graph(auto_approve_threshold=0.8)
    # print(f"\nUpdate Statistics:")
    # print(f"  Auto-approved: {stats['auto_approved']}")
    # print(f"  Manual review required: {stats['manual_review']}")


if __name__ == "__main__":
    main()
