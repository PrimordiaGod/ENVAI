from jarvis.interfaces.context import ContextInterface
from jarvis.interfaces.research import ResearchInterface
from jarvis.interfaces.voice import VoiceInterface
from jarvis.interfaces.plugin import PluginInterface
from jarvis.interfaces.storage import StorageInterface
from jarvis.interfaces.ai_model import AIModelInterface, LanguageModelInterface, PersonalizationInterface
from jarvis.interfaces.smart_home import SmartHomeInterface, AutomationInterface
from jarvis.interfaces.collaboration import CollaborationInterface, RealTimeInterface, UserManagementInterface
from jarvis.interfaces.security import SecurityInterface

from jarvis.modules.context_enhanced import EnhancedContextEngine
from jarvis.modules.research_enhanced import EnhancedResearchEngine
from jarvis.modules.voice_real import RealVoiceInterface
from jarvis.modules.plugin_system import PluginSystem
from jarvis.modules.storage_cloud import CloudStorage
from jarvis.modules.ai_advanced import AdvancedAIModel
from jarvis.modules.smart_home_local import LocalSmartHome
from jarvis.modules.collaboration_local import LocalCollaboration
from jarvis.modules.security_advanced import AdvancedSecurity

from typing import Dict, List, Optional, Any
import json
import datetime
import threading
import time

