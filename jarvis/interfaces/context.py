from abc import ABC, abstractmethod

from typing import Dict, List, Optional, Any

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

    # Phase 2: Long-term memory and personalization

    @abstractmethod

    def store_long_term_memory(self, user_id: str, memory: dict) -> None:

        """Store long-term memory for a user (preferences, patterns, etc.)."""

        pass

    @abstractmethod

    def retrieve_long_term_memory(self, user_id: str) -> dict:

        """Retrieve long-term memory for a user."""

        pass

    @abstractmethod

    def anticipate_user_intent(self, user_id: str, current_input: str) -> List[str]:

        """Anticipate user's next likely actions based on history and patterns."""

        pass

    @abstractmethod

    def update_user_preferences(self, user_id: str, preferences: dict) -> None:

        """Update user preferences and personalization data."""

        pass

    @abstractmethod

    def get_user_preferences(self, user_id: str) -> dict:

        """Get user preferences for personalization."""

        pass

    @abstractmethod

    def analyze_conversation_patterns(self, user_id: str) -> dict:

        """Analyze conversation patterns to improve anticipation."""

        pass