from jarvis.interfaces.voice import VoiceInterface
from typing import Optional, Callable, Dict, List
import threading
import time
import queue
import re
import json
import os

try:
    import speech_recognition as sr
    import pyttsx3
    import sounddevice as sd
    import numpy as np
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False
    print("Warning: Voice libraries not available. Install with: pip install SpeechRecognition pyttsx3 sounddevice")

class AdvancedVoiceInterface(VoiceInterface):
    def __init__(self):
        self._is_initialized = False
        self._is_listening = False
        self._voice_callback = None
        self._voice_settings = {
            'speed': 1.0,
            'pitch': 1.0,
            'language': 'en-US',
            'voice_enabled': True,
            'wake_word': 'jarvis',
            'voice_id': None,
            'volume': 1.0
        }
        self._continuous_thread = None
        self._audio_queue = queue.Queue()
        self._recognizer = None
        self._engine = None
        self._microphone = None
        self._current_session = None

    def initialize(self) -> bool:
        """Initialize the voice interface with real speech recognition."""
        if not VOICE_AVAILABLE:
            print("Voice libraries not available. Using simulation mode.")
            self._is_initialized = True
            return True

        try:
            # Initialize speech recognition
            self._recognizer = sr.Recognizer()
            self._recognizer.energy_threshold = 4000
            self._recognizer.dynamic_energy_threshold = True
            self._recognizer.pause_threshold = 0.8

            # Initialize text-to-speech engine
            self._engine = pyttsx3.init()
            self._engine.setProperty('rate', int(200 * self._voice_settings['speed']))
            self._engine.setProperty('volume', self._voice_settings['volume'])

            # Get available voices
            voices = self._engine.getProperty('voices')
            if voices:
                self._voice_settings['voice_id'] = voices[0].id
                self._engine.setProperty('voice', voices[0].id)

            # Initialize microphone
            self._microphone = sr.Microphone()
            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=1)

            self._is_initialized = True
            print("✅ Voice interface initialized successfully")
            return True

        except Exception as e:
            print(f"❌ Voice interface initialization failed: {e}")
            return False

    def listen(self, timeout: float = 5.0) -> Optional[str]:
        """Listen for voice input and return transcribed text."""
        if not self._is_initialized:
            print("Voice interface not initialized")
            return None

        if not VOICE_AVAILABLE:
            print(f"[Voice] Listening for {timeout} seconds... (simulation mode)")
            time.sleep(1)
            return None

        try:
            with self._microphone as source:
                print(f"[Voice] Listening for {timeout} seconds...")
                audio = self._recognizer.listen(source, timeout=timeout, phrase_time_limit=10)
                
                try:
                    text = self._recognizer.recognize_google(audio)
                    print(f"[Voice] Heard: {text}")
                    return text
                except sr.UnknownValueError:
                    print("[Voice] Could not understand audio")
                    return None
                except sr.RequestError as e:
                    print(f"[Voice] Speech recognition error: {e}")
                    return None

        except Exception as e:
            print(f"[Voice] Error during listening: {e}")
            return None

    def speak(self, text: str) -> bool:
        """Convert text to speech and play it."""
        if not self._is_initialized or not self._voice_settings['voice_enabled']:
            return False

        if not VOICE_AVAILABLE:
            print(f"[Voice] Speaking: {text}")
            return True

        try:
            self._engine.say(text)
            self._engine.runAndWait()
            return True
        except Exception as e:
            print(f"[Voice] Speech synthesis error: {e}")
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
        
        if VOICE_AVAILABLE and self._engine:
            if 'speed' in settings:
                self._engine.setProperty('rate', int(200 * settings['speed']))
            if 'volume' in settings:
                self._engine.setProperty('volume', settings['volume'])
            if 'voice_id' in settings and settings['voice_id']:
                self._engine.setProperty('voice', settings['voice_id'])

    def get_voice_settings(self) -> dict:
        """Get current voice settings."""
        return self._voice_settings.copy()

    def start_continuous_listening(self) -> bool:
        """Start continuous listening mode with wake word detection."""
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
        """Continuous listening loop with wake word detection."""
        while self._is_listening:
            try:
                # Listen for wake word
                result = self.listen(timeout=1.0)
                if result:
                    # Check for wake word
                    if self.detect_wake_word(result):
                        self.speak("Yes, I'm listening")
                        # Listen for command
                        command = self.listen(timeout=5.0)
                        if command and self._voice_callback:
                            self._voice_callback(command)
                    else:
                        # Process as direct command
                        if self._voice_callback:
                            self._voice_callback(result)
                
                time.sleep(0.1)
            except Exception as e:
                print(f"Error in continuous listening: {e}")
                break

    def detect_wake_word(self, audio_data: bytes) -> bool:
        """Detect if wake word was spoken in audio data."""
        if isinstance(audio_data, str):
            text = audio_data.lower()
            wake_word = self._voice_settings['wake_word'].lower()
            return wake_word in text
        return False

    def process_voice_command(self, command: str) -> Dict[str, any]:
        """Process voice commands and return structured data."""
        command = command.lower().strip()
        
        # Define command patterns
        patterns = {
            'search': r'(search|find|look up)\s+(.+)',
            'weather': r'(weather|temperature)\s+(.+)',
            'time': r'(time|what time)',
            'date': r'(date|what date)',
            'joke': r'(joke|tell joke)',
            'music': r'(play|start)\s+(.+)',
            'volume': r'(volume|speaker)\s+(up|down|mute)',
            'help': r'(help|what can you do)',
        }
        
        result = {
            'command': 'unknown',
            'parameters': {},
            'confidence': 0.0,
            'raw_text': command
        }
        
        for cmd_type, pattern in patterns.items():
            match = re.search(pattern, command)
            if match:
                result['command'] = cmd_type
                result['confidence'] = 0.8
                if len(match.groups()) > 1:
                    result['parameters']['query'] = match.group(2)
                break
        
        return result

    def get_available_voices(self) -> List[Dict[str, str]]:
        """Get list of available voice options."""
        if not VOICE_AVAILABLE or not self._engine:
            return []
        
        try:
            voices = self._engine.getProperty('voices')
            return [
                {
                    'id': voice.id,
                    'name': voice.name,
                    'languages': voice.languages,
                    'gender': voice.gender,
                    'age': voice.age
                }
                for voice in voices
            ]
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []

    def set_voice(self, voice_id: str) -> bool:
        """Set specific voice for text-to-speech."""
        if not VOICE_AVAILABLE or not self._engine:
            return False
        
        try:
            self._engine.setProperty('voice', voice_id)
            self._voice_settings['voice_id'] = voice_id
            return True
        except Exception as e:
            print(f"Error setting voice: {e}")
            return False

    def get_voice_status(self) -> Dict[str, any]:
        """Get current voice interface status."""
        return {
            'initialized': self._is_initialized,
            'listening': self._is_listening,
            'voice_available': VOICE_AVAILABLE,
            'settings': self._voice_settings,
            'session_active': self._current_session is not None
        }

    def calibrate_microphone(self) -> Dict[str, any]:
        """Calibrate microphone for optimal performance."""
        if not VOICE_AVAILABLE or not self._microphone:
            return {'success': False, 'error': 'Voice not available'}
        
        try:
            with self._microphone as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=2)
                energy_threshold = self._recognizer.energy_threshold
                
                return {
                    'success': True,
                    'energy_threshold': energy_threshold,
                    'message': 'Microphone calibrated successfully'
                }
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def start_voice_session(self) -> bool:
        """Start a voice interaction session."""
        if self._current_session:
            return False
        
        self._current_session = {
            'start_time': time.time(),
            'commands': [],
            'responses': []
        }
        return True

    def end_voice_session(self) -> bool:
        """End the current voice interaction session."""
        if not self._current_session:
            return False
        
        session_data = self._current_session
        self._current_session = None
        return True

    def simulate_voice_input(self, text: str) -> bool:
        """Simulate voice input for testing purposes."""
        if self._voice_callback:
            self._voice_callback(text)
            return True
        return False

# Alias for backward compatibility
SimpleVoiceInterface = AdvancedVoiceInterface