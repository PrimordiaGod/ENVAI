from jarvis.interfaces.plugin import PluginManagerInterface, PluginInterface
from typing import Dict, List, Optional, Any
import importlib
import os
import json

class PluginManager(PluginManagerInterface):
    def __init__(self):
        self._plugins = {}
        self._plugin_contexts = {}
        self._plugin_directory = "plugins"

    def register_plugin(self, plugin: PluginInterface) -> bool:
        """Register a new plugin."""
        try:
            plugin_info = plugin.get_plugin_info()
            plugin_name = plugin_info.get('name', 'unknown')
            
            if plugin_name in self._plugins:
                print(f"Plugin {plugin_name} is already registered")
                return False
            
            # Initialize plugin with context
            context = {
                'plugin_manager': self,
                'plugin_directory': self._plugin_directory
            }
            
            if plugin.initialize(context):
                self._plugins[plugin_name] = plugin
                self._plugin_contexts[plugin_name] = context
                print(f"Plugin {plugin_name} registered successfully")
                return True
            else:
                print(f"Failed to initialize plugin {plugin_name}")
                return False
                
        except Exception as e:
            print(f"Error registering plugin: {e}")
            return False

    def unregister_plugin(self, plugin_name: str) -> bool:
        """Unregister a plugin."""
        if plugin_name in self._plugins:
            try:
                plugin = self._plugins[plugin_name]
                plugin.cleanup()
                del self._plugins[plugin_name]
                del self._plugin_contexts[plugin_name]
                print(f"Plugin {plugin_name} unregistered successfully")
                return True
            except Exception as e:
                print(f"Error unregistering plugin {plugin_name}: {e}")
                return False
        return False

    def get_plugin(self, plugin_name: str) -> Optional[PluginInterface]:
        """Get a plugin by name."""
        return self._plugins.get(plugin_name)

    def list_plugins(self) -> List[dict]:
        """List all registered plugins."""
        plugin_list = []
        for name, plugin in self._plugins.items():
            try:
                info = plugin.get_plugin_info()
                info['commands'] = plugin.get_available_commands()
                plugin_list.append(info)
            except Exception as e:
                plugin_list.append({
                    'name': name,
                    'error': str(e)
                })
        return plugin_list

    def execute_plugin_command(self, plugin_name: str, command: str, parameters: dict = None) -> dict:
        """Execute a command on a specific plugin."""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return {'error': f'Plugin {plugin_name} not found'}
        
        try:
            if command not in plugin.get_available_commands():
                return {'error': f'Command {command} not available in plugin {plugin_name}'}
            
            result = plugin.execute(command, parameters or {})
            return result
        except Exception as e:
            return {'error': f'Error executing command {command} in plugin {plugin_name}: {e}'}

    def get_all_commands(self) -> Dict[str, List[str]]:
        """Get all available commands from all plugins."""
        commands = {}
        for name, plugin in self._plugins.items():
            try:
                commands[name] = plugin.get_available_commands()
            except Exception as e:
                commands[name] = [f'error: {e}']
        return commands

    def load_plugins_from_directory(self, directory: str = None) -> int:
        """Load plugins from a directory."""
        if directory is None:
            directory = self._plugin_directory
        
        if not os.path.exists(directory):
            print(f"Plugin directory {directory} does not exist")
            return 0
        
        loaded_count = 0
        for filename in os.listdir(directory):
            if filename.endswith('.py') and not filename.startswith('__'):
                plugin_name = filename[:-3]
                try:
                    # Import the plugin module
                    module_path = f"{directory}.{plugin_name}"
                    module = importlib.import_module(module_path)
                    
                    # Look for a class that implements PluginInterface
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if (isinstance(attr, type) and 
                            issubclass(attr, PluginInterface) and 
                            attr != PluginInterface):
                            plugin_instance = attr()
                            if self.register_plugin(plugin_instance):
                                loaded_count += 1
                            break
                            
                except Exception as e:
                    print(f"Error loading plugin {plugin_name}: {e}")
        
        return loaded_count

    def save_plugin_config(self, filename: str = "plugin_config.json") -> bool:
        """Save plugin configuration to file."""
        try:
            config = {
                'plugins': self.list_plugins(),
                'commands': self.get_all_commands()
            }
            with open(filename, 'w') as f:
                json.dump(config, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving plugin config: {e}")
            return False

    def load_plugin_config(self, filename: str = "plugin_config.json") -> bool:
        """Load plugin configuration from file."""
        try:
            if not os.path.exists(filename):
                return False
            
            with open(filename, 'r') as f:
                config = json.load(f)
            
            # Apply configuration (in future phases, this could restore plugin states)
            print(f"Loaded plugin configuration with {len(config.get('plugins', []))} plugins")
            return True
        except Exception as e:
            print(f"Error loading plugin config: {e}")
            return False