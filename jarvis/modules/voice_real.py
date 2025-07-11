from jarvis.interfaces.voice import VoiceInterface
from typing import Optional, Callable, List
import threading
import time
import speech_recognition as sr
import pyttsx3
import queue

class RealVoiceInterface(VoiceInterface):
    def __init__(self):
        self._is_initialized = False
        self._is_listening = False
        self._voice_callback = None
        self._voice_settings = {
            'speed': 1.0,
            'pitch': 1.0,
            'language': 'en-US',
            'voice_enabled': True
        }
        self._continuous_thread = None
        self._audio_queue = queue.Queue()
        
        # Speech recognition components
        self._recognizer = None
        self._microphone = None
        
        # Text-to-speech components
        self._tts_engine = None

    def initialize(self) -> bool:
        """Initialize the real voice interface."""
        try:
            # Initialize speech recognition
            self._recognizer = sr.Recognizer()
            self._microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # Initialize text-to-speech
            self._tts_engine = pyttsx3.init()
            
            # Configure TTS settings
            self._tts_engine.setProperty('rate', int(200 * self._voice_settings['speed']))
            self._tts_engine.setProperty('volume', 0.9)
            
            # Get available voices and set a default
            voices = self._tts_engine.getProperty('voices')
            if voices:
                self._tts_engine.setProperty('voice', voices[0].id)
            
            self._is_initialized = True
            return True
            
        except Exception as e:
            print(f"Voice interface initialization failed: {e}")
            return False

    def listen(self, timeout: float = 5.0) -> Optional[str]:
        """Listen for voice input and return transcribed text."""
        if not self._is_initialized:
            print("Voice interface not initialized")
            return None
        
        try:
            with self._microphone as source:
                print(f"[Voice] Listening for {timeout} seconds...")
                audio = self._recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                # Try to recognize speech
                try:
                    text = self._recognizer.recognize_google(audio)
                    print(f"[Voice] Recognized: {text}")
                    return text
                except sr.UnknownValueError:
                    print("[Voice] Could not understand audio")
                    return None
                except sr.RequestError as e:
                    print(f"[Voice] Recognition service error: {e}")
                    return None
                    
        except Exception as e:
            print(f"Error during speech recognition: {e}")
            return None

    def speak(self, text: str) -> bool:
        """Convert text to speech and play it."""
        if not self._is_initialized or not self._voice_settings['voice_enabled']:
            return False
        
        try:
            print(f"[Voice] Speaking: {text}")
            self._tts_engine.say(text)
            self._tts_engine.runAndWait()
            return True
        except Exception as e:
            print(f"Error during text-to-speech: {e}")
            return False

    def is_listening(self) -> bool:
        """Check if the voice interface is currently listening."""
        return self._is_listening

    def set_voice_callback(self, callback: Callable[[str], None]) -> None:
        """Set a callback function to handle voice input."""
        self._voice_callback = callback

    def set_voice_settings(self, settings: dict) -> None:
        """Configure voice settings."""
        self._voice_settings.update(settings)
        
        # Update TTS engine settings if available
        if self._tts_engine:
            if 'speed' in settings:
                self._tts_engine.setProperty('rate', int(200 * settings['speed']))
            if 'pitch' in settings:
                # Note: pyttsx3 doesn't directly support pitch, but we store it
                pass

    def get_voice_settings(self) -> dict:
        """Get current voice settings."""
        return self._voice_settings.copy()

    def start_continuous_listening(self) -> bool:
        """Start continuous listening mode."""
        if not self._is_initialized:
            return False
        
        if self._is_listening:
            return True
        
        self._is_listening = True
        self._continuous_thread = threading.Thread(target=self._continuous_listen_loop)
        self._continuous_thread.daemon = True
        self._continuous_thread.start()
        return True

    def stop_continuous_listening(self) -> bool:
        """Stop continuous listening mode."""
        self._is_listening = False
        if self._continuous_thread:
            self._continuous_thread.join(timeout=1.0)
        return True

    def _continuous_listen_loop(self):
        """Continuous listening loop for background processing."""
        while self._is_listening:
            try:
                # Listen for a short duration
                result = self.listen(timeout=1.0)
                if result and self._voice_callback:
                    self._voice_callback(result)
                time.sleep(0.1)  # Small delay to prevent CPU overuse
            except Exception as e:
                print(f"Error in continuous listening: {e}")
                break

    def simulate_voice_input(self, text: str) -> bool:
        """Simulate voice input for testing purposes."""
        if self._voice_callback:
            self._voice_callback(text)
            return True
        return False

    def get_available_voices(self) -> List[dict]:
        """Get list of available TTS voices."""
        if not self._tts_engine:
            return []
        
        voices = self._tts_engine.getProperty('voices')
        voice_list = []
        for voice in voices:
            voice_list.append({
                'id': voice.id,
                'name': voice.name,
                'languages': voice.languages
            })
        return voice_list

    def set_voice(self, voice_id: str) -> bool:
        """Set a specific voice for TTS."""
        if not self._tts_engine:
            return False
        
        try:
            self._tts_engine.setProperty('voice', voice_id)
            return True
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False