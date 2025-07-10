from abc import ABC, abstractmethod
from typing import Optional, Callable

class VoiceInterface(ABC):
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the voice interface (microphone, speakers, etc.)."""
        pass

    @abstractmethod
    def listen(self, timeout: float = 5.0) -> Optional[str]:
        """Listen for voice input and return transcribed text."""
        pass

    @abstractmethod
    def speak(self, text: str) -> bool:
        """Convert text to speech and play it."""
        pass

    @abstractmethod
    def is_listening(self) -> bool:
        """Check if the voice interface is currently listening."""
        pass

    @abstractmethod
    def set_voice_callback(self, callback: Callable[[str], None]) -> None:
        """Set a callback function to handle voice input."""
        pass

    @abstractmethod
    def set_voice_settings(self, settings: dict) -> None:
        """Configure voice settings (speed, pitch, language, etc.)."""
        pass

    @abstractmethod
    def get_voice_settings(self) -> dict:
        """Get current voice settings."""
        pass

    @abstractmethod
    def start_continuous_listening(self) -> bool:
        """Start continuous listening mode."""
        pass

    @abstractmethod
    def stop_continuous_listening(self) -> bool:
        """Stop continuous listening mode."""
        pass