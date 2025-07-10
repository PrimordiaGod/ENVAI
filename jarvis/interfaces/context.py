from abc import ABC, abstractmethod

class ContextEngineInterface(ABC):
    @abstractmethod
    def store_context(self, user_id: str, context: dict) -> None:
        """Store the context for a user."""
        pass

    @abstractmethod
    def retrieve_context(self, user_id: str) -> dict:
        """Retrieve the context for a user."""
        pass

    @abstractmethod
    def clear_context(self, user_id: str) -> None:
        """Clear the context for a user."""
        pass