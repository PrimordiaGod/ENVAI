"""
JARVIS Next-Gen AI Personal Assistant
Main entry point for Phase 3 prototype.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jarvis.modules.interaction_cli import CLIInteraction
from jarvis.modules.context_memory import MemoryContextEngine
from jarvis.modules.research_web import WebResearch
from jarvis.modules.selfmod_sandbox import SandboxSelfMod
from jarvis.modules.storage_encrypted import EncryptedStorage
from jarvis.modules.voice_simple import AdvancedVoiceInterface
from jarvis.modules.plugin_manager import PluginManager
from jarvis.modules.cloud_local import LocalCloudStorage
from jarvis.modules.ai_model_openai import OpenAIInterface
from jarvis.modules.smart_home_hub import SmartHomeHub
from jarvis.emotional_intelligence.emotional_coordinator import EmotionalIntelligenceCoordinator

USER_ID = 'default_user'  # For Phase 3, single user

class JARVISPhase3:
    def __init__(self):
        # Initialize core modules
        self.interaction = CLIInteraction()
        self.context_engine = MemoryContextEngine()
        self.research = WebResearch()
        self.selfmod = SandboxSelfMod()
        self.storage = EncryptedStorage()
        
        # Phase 2: Enhanced modules
        self.voice = AdvancedVoiceInterface()
        self.plugin_manager = PluginManager()
        self.cloud_storage = LocalCloudStorage()
        
        # Phase 3: New modules
        self.ai_model = OpenAIInterface()
        self.smart_home = SmartHomeHub()
        
        # Phase 4: Emotional Intelligence
        self.emotional_coordinator = EmotionalIntelligenceCoordinator()
        
        # Initialize Phase 3 features
        self._initialize_phase3()

    def _initialize_phase3(self):
        """Initialize Phase 3 features."""
        # Initialize voice interface
        if self.voice.initialize():
            self.interaction.send_message("✅ Voice interface initialized")
        else:
            self.interaction.send_message("⚠️ Voice interface not available")

        # Initialize cloud storage
        cloud_config = {'local_mode': True}
        if self.cloud_storage.initialize(cloud_config):
            self.interaction.send_message("✅ Cloud storage initialized")
        else:
            self.interaction.send_message("⚠️ Cloud storage not available")

        # Initialize AI model
        ai_config = {'api_key': os.getenv('OPENAI_API_KEY', '')}
        if self.ai_model.initialize(ai_config):
            self.interaction.send_message("✅ AI model interface initialized")
        else:
            self.interaction.send_message("⚠️ AI model interface not available (using fallback)")

        # Initialize smart home hub
        smart_home_config = {'auto_discover': True}
        if self.smart_home.initialize(smart_home_config):
            self.interaction.send_message("✅ Smart home hub initialized")
        else:
            self.interaction.send_message("⚠️ Smart home hub not available")

        # Initialize emotional intelligence
        self.interaction.send_message("🧠 Emotional intelligence system initialized")
        self.interaction.send_message("💙 Advanced memory architecture and personality adaptation active")

        # Set up voice callback
        self.voice.set_voice_callback(self._handle_voice_input)

    def _handle_voice_input(self, text: str):
        """Handle voice input from the voice interface."""
        self.interaction.send_message(f"[Voice] Heard: {text}")
        self._process_input(text)

    async def _process_input(self, user_input: str):
        """Process user input with Phase 3 enhancements."""
        # Phase 4: Emotional intelligence processing
        emotional_result = await self.emotional_coordinator.process_interaction(user_input)
        
        # Store user input in context
        context = self.context_engine.retrieve_context(USER_ID)
        context['last_input'] = user_input
        context['emotional_context'] = emotional_result['emotional_context']
        self.context_engine.store_context(USER_ID, context)

        # Phase 3: AI-powered intent extraction
        intent_analysis = self.ai_model.extract_intent(user_input)
        
        # Phase 3: Smart home voice control
        if intent_analysis.get('intent') == 'command':
            smart_home_result = self.smart_home.voice_control(user_input)
            if smart_home_result['success']:
                self.interaction.send_message(f"🏠 {smart_home_result['message']}")
                return

        # Phase 3: AI-powered response generation
        if self.ai_model.is_available():
            # Generate AI response
            ai_response = self.ai_model.generate_response(user_input, context)
            if ai_response.confidence > 0.7:
                response = ai_response.text
            else:
                # Fallback to research
                response = self._fallback_research(user_input, context)
        else:
            # Fallback to research
            response = self._fallback_research(user_input, context)

        # Phase 2: User intent anticipation
        anticipations = self.context_engine.anticipate_user_intent(USER_ID, user_input)
        
        # Store enhanced context
        context['last_response'] = response
        context['last_intent'] = intent_analysis
        self.context_engine.store_context(USER_ID, context)

        # Add conversation entry for pattern analysis
        self.context_engine.add_conversation_entry(USER_ID, user_input, response)

        # Phase 2: Plugin system integration
        if user_input.startswith('/plugin'):
            self._handle_plugin_command(user_input)
            return

        # Phase 2: Cloud sync commands
        if user_input.startswith('/sync'):
            self._handle_sync_command(user_input)
            return

        # Phase 3: Smart home commands
        if user_input.startswith('/home'):
            self._handle_smart_home_command(user_input)
            return

        # Phase 3: AI model commands
        if user_input.startswith('/ai'):
            self._handle_ai_command(user_input)
            return

        # Phase 4: Emotional intelligence commands
        if user_input.startswith('/emotional'):
            self._handle_emotional_command(user_input)
            return

        # Phase 4: Apply emotional intelligence to response
        emotional_context = emotional_result['emotional_context']
        communication_style = emotional_result['communication_style']
        response_template = emotional_result['response_template']
        
        # Adapt response based on emotional context
        if emotional_context['emotion'] != 'neutral':
            final_response = f"{response_template}\n\n{response}"
        else:
            final_response = response
        
        # Add anticipations if available
        if anticipations:
            final_response += "\n\n💡 Suggestions:\n"
            for anticipation in anticipations:
                final_response += f"• {anticipation}\n"

        # Add emotional rapport indicator
        rapport_score = emotional_result['rapport_score']
        if rapport_score > 0.8:
            final_response += f"\n💙 Emotional rapport: Excellent ({rapport_score:.2f})"
        elif rapport_score > 0.6:
            final_response += f"\n💙 Emotional rapport: Good ({rapport_score:.2f})"

        self.interaction.send_message(final_response)

    def _fallback_research(self, user_input: str, context: dict) -> str:
        """Fallback research when AI model is not available."""
        # Phase 2: Enhanced research with deep analysis
        analysis = None
        if any(word in user_input.lower() for word in ['research', 'search', 'find', 'what is']):
            # Deep analysis for research queries
            analysis = self.research.deep_analysis(user_input, context)
            summary = self.research.synthesize_information([analysis])
        else:
            # Regular search for other queries
            results = self.research.search(user_input)
            summary = self.research.summarize(results)
        
        return summary

    def _handle_plugin_command(self, command: str):
        """Handle plugin-related commands."""
        parts = command.split()
        if len(parts) < 2:
            self.interaction.send_message("Usage: /plugin <list|info|execute> [plugin_name] [command]")
            return

        action = parts[1]
        
        if action == 'list':
            plugins = self.plugin_manager.list_plugins()
            if plugins:
                response = "📦 Available plugins:\n"
                for plugin in plugins:
                    response += f"• {plugin.get('name', 'Unknown')}: {plugin.get('description', 'No description')}\n"
            else:
                response = "No plugins available"
            self.interaction.send_message(response)

        elif action == 'info' and len(parts) > 2:
            plugin_name = parts[2]
            plugin = self.plugin_manager.get_plugin(plugin_name)
            if plugin:
                info = plugin.get_plugin_info()
                commands = plugin.get_available_commands()
                response = f"📦 Plugin: {info.get('name', 'Unknown')}\n"
                response += f"Version: {info.get('version', 'Unknown')}\n"
                response += f"Description: {info.get('description', 'No description')}\n"
                response += f"Commands: {', '.join(commands)}"
            else:
                response = f"Plugin '{plugin_name}' not found"
            self.interaction.send_message(response)

        elif action == 'execute' and len(parts) > 3:
            plugin_name = parts[2]
            plugin_command = parts[3]
            result = self.plugin_manager.execute_plugin_command(plugin_name, plugin_command)
            self.interaction.send_message(f"Plugin result: {result}")

    def _handle_sync_command(self, command: str):
        """Handle cloud sync commands."""
        parts = command.split()
        if len(parts) < 2:
            self.interaction.send_message("Usage: /sync <to|from|status>")
            return

        action = parts[1]
        
        if action == 'to':
            # Sync local data to cloud
            local_data = {
                'context': self.context_engine.retrieve_context(USER_ID),
                'preferences': self.context_engine.get_user_preferences(USER_ID)
            }
            if self.cloud_storage.sync_to_cloud(local_data):
                self.interaction.send_message("✅ Data synced to cloud")
            else:
                self.interaction.send_message("❌ Failed to sync to cloud")

        elif action == 'from':
            # Sync data from cloud
            cloud_data = self.cloud_storage.sync_from_cloud()
            if cloud_data:
                self.interaction.send_message(f"✅ Synced {len(cloud_data)} items from cloud")
            else:
                self.interaction.send_message("❌ Failed to sync from cloud")

        elif action == 'status':
            # Show sync status
            status = self.cloud_storage.get_sync_status()
            response = f"🔄 Sync Status:\n"
            response += f"Last sync: {status.get('last_sync', 'Never')}\n"
            response += f"Total syncs: {status.get('sync_count', 0)}\n"
            response += f"Errors: {len(status.get('errors', []))}"
            self.interaction.send_message(response)

    def _handle_smart_home_command(self, command: str):
        """Handle smart home commands."""
        parts = command.split()
        if len(parts) < 2:
            self.interaction.send_message("Usage: /home <devices|status|control|scenes|energy> [parameters]")
            return

        action = parts[1]
        
        if action == 'devices':
            devices = self.smart_home.discover_devices()
            response = "🏠 Smart Home Devices:\n"
            for device in devices:
                status = "🟢" if device.properties.get('power', False) else "🔴"
                response += f"{status} {device.name} ({device.type.value})\n"
            self.interaction.send_message(response)

        elif action == 'status':
            status = self.smart_home.get_system_status()
            response = f"🏠 Smart Home Status:\n"
            response += f"Total devices: {status['total_devices']}\n"
            response += f"Online devices: {status['online_devices']}\n"
            response += f"Powered devices: {status['powered_devices']}\n"
            response += f"System health: {status['system_health']}"
            self.interaction.send_message(response)

        elif action == 'control' and len(parts) > 3:
            device_id = parts[2]
            control_action = parts[3]
            success = self.smart_home.control_device(device_id, control_action)
            if success:
                self.interaction.send_message(f"✅ {device_id}: {control_action} executed")
            else:
                self.interaction.send_message(f"❌ Failed to {control_action} {device_id}")

        elif action == 'scenes':
            scenes = self.smart_home.get_scenes()
            response = "🎭 Available Scenes:\n"
            for scene in scenes:
                response += f"• {scene['name']}: {scene['description']}\n"
            self.interaction.send_message(response)

        elif action == 'energy':
            energy = self.smart_home.get_energy_usage()
            response = f"⚡ Energy Usage:\n"
            response += f"Devices on: {energy['total_devices_on']}\n"
            response += f"Power consumption: {energy['total_power_consumption']}W\n"
            response += f"Daily usage: {energy['daily_usage']:.1f} kWh\n"
            response += f"Monthly cost: ${energy['estimated_cost']:.2f}"
            self.interaction.send_message(response)

    def _handle_ai_command(self, command: str):
        """Handle AI model commands."""
        parts = command.split()
        if len(parts) < 2:
            self.interaction.send_message("Usage: /ai <status|model|sentiment|summarize> [parameters]")
            return

        action = parts[1]
        
        if action == 'status':
            model_info = self.ai_model.get_model_info()
            usage_stats = self.ai_model.get_usage_stats()
            response = f"🤖 AI Model Status:\n"
            response += f"Model: {model_info['name']}\n"
            response += f"Provider: {model_info['provider']}\n"
            response += f"Available: {'Yes' if model_info['available'] else 'No'}\n"
            response += f"Total requests: {usage_stats['total_requests']}\n"
            response += f"Total tokens: {usage_stats['total_tokens']}"
            self.interaction.send_message(response)

        elif action == 'model' and len(parts) > 2:
            model_name = parts[2]
            success = self.ai_model.switch_model(model_name)
            if success:
                self.interaction.send_message(f"✅ Switched to model: {model_name}")
            else:
                self.interaction.send_message(f"❌ Failed to switch to model: {model_name}")

        elif action == 'sentiment' and len(parts) > 2:
            text = ' '.join(parts[2:])
            sentiment = self.ai_model.analyze_sentiment(text)
            response = f"😊 Sentiment Analysis:\n"
            response += f"Sentiment: {sentiment['sentiment']}\n"
            response += f"Confidence: {sentiment['confidence']:.2f}\n"
            response += f"Score: {sentiment['score']:.2f}"
            self.interaction.send_message(response)

        elif action == 'summarize' and len(parts) > 2:
            text = ' '.join(parts[2:])
            summary = self.ai_model.summarize_text(text)
            response = f"📝 Summary:\n{summary}"
            self.interaction.send_message(response)

    async def _handle_emotional_command(self, command: str):
        """Handle emotional intelligence commands."""
        parts = command.split()
        if len(parts) < 2:
            self.interaction.send_message("Usage: /emotional <insights|memory|personality|learning|rapport> [parameters]")
            return

        action = parts[1]
        
        if action == 'insights':
            insights = await self.emotional_coordinator.get_emotional_insights()
            response = f"🧠 Emotional Intelligence Insights:\n"
            response += f"Dominant emotion: {insights['emotional_patterns']['dominant_emotion']}\n"
            response += f"Average intensity: {insights['emotional_patterns']['average_intensity']:.2f}\n"
            response += f"Rapport score: {insights['rapport_metrics']['current_score']:.2f}\n"
            response += f"Adaptation success rate: {insights['learning_metrics']['adaptation_success_rate']:.2f}\n"
            response += f"Total memories: {insights['memory_insights']['total_memories']}"
            self.interaction.send_message(response)

        elif action == 'memory':
            memory_data = self.emotional_coordinator.emotional_memory.export_memory_data()
            response = f"💾 Emotional Memory Status:\n"
            response += f"Total memories: {memory_data['total_memories']}\n"
            response += f"Memory types: {len(memory_data['memory_types'])}\n"
            response += f"Learning moments: {memory_data['learning_moments']}\n"
            response += f"Patterns identified: {len(memory_data['patterns'])}"
            self.interaction.send_message(response)

        elif action == 'personality':
            personality_data = self.emotional_coordinator.personality_engine.export_personality_data()
            response = f"🎭 Personality Profile:\n"
            response += f"Communication style: {personality_data['personality_summary']['communication_style']}\n"
            response += f"Adaptation history: {personality_data['adaptation_history']}\n"
            response += f"Learning moments: {personality_data['learning_moments']}\n"
            response += f"Adaptation suggestions: {len(personality_data['emotional_adaptation_suggestions'])}"
            self.interaction.send_message(response)

        elif action == 'learning':
            learning_report = await self.emotional_coordinator.get_continuous_learning_report()
            response = f"📚 Continuous Learning Report:\n"
            response += f"Learning sessions: {learning_report['total_learning_sessions']}\n"
            response += f"Success rate: {learning_report['success_rate']:.2f}\n"
            response += f"Positive outcomes: {learning_report['positive_learning_outcomes']}\n"
            response += f"Negative outcomes: {learning_report['negative_learning_outcomes']}"
            self.interaction.send_message(response)

        elif action == 'rapport':
            rapport_metrics = self.emotional_coordinator.rapport_metrics
            response = f"💙 Rapport Metrics:\n"
            response += f"Current score: {rapport_metrics.get('current_score', 0):.2f}\n"
            response += f"Emotional alignment: {rapport_metrics.get('emotional_alignment', 0):.2f}\n"
            response += f"Memory relevance: {rapport_metrics.get('memory_relevance', 0):.2f}\n"
            response += f"Learning engagement: {rapport_metrics.get('learning_engagement', 0):.2f}\n"
            response += f"Total interactions: {rapport_metrics.get('total_interactions', 0)}"
            self.interaction.send_message(response)

    async def run(self):
        """Main application loop."""
        self.interaction.send_message("🚀 Welcome to JARVIS AI Assistant (Phase 4)")
        self.interaction.send_message("New features: Real voice, AI models, smart home, emotional intelligence")
        self.interaction.send_message("Commands: /plugin, /sync, /home, /ai, /emotional, 'exit' to quit")
        
        while True:
            user_input = self.interaction.get_user_input()
            if user_input.lower() in {"exit", "quit"}:
                self.interaction.send_message("Goodbye!")
                break
            
            await self._process_input(user_input)

if __name__ == "__main__":
    import asyncio
    jarvis = JARVISPhase3()
    asyncio.run(jarvis.run())