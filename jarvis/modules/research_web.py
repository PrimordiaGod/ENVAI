from jarvis.interfaces.research import ResearchInterface
import requests
import json
import datetime
from typing import Dict, List, Optional, Any
from collections import defaultdict

class WebResearch(ResearchInterface):
    def __init__(self):
        self._research_sessions = {}
        self._sources = {
            'duckduckgo': 'https://api.duckduckgo.com/',
            'wikipedia': 'https://en.wikipedia.org/api/rest_v1/page/summary/',
            'newsapi': 'https://newsapi.org/v2/everything'  # Would need API key
        }

    def search(self, query: str) -> dict:
        # DuckDuckGo Instant Answer API (no key required, limited info)
        url = 'https://api.duckduckgo.com/'
        params = {'q': query, 'format': 'json', 'no_redirect': 1, 'no_html': 1}
        resp = requests.get(url, params=params)
        if resp.status_code == 200:
            return resp.json()
        return {}

    def summarize(self, results: dict) -> str:
        # Use AbstractText and AbstractURL if available
        abstract = results.get('AbstractText')
        url = results.get('AbstractURL')
        if abstract and url:
            return f"{abstract}\nSource: {url}"
        elif abstract:
            return abstract
        elif url:
            return f"Source: {url}"
        else:
            return "No summary available."

    def multi_source_search(self, query: str, sources: List[str] = None) -> dict:
        """Search multiple sources and synthesize results."""
        if sources is None:
            sources = ['duckduckgo']
        
        all_results = {}
        for source in sources:
            try:
                if source == 'duckduckgo':
                    results = self.search(query)
                    all_results[source] = results
                # Add more sources as needed
            except Exception as e:
                all_results[source] = {'error': str(e)}
        
        return {
            'query': query,
            'sources': all_results,
            'timestamp': datetime.datetime.now().isoformat()
        }

    def deep_analysis(self, query: str, context: dict = None) -> dict:
        """Perform deep analysis of a topic with context awareness."""
        # Enhanced search with context
        enhanced_query = query
        if context and context.get('previous_topics'):
            enhanced_query = f"{query} {context['previous_topics']}"
        
        # Multi-source search
        results = self.multi_source_search(enhanced_query)
        
        # Analyze results
        analysis = {
            'query': query,
            'enhanced_query': enhanced_query,
            'sources_consulted': len(results['sources']),
            'key_findings': self._extract_key_findings(results),
            'confidence_score': self._calculate_confidence(results),
            'recommendations': self._generate_recommendations(results),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        return analysis

    def synthesize_information(self, sources: List[dict]) -> str:
        """Synthesize information from multiple sources."""
        if not sources:
            return "No sources provided for synthesis."
        
        # Extract key information from each source
        key_points = []
        for source in sources:
            if 'AbstractText' in source:
                key_points.append(source['AbstractText'])
            elif 'error' not in source:
                key_points.append(str(source))
        
        if not key_points:
            return "Unable to extract information from provided sources."
        
        # Simple synthesis (in future phases, could use NLP/ML)
        synthesis = f"Based on {len(sources)} sources:\n\n"
        for i, point in enumerate(key_points[:3], 1):  # Limit to 3 key points
            synthesis += f"{i}. {point}\n"
        
        return synthesis

    def fact_check(self, statement: str) -> dict:
        """Fact-check a statement against reliable sources."""
        # Search for the statement
        results = self.search(statement)
        
        # Simple fact-checking logic
        fact_check_result = {
            'statement': statement,
            'sources_found': len(results) > 0,
            'confidence': 'medium' if results else 'low',
            'supporting_evidence': results.get('AbstractText', ''),
            'source_url': results.get('AbstractURL', ''),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        return fact_check_result

    def get_trending_topics(self, category: str = None) -> List[str]:
        """Get trending topics for research suggestions."""
        # Simple trending topics (in future phases, could use real APIs)
        trending = [
            "artificial intelligence developments",
            "climate change research",
            "space exploration news",
            "technology innovations",
            "scientific discoveries"
        ]
        
        if category:
            # Filter by category if provided
            trending = [topic for topic in trending if category.lower() in topic.lower()]
        
        return trending

    def save_research_session(self, session_id: str, data: dict) -> None:
        """Save a research session for later reference."""
        self._research_sessions[session_id] = {
            'data': data,
            'timestamp': datetime.datetime.now().isoformat()
        }

    def load_research_session(self, session_id: str) -> dict:
        """Load a previously saved research session."""
        return self._research_sessions.get(session_id, {})

    def _extract_key_findings(self, results: dict) -> List[str]:
        """Extract key findings from search results."""
        findings = []
        for source, data in results['sources'].items():
            if 'AbstractText' in data:
                findings.append(data['AbstractText'])
        return findings[:3]  # Return top 3 findings

    def _calculate_confidence(self, results: dict) -> float:
        """Calculate confidence score based on source quality and quantity."""
        valid_sources = sum(1 for data in results['sources'].values() if 'error' not in data)
        total_sources = len(results['sources'])
        return min(valid_sources / max(total_sources, 1), 1.0)

    def _generate_recommendations(self, results: dict) -> List[str]:
        """Generate recommendations based on search results."""
        recommendations = []
        
        # Simple recommendation logic
        if results['sources']:
            recommendations.append("Consider exploring related topics for more depth")
            recommendations.append("Verify information across multiple sources")
        
        return recommendations