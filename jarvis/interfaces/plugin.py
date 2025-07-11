from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Callable

class PluginInterface(ABC):
    @abstractmethod
    def get_plugin_info(self) -> dict:
        """Return plugin metadata (name, version, description, etc.)."""
        pass

    @abstractmethod
    def initialize(self, context: dict) -> bool:
        """Initialize the plugin with context."""
        pass

    @abstractmethod
    def execute(self, command: str, parameters: dict = None) -> dict:
        """Execute a plugin command."""
        pass

    @abstractmethod
    def get_available_commands(self) -> List[str]:
        """Return list of available commands for this plugin."""
        pass

    @abstractmethod
    def cleanup(self) -> None:
        """Clean up plugin resources."""
        pass

class PluginManagerInterface(ABC):
    @abstractmethod
    def register_plugin(self, plugin: PluginInterface) -> bool:
        """Register a new plugin."""
        pass

    @abstractmethod
    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin."""
        pass

    @abstractmethod
    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """Get a plugin by name."""
        pass

    @abstractmethod
    def list_plugins(self) -> List[dict]:
        """List all registered plugins."""
        pass

    @abstractmethod
    def execute_plugin_command(self, plugin_name: str, command: str, parameters: dict = None) -> dict:
        """Execute a command on a specific plugin."""
        pass

    @abstractmethod
    def get_all_commands(self) -> Dict[str, List[str]]:
        """Get all available commands from all plugins."""
        pass