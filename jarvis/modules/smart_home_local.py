from jarvis.interfaces.smart_home import SmartHomeInterface, AutomationInterface, DeviceTypeInterface
from typing import Dict, List, Optional, Any
import json
import datetime
import threading
import time
import uuid

class LocalSmartHome(SmartHomeInterface, AutomationInterface):
    def __init__(self):
        self._is_initialized = False
        self._devices = {}
        self._automations = {}
        self._device_types = {
            'light': LightDevice(),
            'thermostat': ThermostatDevice(),
            'lock': LockDevice(),
            'camera': CameraDevice(),
            'sensor': SensorDevice()
        }

    def initialize(self, config: dict) -> bool:
        """Initialize local smart home system."""
        try:
            # Add some default devices for testing
            self._add_default_devices()
            self._is_initialized = True
            return True
        except Exception as e:
            print(f"Smart home initialization failed: {e}")
            return False

    def discover_devices(self) -> List[dict]:
        """Discover available smart home devices."""
        if not self._is_initialized:
            return []
        
        # Simulate device discovery
        discovered_devices = []
        for device_id, device in self._devices.items():
            discovered_devices.append({
                'id': device_id,
                'name': device['name'],
                'type': device['type'],
                'status': device['status'],
                'discovered': datetime.datetime.now().isoformat()
            })
        
        return discovered_devices

    def get_device_status(self, device_id: str) -> dict:
        """Get status of a specific device."""
        if device_id not in self._devices:
            return {'error': 'Device not found'}
        
        device = self._devices[device_id]
        return {
            'id': device_id,
            'name': device['name'],
            'type': device['type'],
            'status': device['status'],
            'last_updated': datetime.datetime.now().isoformat()
        }

    def control_device(self, device_id: str, command: str, parameters: dict = None) -> bool:
        """Control a smart home device."""
        if device_id not in self._devices:
            return False
        
        device = self._devices[device_id]
        device_type = device['type']
        
        if device_type in self._device_types:
            device_handler = self._device_types[device_type]
            if device_handler.validate_command(command, parameters or {}):
                success = device_handler.execute_command(device_id, command, parameters or {})
                if success:
                    # Update device status
                    device['status']['last_command'] = command
                    device['status']['last_updated'] = datetime.datetime.now().isoformat()
                return success
        
        return False

    def get_all_devices(self) -> List[dict]:
        """Get all registered devices."""
        return list(self._devices.values())

    def add_device(self, device_info: dict) -> bool:
        """Add a new device to the system."""
        try:
            device_id = str(uuid.uuid4())
            device_info['id'] = device_id
            device_info['added'] = datetime.datetime.now().isoformat()
            
            # Initialize device status based on type
            device_type = device_info.get('type', 'unknown')
            if device_type in self._device_types:
                device_handler = self._device_types[device_type]
                device_info['status'] = device_handler.get_default_status()
            
            self._devices[device_id] = device_info
            return True
        except Exception as e:
            print(f"Error adding device: {e}")
            return False

    def remove_device(self, device_id: str) -> bool:
        """Remove a device from the system."""
        if device_id in self._devices:
            del self._devices[device_id]
            return True
        return False

    # Automation Interface Methods
    def create_automation(self, name: str, conditions: dict, actions: List[dict]) -> bool:
        """Create a new automation rule."""
        try:
            automation_id = str(uuid.uuid4())
            automation = {
                'id': automation_id,
                'name': name,
                'conditions': conditions,
                'actions': actions,
                'enabled': True,
                'created': datetime.datetime.now().isoformat(),
                'last_triggered': None
            }
            
            self._automations[automation_id] = automation
            return True
        except Exception as e:
            print(f"Error creating automation: {e}")
            return False

    def list_automations(self) -> List[dict]:
        """List all automation rules."""
        return list(self._automations.values())

    def enable_automation(self, automation_id: str) -> bool:
        """Enable an automation rule."""
        if automation_id in self._automations:
            self._automations[automation_id]['enabled'] = True
            return True
        return False

    def disable_automation(self, automation_id: str) -> bool:
        """Disable an automation rule."""
        if automation_id in self._automations:
            self._automations[automation_id]['enabled'] = False
            return True
        return False

    def delete_automation(self, automation_id: str) -> bool:
        """Delete an automation rule."""
        if automation_id in self._automations:
            del self._automations[automation_id]
            return True
        return False

    def _add_default_devices(self):
        """Add default devices for testing."""
        default_devices = [
            {
                'name': 'Living Room Light',
                'type': 'light',
                'location': 'living_room'
            },
            {
                'name': 'Kitchen Light',
                'type': 'light',
                'location': 'kitchen'
            },
            {
                'name': 'Main Thermostat',
                'type': 'thermostat',
                'location': 'hallway'
            },
            {
                'name': 'Front Door Lock',
                'type': 'lock',
                'location': 'entrance'
            },
            {
                'name': 'Security Camera',
                'type': 'camera',
                'location': 'front_yard'
            },
            {
                'name': 'Motion Sensor',
                'type': 'sensor',
                'location': 'living_room'
            }
        ]
        
        for device_info in default_devices:
            self.add_device(device_info)

