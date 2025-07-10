from abc import ABC, abstractmethod
from typing import Optional, Callable, Dict, List

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

    # Phase 3: Enhanced Voice Features
    @abstractmethod
    def detect_wake_word(self, audio_data: bytes) -> bool:
        """Detect if wake word was spoken in audio data."""
        pass

    @abstractmethod
    def process_voice_command(self, command: str) -> Dict[str, any]:
        """Process voice commands and return structured data."""
        pass

    @abstractmethod
    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available voice options."""
        pass

    @abstractmethod
    def set_voice(self, voice_id: str) -> bool:
        """Set specific voice for text-to-speech."""
        pass

    @abstractmethod
    def get_voice_status(self) -> Dict[str, any]:
        """Get current voice interface status."""
        pass

    @abstractmethod
    def calibrate_microphone(self) -> Dict[str, any]:
        """Calibrate microphone for optimal performance."""
        pass

    @abstractmethod
    def start_voice_session(self) -> bool:
        """Start a voice interaction session."""
        pass

    @abstractmethod
    def end_voice_session(self) -> bool:
        """End the current voice interaction session."""
        pass