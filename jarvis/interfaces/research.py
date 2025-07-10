from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any

class ResearchInterface(ABC):
    @abstractmethod
    def search(self, query: str) -> dict:
        """Perform a web search and return results as a dictionary."""
        pass

    @abstractmethod
    def summarize(self, results: dict) -> str:
        """Summarize the search results."""
        pass

    # Phase 2: Enhanced research capabilities
    @abstractmethod
    def multi_source_search(self, query: str, sources: List[str] = None) -> dict:
        """Search multiple sources and synthesize results."""
        pass

    @abstractmethod
    def deep_analysis(self, query: str, context: dict = None) -> dict:
        """Perform deep analysis of a topic with context awareness."""
        pass

    @abstractmethod
    def synthesize_information(self, sources: List[dict]) -> str:
        """Synthesize information from multiple sources."""
        pass

    @abstractmethod
    def fact_check(self, statement: str) -> dict:
        """Fact-check a statement against reliable sources."""
        pass

    @abstractmethod
    def get_trending_topics(self, category: str = None) -> List[str]:
        """Get trending topics for research suggestions."""
        pass

    @abstractmethod
    def save_research_session(self, session_id: str, data: dict) -> None:
        """Save a research session for later reference."""
        pass

    @abstractmethod
    def load_research_session(self, session_id: str) -> dict:
        """Load a previously saved research session."""
        pass