class LightDevice(DeviceTypeInterface):
    def get_supported_commands(self) -> List[str]:
        return ['turn_on', 'turn_off', 'set_brightness', 'set_color', 'toggle']

    def validate_command(self, command: str, parameters: dict) -> bool:
        if command not in self.get_supported_commands():
            return False
        
        if command == 'set_brightness' and 'brightness' not in parameters:
            return False
        
        if command == 'set_color' and 'color' not in parameters:
            return False
        
        return True

    def execute_command(self, device_id: str, command: str, parameters: dict) -> bool:
        # Simulate light control
        print(f"[Smart Home] Light {device_id}: {command} {parameters}")
        return True

    def get_default_status(self) -> dict:
        return {
            'power': 'off',
            'brightness': 0,
            'color': '#ffffff',
            'last_command': None,
            'last_updated': datetime.datetime.now().isoformat()
        }

class ThermostatDevice(DeviceTypeInterface):
    def get_supported_commands(self) -> List[str]:
        return ['set_temperature', 'set_mode', 'get_temperature']

    def validate_command(self, command: str, parameters: dict) -> bool:
        if command not in self.get_supported_commands():
            return False
        
        if command == 'set_temperature' and 'temperature' not in parameters:
            return False
        
        if command == 'set_mode' and 'mode' not in parameters:
            return False
        
        return True

    def execute_command(self, device_id: str, command: str, parameters: dict) -> bool:
        # Simulate thermostat control
        print(f"[Smart Home] Thermostat {device_id}: {command} {parameters}")
        return True

    def get_default_status(self) -> dict:
        return {
            'temperature': 72,
            'mode': 'cool',
            'target_temperature': 72,
            'last_command': None,
            'last_updated': datetime.datetime.now().isoformat()
        }

class LockDevice(DeviceTypeInterface):
    def get_supported_commands(self) -> List[str]:
        return ['lock', 'unlock', 'get_status']

    def validate_command(self, command: str, parameters: dict) -> bool:
        return command in self.get_supported_commands()

    def execute_command(self, device_id: str, command: str, parameters: dict) -> bool:
        # Simulate lock control
        print(f"[Smart Home] Lock {device_id}: {command} {parameters}")
        return True

    def get_default_status(self) -> dict:
        return {
            'locked': True,
            'battery_level': 85,
            'last_command': None,
            'last_updated': datetime.datetime.now().isoformat()
        }

class CameraDevice(DeviceTypeInterface):
    def get_supported_commands(self) -> List[str]:
        return ['start_recording', 'stop_recording', 'take_photo', 'get_status']

    def validate_command(self, command: str, parameters: dict) -> bool:
        return command in self.get_supported_commands()

    def execute_command(self, device_id: str, command: str, parameters: dict) -> bool:
        # Simulate camera control
        print(f"[Smart Home] Camera {device_id}: {command} {parameters}")
        return True

    def get_default_status(self) -> dict:
        return {
            'recording': False,
            'motion_detected': False,
            'battery_level': 90,
            'last_command': None,
            'last_updated': datetime.datetime.now().isoformat()
        }

class SensorDevice(DeviceTypeInterface):
    def get_supported_commands(self) -> List[str]:
        return ['get_reading', 'calibrate']

    def validate_command(self, command: str, parameters: dict) -> bool:
        return command in self.get_supported_commands()

    def execute_command(self, device_id: str, command: str, parameters: dict) -> bool:
        # Simulate sensor control
        print(f"[Smart Home] Sensor {device_id}: {command} {parameters}")
        return True

    def get_default_status(self) -> dict:
        return {
            'motion_detected': False,
            'temperature': 70,
            'humidity': 45,
            'battery_level': 95,
            'last_command': None,
            'last_updated': datetime.datetime.now().isoformat()
        }