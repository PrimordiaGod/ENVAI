from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class AIModelResponse:
    """Structured response from AI model."""
    text: str
    confidence: float
    model_used: str
    tokens_used: int
    processing_time: float
    metadata: Dict[str, Any]

class AIModelInterface(ABC):
    """Interface for AI model integration."""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the AI model with configuration."""
        pass

    @abstractmethod
    def generate_response(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> AIModelResponse:
        """Generate a response using the AI model."""
        pass

    @abstractmethod
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of the given text."""
        pass

    @abstractmethod
    def extract_intent(self, text: str) -> Dict[str, Any]:
        """Extract user intent from text."""
        pass

    @abstractmethod
    def summarize_text(self, text: str, max_length: int = 200) -> str:
        """Summarize the given text."""
        pass

    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check if the AI model is available."""
        pass

    @abstractmethod
    def get_usage_stats(self) -> Dict[str, Any]:
        """Get usage statistics for the model."""
        pass

    @abstractmethod
    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model."""
        pass

    @abstractmethod
    def get_available_models(self) -> List[Dict[str, Any]]:
        """Get list of available models."""
        pass

    @abstractmethod
    def fine_tune_context(self, user_id: str, conversation_history: List[Dict[str, Any]]) -> bool:
        """Fine-tune the model context for a specific user."""
        pass

    @abstractmethod
    def validate_response(self, response: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the generated response against context."""
        pass

class LanguageModelInterface(ABC):
    @abstractmethod
    def load_model(self, model_name: str) -> bool:
        """Load a specific language model."""
        pass

    @abstractmethod
    def generate_completion(self, prompt: str, max_tokens: int = 100) -> str:
        """Generate text completion."""
        pass

    @abstractmethod
    def generate_embedding(self, text: str) -> List[float]:
        """Generate text embeddings."""
        pass

    @abstractmethod
    def calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts."""
        pass

class PersonalizationInterface(ABC):
    @abstractmethod
    def learn_user_patterns(self, user_id: str, data: dict) -> bool:
        """Learn patterns from user data."""
        pass

    @abstractmethod
    def predict_user_preferences(self, user_id: str, context: dict) -> dict:
        """Predict user preferences based on learned patterns."""
        pass

    @abstractmethod
    def adapt_response_style(self, user_id: str, base_response: str) -> str:
        """Adapt response style to user preferences."""
        pass

    @abstractmethod
    def get_user_profile(self, user_id: str) -> dict:
        """Get user's learned profile."""
        pass