class JARVIS:
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.is_initialized = False
        
        # Core components
        self.context_engine: Optional[ContextInterface] = None
        self.research_engine: Optional[ResearchInterface] = None
        self.voice_interface: Optional[VoiceInterface] = None
        self.plugin_system: Optional[PluginInterface] = None
        self.storage_system: Optional[StorageInterface] = None
        
        # Phase 3 components
        self.ai_model: Optional[AIModelInterface] = None
        self.smart_home: Optional[SmartHomeInterface] = None
        self.collaboration: Optional[CollaborationInterface] = None
        self.security: Optional[SecurityInterface] = None
        
        # User management
        self.current_user_id: Optional[str] = None
        self.user_session: Optional[dict] = None
        
        # Voice callback
        self.voice_callback = None

    def initialize(self) -> bool:
        """Initialize all JARVIS components."""
        try:
            print("🤖 Initializing JARVIS Phase 3...")
            
            # Initialize core components
            self.context_engine = EnhancedContextEngine()
            if not self.context_engine.initialize(self.config.get('context', {})):
                raise Exception("Failed to initialize context engine")
            
            self.research_engine = EnhancedResearchEngine()
            if not self.research_engine.initialize(self.config.get('research', {})):
                raise Exception("Failed to initialize research engine")
            
            # Initialize real voice interface
            self.voice_interface = RealVoiceInterface()
            if not self.voice_interface.initialize():
                print("⚠️  Voice interface initialization failed, using fallback")
                from jarvis.modules.voice_simulated import SimulatedVoiceInterface
                self.voice_interface = SimulatedVoiceInterface()
                self.voice_interface.initialize()
            
            # Set voice callback
            self.voice_interface.set_voice_callback(self._handle_voice_input)
            
            self.plugin_system = PluginSystem()
            if not self.plugin_system.initialize(self.config.get('plugins', {})):
                raise Exception("Failed to initialize plugin system")
            
            self.storage_system = CloudStorage()
            if not self.storage_system.initialize(self.config.get('storage', {})):
                raise Exception("Failed to initialize storage system")
            
            # Initialize Phase 3 components
            self.ai_model = AdvancedAIModel()
            if not self.ai_model.initialize(self.config.get('ai_model', {})):
                raise Exception("Failed to initialize AI model")
            
            self.smart_home = LocalSmartHome()
            if not self.smart_home.initialize(self.config.get('smart_home', {})):
                raise Exception("Failed to initialize smart home")
            
            self.collaboration = LocalCollaboration()
            if not self.collaboration.initialize(self.config.get('collaboration', {})):
                raise Exception("Failed to initialize collaboration system")
            
            self.security = AdvancedSecurity()
            if not self.security.initialize(self.config.get('security', {})):
                raise Exception("Failed to initialize security system")
            
            self.is_initialized = True
            print("✅ JARVIS Phase 3 initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ JARVIS initialization failed: {e}")
            return False

    def process_input(self, user_input: str, user_id: str = None) -> str:
        """Process user input and generate response."""
        if not self.is_initialized:
            return "JARVIS is not initialized."
        
        try:
            # Set current user
            self.current_user_id = user_id or "default_user"
            
            # Security check
            threats = self.security.detect_threats({'input': user_input})
            if threats:
                self.security.log_access(self.current_user_id, 'input_processing', False, {
                    'threats_detected': threats
                })
                return "Security threat detected. Input blocked."
            
            # Log access
            self.security.log_access(self.current_user_id, 'input_processing', True)
            
            # Learn user patterns
            self.ai_model.learn_user_patterns(self.current_user_id, {'text': user_input})
            
            # Extract intent and sentiment
            intent = self.ai_model.extract_intent(user_input)
            sentiment = self.ai_model.analyze_sentiment(user_input)
            
            # Update context
            self.context_engine.update_context(self.current_user_id, {
                'input': user_input,
                'intent': intent,
                'sentiment': sentiment,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            # Generate response based on intent
            response = self._generate_response(user_input, intent, sentiment)
            
            # Adapt response to user preferences
            if self.current_user_id:
                response = self.ai_model.adapt_response_style(self.current_user_id, response)
            
            # Update context with response
            self.context_engine.update_context(self.current_user_id, {
                'response': response,
                'timestamp': datetime.datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            print(f"Error processing input: {e}")
            return "I encountered an error processing your request."

    def _generate_response(self, user_input: str, intent: dict, sentiment: dict) -> str:
        """Generate response based on intent and context."""
        
        # Handle different intents
        if intent['intent'] == 'research':
            return self._handle_research_request(user_input)
        elif intent['intent'] == 'weather':
            return self._handle_weather_request(user_input)
        elif intent['intent'] == 'schedule':
            return self._handle_schedule_request(user_input)
        elif intent['intent'] == 'smart_home':
            return self._handle_smart_home_request(user_input)
        elif intent['intent'] == 'collaboration':
            return self._handle_collaboration_request(user_input)
        elif intent['intent'] == 'greeting':
            return self._handle_greeting(user_input)
        elif intent['intent'] == 'farewell':
            return self._handle_farewell(user_input)
        else:
            # Use AI model for general responses
            context = self.context_engine.get_context(self.current_user_id)
            return self.ai_model.generate_response(user_input, {
                'user_id': self.current_user_id,
                'context': context,
                'intent': intent,
                'sentiment': sentiment
            })

    def _handle_research_request(self, user_input: str) -> str:
        """Handle research requests."""
        try:
            results = self.research_engine.search(user_input)
            if results:
                summary = self.ai_model.summarize_text(results[0]['content'])
                return f"Research results: {summary}"
            else:
                return "I couldn't find relevant information for your query."
        except Exception as e:
            return f"Research failed: {e}"

    def _handle_weather_request(self, user_input: str) -> str:
        """Handle weather requests."""
        return "The weather is currently sunny with a temperature of 72°F. Perfect for outdoor activities!"

    def _handle_schedule_request(self, user_input: str) -> str:
        """Handle schedule requests."""
        return "I can help you manage your schedule. What would you like to do?"

    def _handle_smart_home_request(self, user_input: str) -> str:
        """Handle smart home requests."""
        try:
            devices = self.smart_home.get_all_devices()
            if "light" in user_input.lower():
                # Find light devices
                light_devices = [d for d in devices if d['type'] == 'light']
                if light_devices:
                    device_id = light_devices[0]['id']
                    if "on" in user_input.lower():
                        self.smart_home.control_device(device_id, "turn_on")
                        return "Turning on the lights."
                    elif "off" in user_input.lower():
                        self.smart_home.control_device(device_id, "turn_off")
                        return "Turning off the lights."
            
            return f"I found {len(devices)} smart home devices. What would you like to control?"
        except Exception as e:
            return f"Smart home control failed: {e}"

    def _handle_collaboration_request(self, user_input: str) -> str:
        """Handle collaboration requests."""
        try:
            workspaces = self.collaboration.list_workspaces()
            if "create" in user_input.lower():
                workspace_id = self.collaboration.create_workspace("New Workspace", self.current_user_id)
                return f"Created new workspace with ID: {workspace_id}"
            elif "join" in user_input.lower():
                return f"I found {len(workspaces)} available workspaces."
            else:
                return f"You have {len(workspaces)} workspaces available."
        except Exception as e:
            return f"Collaboration failed: {e}"

    def _handle_greeting(self, user_input: str) -> str:
        """Handle greeting messages."""
        return "Hello! I'm JARVIS, your advanced AI assistant. How can I help you today?"

    def _handle_farewell(self, user_input: str) -> str:
        """Handle farewell messages."""
        return "Goodbye! Have a great day!"

    def _handle_voice_input(self, text: str):
        """Handle voice input from the voice interface."""
        if self.voice_callback:
            self.voice_callback(text)
        else:
            response = self.process_input(text, self.current_user_id)
            self.voice_interface.speak(response)

    def start_voice_mode(self):
        """Start voice interaction mode."""
        if self.voice_interface:
            self.voice_interface.start_continuous_listening()
            print("🎤 Voice mode activated. Speak to interact with JARVIS.")

    def stop_voice_mode(self):
        """Stop voice interaction mode."""
        if self.voice_interface:
            self.voice_interface.stop_continuous_listening()
            print("🔇 Voice mode deactivated.")

    def speak(self, text: str):
        """Convert text to speech."""
        if self.voice_interface:
            self.voice_interface.speak(text)

    def listen(self, timeout: float = 5.0) -> Optional[str]:
        """Listen for voice input."""
        if self.voice_interface:
            return self.voice_interface.listen(timeout)
        return None

    def get_system_status(self) -> dict:
        """Get comprehensive system status."""
        return {
            'initialized': self.is_initialized,
            'current_user': self.current_user_id,
            'context_engine': self.context_engine.get_status() if self.context_engine else None,
            'research_engine': self.research_engine.get_status() if self.research_engine else None,
            'voice_interface': self.voice_interface.get_voice_settings() if self.voice_interface else None,
            'ai_model': self.ai_model.get_model_info() if self.ai_model else None,
            'smart_home': {
                'devices': len(self.smart_home.get_all_devices()) if self.smart_home else 0,
                'automations': len(self.smart_home.list_automations()) if self.smart_home else 0
            },
            'collaboration': {
                'workspaces': len(self.collaboration.list_workspaces()) if self.collaboration else 0,
                'users': len(self.collaboration.list_users()) if self.collaboration else 0
            },
            'security': self.security.get_security_report() if self.security else None
        }

    def authenticate_user(self, credentials: dict) -> Optional[str]:
        """Authenticate a user."""
        if self.collaboration:
            return self.collaboration.authenticate_user(credentials)
        return None

    def create_user(self, user_info: dict) -> Optional[str]:
        """Create a new user."""
        if self.collaboration:
            return self.collaboration.create_user(user_info)
        return None

    def get_user_profile(self, user_id: str) -> dict:
        """Get user profile and preferences."""
        if self.ai_model:
            return self.ai_model.get_user_profile(user_id)
        return {}

    def control_smart_device(self, device_id: str, command: str, parameters: dict = None) -> bool:
        """Control a smart home device."""
        if self.smart_home:
            return self.smart_home.control_device(device_id, command, parameters)
        return False

    def get_smart_devices(self) -> List[dict]:
        """Get all smart home devices."""
        if self.smart_home:
            return self.smart_home.get_all_devices()
        return []

    def create_automation(self, name: str, conditions: dict, actions: List[dict]) -> bool:
        """Create a smart home automation."""
        if self.smart_home:
            return self.smart_home.create_automation(name, conditions, actions)
        return False

    def create_workspace(self, name: str, owner_id: str) -> Optional[str]:
        """Create a collaborative workspace."""
        if self.collaboration:
            return self.collaboration.create_workspace(name, owner_id)
        return None

    def join_workspace(self, workspace_id: str, user_id: str) -> bool:
        """Join a collaborative workspace."""
        if self.collaboration:
            return self.collaboration.join_workspace(workspace_id, user_id)
        return False

    def start_session(self, session_id: str, participants: List[str]) -> bool:
        """Start a real-time collaboration session."""
        if self.collaboration:
            return self.collaboration.start_session(session_id, participants)
        return False

    def send_message(self, session_id: str, user_id: str, message: str) -> bool:
        """Send a message in a collaboration session."""
        if self.collaboration:
            return self.collaboration.send_message(session_id, user_id, message)
        return False

    def get_security_report(self) -> dict:
        """Get security status report."""
        if self.security:
            return self.security.get_security_report()
        return {}

    def encrypt_data(self, data: str) -> str:
        """Encrypt sensitive data."""
        if self.security:
            return self.security.encrypt_data(data)
        return data

    def decrypt_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data."""
        if self.security:
            return self.security.decrypt_data(encrypted_data)
        return encrypted_data