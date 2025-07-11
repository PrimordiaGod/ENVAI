"""
Emotional Intelligence Package for JARVIS

Provides advanced emotional intelligence capabilities including:
- Advanced memory architecture
- Personality adaptation
- Continuous learning
- Emotional analysis
- Rapport building
"""

from .emotional_memory import (
    AdvancedEmotionalMemory,
    EmotionalState,
    EmotionalContext,
    MemoryType,
    MemoryEntry,
    MemoryPattern
)

from .personality_engine import (
    PersonalityEngine,
    CommunicationStyle,
    PersonalityTrait,
    PersonalityProfile,
    EmotionalResponse
)

from .emotional_coordinator import (
    EmotionalIntelligenceCoordinator,
    EmotionalAnalysis,
    InteractionContext
)

__all__ = [
    # Memory system
    'AdvancedEmotionalMemory',
    'EmotionalState',
    'EmotionalContext',
    'MemoryType',
    'MemoryEntry',
    'MemoryPattern',
    
    # Personality system
    'PersonalityEngine',
    'CommunicationStyle',
    'PersonalityTrait',
    'PersonalityProfile',
    'EmotionalResponse',
    
    # Coordinator
    'EmotionalIntelligenceCoordinator',
    'EmotionalAnalysis',
    'InteractionContext'
]