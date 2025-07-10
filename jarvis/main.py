"""
JARVIS Next-Gen AI Personal Assistant
Main entry point for Phase 2 prototype.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from jarvis.modules.interaction_cli import CLIInteraction
from jarvis.modules.context_memory import MemoryContextEngine
from jarvis.modules.research_web import WebResearch
from jarvis.modules.selfmod_sandbox import SandboxSelfMod
from jarvis.modules.storage_encrypted import EncryptedStorage
from jarvis.modules.voice_simple import SimpleVoiceInterface
from jarvis.modules.plugin_manager import PluginManager
from jarvis.modules.cloud_local import LocalCloudStorage

USER_ID = 'default_user'  # For Phase 2, single user

class JARVISPhase2:
    def __init__(self):
        # Initialize core modules
        self.interaction = CLIInteraction()
        self.context_engine = MemoryContextEngine()
        self.research = WebResearch()
        self.selfmod = SandboxSelfMod()
        self.storage = EncryptedStorage()
        
        # Phase 2: New modules
        self.voice = SimpleVoiceInterface()
        self.plugin_manager = PluginManager()
        self.cloud_storage = LocalCloudStorage()
        
        # Initialize Phase 2 features
        self._initialize_phase2()

    def _initialize_phase2(self):
        """Initialize Phase 2 features."""
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

        # Set up voice callback
        self.voice.set_voice_callback(self._handle_voice_input)

    def _handle_voice_input(self, text: str):
        """Handle voice input from the voice interface."""
        self.interaction.send_message(f"[Voice] Heard: {text}")
        self._process_input(text)

    def _process_input(self, user_input: str):
        """Process user input with Phase 2 enhancements."""
        # Store user input in context
        context = self.context_engine.retrieve_context(USER_ID)
        context['last_input'] = user_input
        self.context_engine.store_context(USER_ID, context)

        # Phase 2: User intent anticipation
        anticipations = self.context_engine.anticipate_user_intent(USER_ID, user_input)
        
        # Phase 2: Enhanced research with deep analysis
        analysis = None # Initialize analysis to None
        if any(word in user_input.lower() for word in ['research', 'search', 'find', 'what is']):
            # Deep analysis for research queries
            analysis = self.research.deep_analysis(user_input, context)
            summary = self.research.synthesize_information([analysis])
        else:
            # Regular search for other queries
            results = self.research.search(user_input)
            summary = self.research.summarize(results)

        # Store enhanced context
        context['last_summary'] = summary
        context['last_analysis'] = analysis if analysis else None
        self.context_engine.store_context(USER_ID, context)

        # Add conversation entry for pattern analysis
        self.context_engine.add_conversation_entry(USER_ID, user_input, summary)

        # Phase 2: Plugin system integration
        if user_input.startswith('/plugin'):
            self._handle_plugin_command(user_input)
            return

        # Phase 2: Cloud sync commands
        if user_input.startswith('/sync'):
            self._handle_sync_command(user_input)
            return

        # Respond to user
        response = summary
        
        # Add anticipations if available
        if anticipations:
            response += "\n\n💡 Suggestions:\n"
            for anticipation in anticipations:
                response += f"• {anticipation}\n"

        self.interaction.send_message(response)

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

    def run(self):
        """Main application loop."""
        self.interaction.send_message("🚀 Welcome to JARVIS AI Assistant (Phase 2)")
        self.interaction.send_message("New features: Voice interface, plugins, cloud sync, enhanced research")
        self.interaction.send_message("Commands: /plugin, /sync, 'exit' to quit")
        
        while True:
            user_input = self.interaction.get_user_input()
            if user_input.lower() in {"exit", "quit"}:
                self.interaction.send_message("Goodbye!")
                break
            
            self._process_input(user_input)

def main():
    jarvis = JARVISPhase2()
    jarvis.run()

if __name__ == "__main__":
    main()