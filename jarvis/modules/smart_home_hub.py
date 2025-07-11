from jarvis.interfaces.smart_home import SmartHomeInterface, SmartDevice, DeviceType, DeviceStatus
from typing import Dict, List, Optional, Any
import json
import time
import re
import uuid
from datetime import datetime, timedelta
import threading

class SmartHomeHub(SmartHomeInterface):
    """Smart home hub implementation with device management and automation."""
    
    def __init__(self):
        self._is_initialized = False
        self._devices: Dict[str, SmartDevice] = {}
        self._automations: Dict[str, Dict[str, Any]] = {}
        self._scenes: Dict[str, Dict[str, Any]] = {}
        self._schedules: Dict[str, Dict[str, Any]] = {}
        self._rooms: Dict[str, List[str]] = {}
        self._voice_patterns = self._initialize_voice_patterns()

    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the smart home hub."""
        try:
            # Load default configuration
            self._load_default_config()
            
            # Initialize rooms
            self._rooms = {
                'living_room': ['light_1', 'light_2', 'tv', 'thermostat'],
                'bedroom': ['light_3', 'fan', 'thermostat'],
                'kitchen': ['light_4', 'microwave', 'refrigerator'],
                'bathroom': ['light_5', 'fan'],
                'office': ['light_6', 'computer', 'printer']
            }
            
            # Initialize default scenes
            self._scenes = {
                'movie_mode': {
                    'description': 'Dim lights and prepare for movie watching',
                    'actions': [
                        {'device_id': 'light_1', 'action': 'dim', 'parameters': {'level': 20}},
                        {'device_id': 'light_2', 'action': 'dim', 'parameters': {'level': 20}},
                        {'device_id': 'tv', 'action': 'turn_on', 'parameters': {}}
                    ]
                },
                'sleep_mode': {
                    'description': 'Prepare for sleep - dim lights and set thermostat',
                    'actions': [
                        {'device_id': 'light_3', 'action': 'dim', 'parameters': {'level': 10}},
                        {'device_id': 'thermostat', 'action': 'set_temperature', 'parameters': {'temperature': 68}}
                    ]
                },
                'morning_mode': {
                    'description': 'Morning routine - bright lights and warm temperature',
                    'actions': [
                        {'device_id': 'light_1', 'action': 'turn_on', 'parameters': {'brightness': 100}},
                        {'device_id': 'light_2', 'action': 'turn_on', 'parameters': {'brightness': 100}},
                        {'device_id': 'thermostat', 'action': 'set_temperature', 'parameters': {'temperature': 72}}
                    ]
                }
            }
            
            self._is_initialized = True
            print("✅ Smart home hub initialized successfully")
            return True
            
        except Exception as e:
            print(f"❌ Smart home hub initialization failed: {e}")
            return False

    def _load_default_config(self):
        """Load default device configuration."""
        default_devices = [
            {
                'id': 'light_1', 'name': 'Living Room Light 1', 'type': DeviceType.LIGHT,
                'capabilities': ['turn_on', 'turn_off', 'dim', 'set_brightness'],
                'properties': {'brightness': 100, 'color': 'white', 'power': False},
                'location': 'living_room', 'manufacturer': 'Philips', 'model': 'Hue'
            },
            {
                'id': 'light_2', 'name': 'Living Room Light 2', 'type': DeviceType.LIGHT,
                'capabilities': ['turn_on', 'turn_off', 'dim', 'set_brightness'],
                'properties': {'brightness': 100, 'color': 'white', 'power': False},
                'location': 'living_room', 'manufacturer': 'Philips', 'model': 'Hue'
            },
            {
                'id': 'light_3', 'name': 'Bedroom Light', 'type': DeviceType.LIGHT,
                'capabilities': ['turn_on', 'turn_off', 'dim', 'set_brightness'],
                'properties': {'brightness': 100, 'color': 'white', 'power': False},
                'location': 'bedroom', 'manufacturer': 'Philips', 'model': 'Hue'
            },
            {
                'id': 'thermostat', 'name': 'Main Thermostat', 'type': DeviceType.THERMOSTAT,
                'capabilities': ['set_temperature', 'set_mode', 'get_temperature'],
                'properties': {'temperature': 72, 'mode': 'heat', 'power': True},
                'location': 'living_room', 'manufacturer': 'Nest', 'model': 'Learning'
            },
            {
                'id': 'tv', 'name': 'Living Room TV', 'type': DeviceType.MEDIA,
                'capabilities': ['turn_on', 'turn_off', 'set_volume', 'change_channel'],
                'properties': {'power': False, 'volume': 50, 'channel': 1},
                'location': 'living_room', 'manufacturer': 'Samsung', 'model': 'Smart TV'
            }
        ]
        
        for device_info in default_devices:
            device = SmartDevice(
                id=device_info['id'],
                name=device_info['name'],
                type=device_info['type'],
                status=DeviceStatus.ONLINE,
                capabilities=device_info['capabilities'],
                properties=device_info['properties'],
                location=device_info['location'],
                manufacturer=device_info['manufacturer'],
                model=device_info['model']
            )
            self._devices[device_info['id']] = device

    def discover_devices(self) -> List[SmartDevice]:
        """Discover available smart home devices."""
        return list(self._devices.values())

    def get_device(self, device_id: str) -> Optional[SmartDevice]:
        """Get a specific device by ID."""
        return self._devices.get(device_id)

    def get_devices_by_type(self, device_type: DeviceType) -> List[SmartDevice]:
        """Get all devices of a specific type."""
        return [device for device in self._devices.values() if device.type == device_type]

    def control_device(self, device_id: str, action: str, parameters: Dict[str, Any] = None) -> bool:
        """Control a smart home device."""
        device = self.get_device(device_id)
        if not device:
            print(f"❌ Device {device_id} not found")
            return False
        
        if action not in device.capabilities:
            print(f"❌ Action {action} not supported by device {device_id}")
            return False
        
        try:
            # Update device properties based on action
            if action == 'turn_on':
                device.properties['power'] = True
            elif action == 'turn_off':
                device.properties['power'] = False
            elif action == 'dim':
                level = parameters.get('level', 50) if parameters else 50
                device.properties['brightness'] = level
            elif action == 'set_brightness':
                brightness = parameters.get('brightness', 100) if parameters else 100
                device.properties['brightness'] = brightness
            elif action == 'set_temperature':
                temperature = parameters.get('temperature', 72) if parameters else 72
                device.properties['temperature'] = temperature
            elif action == 'set_volume':
                volume = parameters.get('volume', 50) if parameters else 50
                device.properties['volume'] = volume
            
            print(f"✅ {device.name}: {action} executed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error controlling device {device_id}: {e}")
            return False

    def get_device_status(self, device_id: str) -> Optional[DeviceStatus]:
        """Get the status of a specific device."""
        device = self.get_device(device_id)
        return device.status if device else None

    def create_automation(self, name: str, trigger: Dict[str, Any], actions: List[Dict[str, Any]]) -> str:
        """Create a new automation rule."""
        automation_id = str(uuid.uuid4())
        
        automation = {
            'id': automation_id,
            'name': name,
            'trigger': trigger,
            'actions': actions,
            'enabled': True,
            'created_at': datetime.now().isoformat(),
            'last_triggered': None
        }
        
        self._automations[automation_id] = automation
        print(f"✅ Automation '{name}' created successfully")
        return automation_id

    def get_automations(self) -> List[Dict[str, Any]]:
        """Get all automation rules."""
        return list(self._automations.values())

    def delete_automation(self, automation_id: str) -> bool:
        """Delete an automation rule."""
        if automation_id in self._automations:
            del self._automations[automation_id]
            print(f"✅ Automation {automation_id} deleted successfully")
            return True
        return False

    def get_rooms(self) -> List[Dict[str, Any]]:
        """Get all rooms/locations."""
        return [
            {
                'name': room_name,
                'device_count': len(device_ids),
                'devices': device_ids
            }
            for room_name, device_ids in self._rooms.items()
        ]

    def get_devices_in_room(self, room_name: str) -> List[SmartDevice]:
        """Get all devices in a specific room."""
        device_ids = self._rooms.get(room_name, [])
        return [device for device_id, device in self._devices.items() if device_id in device_ids]

    def voice_control(self, command: str) -> Dict[str, Any]:
        """Process voice commands for smart home control."""
        command = command.lower().strip()
        
        result = {
            'success': False,
            'action': 'unknown',
            'device': None,
            'message': 'Command not understood'
        }
        
        # Check for device control patterns
        for pattern, handler in self._voice_patterns.items():
            match = re.search(pattern, command)
            if match:
                return handler(match, command)
        
        return result

    def _initialize_voice_patterns(self) -> Dict[str, callable]:
        """Initialize voice command patterns."""
        return {
            r'turn on (.+)': self._handle_turn_on,
            r'turn off (.+)': self._handle_turn_off,
            r'dim (.+)': self._handle_dim,
            r'set (.+) to (.+)': self._handle_set_value,
            r'what is the (.+)': self._handle_status_query,
            r'show me (.+)': self._handle_status_query,
            r'activate (.+) mode': self._handle_scene,
            r'set (.+) mode': self._handle_scene
        }

    def _handle_turn_on(self, match, command: str) -> Dict[str, Any]:
        """Handle turn on commands."""
        device_name = match.group(1)
        device = self._find_device_by_name(device_name)
        
        if device:
            success = self.control_device(device.id, 'turn_on')
            return {
                'success': success,
                'action': 'turn_on',
                'device': device.name,
                'message': f"Turning on {device.name}" if success else f"Failed to turn on {device.name}"
            }
        else:
            return {
                'success': False,
                'action': 'turn_on',
                'device': device_name,
                'message': f"Device '{device_name}' not found"
            }

    def _handle_turn_off(self, match, command: str) -> Dict[str, Any]:
        """Handle turn off commands."""
        device_name = match.group(1)
        device = self._find_device_by_name(device_name)
        
        if device:
            success = self.control_device(device.id, 'turn_off')
            return {
                'success': success,
                'action': 'turn_off',
                'device': device.name,
                'message': f"Turning off {device.name}" if success else f"Failed to turn off {device.name}"
            }
        else:
            return {
                'success': False,
                'action': 'turn_off',
                'device': device_name,
                'message': f"Device '{device_name}' not found"
            }

    def _handle_dim(self, match, command: str) -> Dict[str, Any]:
        """Handle dim commands."""
        device_name = match.group(1)
        device = self._find_device_by_name(device_name)
        
        if device:
            success = self.control_device(device.id, 'dim', {'level': 50})
            return {
                'success': success,
                'action': 'dim',
                'device': device.name,
                'message': f"Dimming {device.name}" if success else f"Failed to dim {device.name}"
            }
        else:
            return {
                'success': False,
                'action': 'dim',
                'device': device_name,
                'message': f"Device '{device_name}' not found"
            }

    def _handle_set_value(self, match, command: str) -> Dict[str, Any]:
        """Handle set value commands."""
        device_name = match.group(1)
        value = match.group(2)
        device = self._find_device_by_name(device_name)
        
        if device:
            if device.type == DeviceType.THERMOSTAT:
                try:
                    temp = int(value)
                    success = self.control_device(device.id, 'set_temperature', {'temperature': temp})
                    return {
                        'success': success,
                        'action': 'set_temperature',
                        'device': device.name,
                        'message': f"Setting {device.name} to {temp} degrees" if success else f"Failed to set temperature"
                    }
                except ValueError:
                    return {
                        'success': False,
                        'action': 'set_temperature',
                        'device': device.name,
                        'message': f"Invalid temperature value: {value}"
                    }
            elif device.type == DeviceType.MEDIA:
                try:
                    volume = int(value)
                    success = self.control_device(device.id, 'set_volume', {'volume': volume})
                    return {
                        'success': success,
                        'action': 'set_volume',
                        'device': device.name,
                        'message': f"Setting {device.name} volume to {volume}" if success else f"Failed to set volume"
                    }
                except ValueError:
                    return {
                        'success': False,
                        'action': 'set_volume',
                        'device': device.name,
                        'message': f"Invalid volume value: {value}"
                    }
        
        return {
            'success': False,
            'action': 'set_value',
            'device': device_name,
            'message': f"Device '{device_name}' not found or doesn't support value setting"
        }

    def _handle_status_query(self, match, command: str) -> Dict[str, Any]:
        """Handle status query commands."""
        device_name = match.group(1)
        device = self._find_device_by_name(device_name)
        
        if device:
            status_info = f"{device.name} is {'on' if device.properties.get('power', False) else 'off'}"
            if device.type == DeviceType.THERMOSTAT:
                temp = device.properties.get('temperature', 'unknown')
                status_info += f", temperature is {temp} degrees"
            elif device.type == DeviceType.LIGHT:
                brightness = device.properties.get('brightness', 'unknown')
                status_info += f", brightness is {brightness}%"
            
            return {
                'success': True,
                'action': 'status_query',
                'device': device.name,
                'message': status_info
            }
        else:
            return {
                'success': False,
                'action': 'status_query',
                'device': device_name,
                'message': f"Device '{device_name}' not found"
            }

    def _handle_scene(self, match, command: str) -> Dict[str, Any]:
        """Handle scene activation commands."""
        scene_name = match.group(1).replace(' ', '_').lower()
        
        if scene_name in self._scenes:
            scene = self._scenes[scene_name]
            success_count = 0
            
            for action in scene['actions']:
                if self.control_device(action['device_id'], action['action'], action.get('parameters', {})):
                    success_count += 1
            
            return {
                'success': success_count > 0,
                'action': 'activate_scene',
                'device': scene_name,
                'message': f"Activated {scene_name} scene ({success_count} actions successful)"
            }
        else:
            return {
                'success': False,
                'action': 'activate_scene',
                'device': scene_name,
                'message': f"Scene '{scene_name}' not found"
            }

    def _find_device_by_name(self, name: str) -> Optional[SmartDevice]:
        """Find a device by name (fuzzy matching)."""
        name_lower = name.lower()
        
        # Exact match
        for device in self._devices.values():
            if device.name.lower() == name_lower:
                return device
        
        # Partial match
        for device in self._devices.values():
            if name_lower in device.name.lower() or device.name.lower() in name_lower:
                return device
        
        # Room-based matching
        for room_name, device_ids in self._rooms.items():
            if name_lower in room_name.lower():
                # Return first device in room
                for device_id in device_ids:
                    if device_id in self._devices:
                        return self._devices[device_id]
        
        return None

    def get_energy_usage(self, device_id: Optional[str] = None) -> Dict[str, Any]:
        """Get energy usage statistics."""
        # Simulated energy usage data
        if device_id:
            device = self.get_device(device_id)
            if device:
                return {
                    'device_id': device_id,
                    'power_consumption': 100 if device.properties.get('power', False) else 0,
                    'daily_usage': 2.4,  # kWh
                    'monthly_usage': 72.0,  # kWh
                    'cost': 10.8  # USD
                }
        
        # Overall usage
        total_power = sum(1 for device in self._devices.values() if device.properties.get('power', False))
        return {
            'total_devices_on': total_power,
            'total_power_consumption': total_power * 100,  # watts
            'daily_usage': total_power * 2.4,  # kWh
            'monthly_usage': total_power * 72.0,  # kWh
            'estimated_cost': total_power * 10.8  # USD
        }

    def set_scene(self, scene_name: str) -> bool:
        """Activate a predefined scene."""
        if scene_name not in self._scenes:
            return False
        
        scene = self._scenes[scene_name]
        success_count = 0
        
        for action in scene['actions']:
            if self.control_device(action['device_id'], action['action'], action.get('parameters', {})):
                success_count += 1
        
        return success_count > 0

    def get_scenes(self) -> List[Dict[str, Any]]:
        """Get all available scenes."""
        return [
            {
                'name': name,
                'description': scene['description'],
                'action_count': len(scene['actions'])
            }
            for name, scene in self._scenes.items()
        ]

    def schedule_action(self, device_id: str, action: str, schedule: Dict[str, Any]) -> str:
        """Schedule an action for a device."""
        schedule_id = str(uuid.uuid4())
        
        scheduled_action = {
            'id': schedule_id,
            'device_id': device_id,
            'action': action,
            'schedule': schedule,
            'created_at': datetime.now().isoformat(),
            'executed': False
        }
        
        self._schedules[schedule_id] = scheduled_action
        print(f"✅ Scheduled action {schedule_id} created successfully")
        return schedule_id

    def get_schedules(self) -> List[Dict[str, Any]]:
        """Get all scheduled actions."""
        return list(self._schedules.values())

    def cancel_schedule(self, schedule_id: str) -> bool:
        """Cancel a scheduled action."""
        if schedule_id in self._schedules:
            del self._schedules[schedule_id]
            print(f"✅ Schedule {schedule_id} cancelled successfully")
            return True
        return False

    def get_system_status(self) -> Dict[str, Any]:
        """Get overall smart home system status."""
        total_devices = len(self._devices)
        online_devices = sum(1 for device in self._devices.values() if device.status == DeviceStatus.ONLINE)
        powered_devices = sum(1 for device in self._devices.values() if device.properties.get('power', False))
        
        return {
            'total_devices': total_devices,
            'online_devices': online_devices,
            'powered_devices': powered_devices,
            'automations': len(self._automations),
            'scenes': len(self._scenes),
            'schedules': len(self._schedules),
            'system_health': 'good' if online_devices == total_devices else 'warning',
            'last_updated': datetime.now().isoformat()
        }

    def backup_configuration(self) -> Dict[str, Any]:
        """Backup smart home configuration."""
        return {
            'devices': {device_id: {
                'name': device.name,
                'type': device.type.value,
                'capabilities': device.capabilities,
                'properties': device.properties,
                'location': device.location,
                'manufacturer': device.manufacturer,
                'model': device.model
            } for device_id, device in self._devices.items()},
            'automations': self._automations,
            'scenes': self._scenes,
            'schedules': self._schedules,
            'rooms': self._rooms,
            'backup_timestamp': datetime.now().isoformat()
        }

    def restore_configuration(self, config: Dict[str, Any]) -> bool:
        """Restore smart home configuration."""
        try:
            # Restore devices
            self._devices.clear()
            for device_id, device_data in config.get('devices', {}).items():
                device = SmartDevice(
                    id=device_id,
                    name=device_data['name'],
                    type=DeviceType(device_data['type']),
                    status=DeviceStatus.ONLINE,
                    capabilities=device_data['capabilities'],
                    properties=device_data['properties'],
                    location=device_data.get('location'),
                    manufacturer=device_data.get('manufacturer'),
                    model=device_data.get('model')
                )
                self._devices[device_id] = device
            
            # Restore other configurations
            self._automations = config.get('automations', {})
            self._scenes = config.get('scenes', {})
            self._schedules = config.get('schedules', {})
            self._rooms = config.get('rooms', {})
            
            print("✅ Smart home configuration restored successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to restore configuration: {e}")
            return False