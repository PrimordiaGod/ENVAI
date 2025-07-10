from abc import ABC, abstractmethod

class ResearchInterface(ABC):
    @abstractmethod
    def search(self, query: str) -> dict:
        """Perform a web search and return results as a dictionary."""
        pass

    @abstractmethod
    def summarize(self, results: dict) -> str:
        """Summarize the search results."""
        pass