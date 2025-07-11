from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum

class DeviceType(Enum):
    """Types of smart home devices."""
    LIGHT = "light"
    SWITCH = "switch"
    THERMOSTAT = "thermostat"
    CAMERA = "camera"
    SENSOR = "sensor"
    LOCK = "lock"
    APPLIANCE = "appliance"
    MEDIA = "media"

class DeviceStatus(Enum):
    """Device status enumeration."""
    ONLINE = "online"
    OFFLINE = "offline"
    ERROR = "error"
    BUSY = "busy"

@dataclass
class SmartDevice:
    """Represents a smart home device."""
    id: str
    name: str
    type: DeviceType
    status: DeviceStatus
    capabilities: List[str]
    properties: Dict[str, Any]
    location: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None

class SmartHomeInterface(ABC):
    """Interface for smart home integration."""
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Initialize the smart home interface."""
        pass

    @abstractmethod
    def discover_devices(self) -> List[SmartDevice]:
        """Discover available smart home devices."""
        pass

    @abstractmethod
    def get_device(self, device_id: str) -> Optional[SmartDevice]:
        """Get a specific device by ID."""
        pass

    @abstractmethod
    def get_devices_by_type(self, device_type: DeviceType) -> List[SmartDevice]:
        """Get all devices of a specific type."""
        pass

    @abstractmethod
    def control_device(self, device_id: str, action: str, parameters: Dict[str, Any] = None) -> bool:
        """Control a smart home device."""
        pass

    @abstractmethod
    def get_device_status(self, device_id: str) -> Optional[DeviceStatus]:
        """Get the status of a specific device."""
        pass

    @abstractmethod
    def create_automation(self, name: str, trigger: Dict[str, Any], actions: List[Dict[str, Any]]) -> str:
        """Create a new automation rule."""
        pass

    @abstractmethod
    def get_automations(self) -> List[Dict[str, Any]]:
        """Get all automation rules."""
        pass

    @abstractmethod
    def delete_automation(self, automation_id: str) -> bool:
        """Delete an automation rule."""
        pass

    @abstractmethod
    def get_rooms(self) -> List[Dict[str, Any]]:
        """Get all rooms/locations."""
        pass

    @abstractmethod
    def get_devices_in_room(self, room_name: str) -> List[SmartDevice]:
        """Get all devices in a specific room."""
        pass

    @abstractmethod
    def voice_control(self, command: str) -> Dict[str, Any]:
        """Process voice commands for smart home control."""
        pass

    @abstractmethod
    def get_energy_usage(self, device_id: Optional[str] = None) -> Dict[str, Any]:
        """Get energy usage statistics."""
        pass

    @abstractmethod
    def set_scene(self, scene_name: str) -> bool:
        """Activate a predefined scene."""
        pass

    @abstractmethod
    def get_scenes(self) -> List[Dict[str, Any]]:
        """Get all available scenes."""
        pass

    @abstractmethod
    def schedule_action(self, device_id: str, action: str, schedule: Dict[str, Any]) -> str:
        """Schedule an action for a device."""
        pass

    @abstractmethod
    def get_schedules(self) -> List[Dict[str, Any]]:
        """Get all scheduled actions."""
        pass

    @abstractmethod
    def cancel_schedule(self, schedule_id: str) -> bool:
        """Cancel a scheduled action."""
        pass

    @abstractmethod
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall smart home system status."""
        pass

    @abstractmethod
    def backup_configuration(self) -> Dict[str, Any]:
        """Backup smart home configuration."""
        pass

    @abstractmethod
    def restore_configuration(self, config: Dict[str, Any]) -> bool:
        """Restore smart home configuration."""
        pass