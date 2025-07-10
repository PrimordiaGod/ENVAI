"""
Emotional Intelligence Package for JARVIS Phase 4

This package provides emotional intelligence capabilities including:
- Emotional state detection
- Personalized responses
- Mood-based automation
- Emotional memory
- Empathetic interactions
"""

from .emotion_detector import EmotionDetector
from .personality_engine import PersonalityEngine
from .mood_analyzer import MoodAnalyzer
from .rapport_builder import RapportBuilder
from .emotional_memory import EmotionalMemory

__all__ = [
    'EmotionDetector',
    'PersonalityEngine', 
    'MoodAnalyzer',
    'RapportBuilder',
    'EmotionalMemory'
]