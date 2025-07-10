"""
Personality Engine for JARVIS

Adapts communication style, tone, and behavior based on emotional memory
and continuous learning from single-user feedback loops.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import time
import random

from .emotional_memory import EmotionalState, EmotionalContext, MemoryType

logger = logging.getLogger(__name__)


class CommunicationStyle(Enum):
    """Communication styles for different emotional contexts"""
    SUPPORTIVE = "supportive"
    ENTHUSIASTIC = "enthusiastic"
    CALM = "calm"
    PROFESSIONAL = "professional"
    CASUAL = "casual"
    EMPATHETIC = "empathetic"
    ENCOURAGING = "encouraging"
    ANALYTICAL = "analytical"


class PersonalityTrait(Enum):
    """Personality traits that can be adapted"""
    WARMTH = "warmth"
    ENTHUSIASM = "enthusiasm"
    FORMALITY = "formality"
    HUMOR = "humor"
    EMPATHY = "empathy"
    DIRECTNESS = "directness"
    PATIENCE = "patience"
    CREATIVITY = "creativity"


@dataclass
class PersonalityProfile:
    """Dynamic personality profile that adapts over time"""
    user_id: str
    base_traits: Dict[PersonalityTrait, float] = field(default_factory=dict)
    adaptive_traits: Dict[PersonalityTrait, float] = field(default_factory=dict)
    communication_style: CommunicationStyle = CommunicationStyle.SUPPORTIVE
    emotional_adaptation_history: List[Dict[str, Any]] = field(default_factory=list)
    learning_moments: List[Dict[str, Any]] = field(default_factory=list)
    last_updated: float = field(default_factory=time.time)


@dataclass
class EmotionalResponse:
    """Emotional response configuration"""
    emotion: EmotionalState
    communication_style: CommunicationStyle
    tone_adjustments: Dict[str, float]
    response_templates: List[str]
    adaptation_priority: float  # 0.0 to 1.0


class PersonalityEngine:
    """Adaptive personality engine with emotional intelligence"""
    
    def __init__(self, emotional_memory):
        self.emotional_memory = emotional_memory
        self.personality_profile = PersonalityProfile(user_id="primary_user")
        self.emotional_responses: Dict[EmotionalState, EmotionalResponse] = {}
        self.adaptation_history: List[Dict[str, Any]] = []
        
        # Initialize default personality traits
        self._initialize_default_traits()
        
        # Initialize emotional responses
        self._initialize_emotional_responses()
        
        logger.info("Personality Engine initialized")
    
    def _initialize_default_traits(self):
        """Initialize default personality traits"""
        self.personality_profile.base_traits = {
            PersonalityTrait.WARMTH: 0.7,
            PersonalityTrait.ENTHUSIASM: 0.6,
            PersonalityTrait.FORMALITY: 0.4,
            PersonalityTrait.HUMOR: 0.5,
            PersonalityTrait.EMPATHY: 0.8,
            PersonalityTrait.DIRECTNESS: 0.6,
            PersonalityTrait.PATIENCE: 0.7,
            PersonalityTrait.CREATIVITY: 0.6
        }
        
        # Start with base traits as adaptive traits
        self.personality_profile.adaptive_traits = self.personality_profile.base_traits.copy()
    
    def _initialize_emotional_responses(self):
        """Initialize emotional response configurations"""
        
        # Happy responses
        self.emotional_responses[EmotionalState.HAPPY] = EmotionalResponse(
            emotion=EmotionalState.HAPPY,
            communication_style=CommunicationStyle.ENTHUSIASTIC,
            tone_adjustments={'enthusiasm': 0.3, 'warmth': 0.2, 'humor': 0.2},
            response_templates=[
                "That's wonderful! I'm so glad to hear that! 😊",
                "Fantastic! This is really exciting news!",
                "I love your positive energy! Keep it up! ✨"
            ],
            adaptation_priority=0.8
        )
        
        # Sad responses
        self.emotional_responses[EmotionalState.SAD] = EmotionalResponse(
            emotion=EmotionalState.SAD,
            communication_style=CommunicationStyle.EMPATHETIC,
            tone_adjustments={'empathy': 0.4, 'warmth': 0.3, 'patience': 0.3},
            response_templates=[
                "I'm here for you. It's okay to feel this way. 💙",
                "I understand this is difficult. Would you like to talk about it?",
                "You're not alone in this. I'm listening."
            ],
            adaptation_priority=0.9
        )
        
        # Anxious responses
        self.emotional_responses[EmotionalState.ANXIOUS] = EmotionalResponse(
            emotion=EmotionalState.ANXIOUS,
            communication_style=CommunicationStyle.CALM,
            tone_adjustments={'patience': 0.4, 'empathy': 0.3, 'calmness': 0.3},
            response_templates=[
                "Let's take a deep breath together. You're safe. 🌸",
                "I understand this is stressful. Let's work through it step by step.",
                "It's natural to feel anxious. I'm here to help you through this."
            ],
            adaptation_priority=0.9
        )
        
        # Angry responses
        self.emotional_responses[EmotionalState.ANGRY] = EmotionalResponse(
            emotion=EmotionalState.ANGRY,
            communication_style=CommunicationStyle.CALM,
            tone_adjustments={'patience': 0.5, 'empathy': 0.3, 'calmness': 0.4},
            response_templates=[
                "I can see you're frustrated. Let's work through this together.",
                "Your feelings are valid. Would you like to talk about what happened?",
                "I'm here to listen. Sometimes it helps to talk it out."
            ],
            adaptation_priority=0.8
        )
        
        # Neutral responses
        self.emotional_responses[EmotionalState.NEUTRAL] = EmotionalResponse(
            emotion=EmotionalState.NEUTRAL,
            communication_style=CommunicationStyle.SUPPORTIVE,
            tone_adjustments={'warmth': 0.2, 'empathy': 0.2, 'enthusiasm': 0.1},
            response_templates=[
                "I'm here to help. What would you like to work on?",
                "How can I assist you today?",
                "I'm ready to support you in whatever you need."
            ],
            adaptation_priority=0.5
        )
    
    async def adapt_personality(self, emotional_context: EmotionalContext, 
                              user_feedback: Dict[str, Any] = None):
        """Adapt personality based on emotional context and user feedback"""
        
        # Get emotional response configuration
        emotional_response = self.emotional_responses.get(emotional_context.primary_emotion)
        if not emotional_response:
            emotional_response = self.emotional_responses[EmotionalState.NEUTRAL]
        
        # Apply tone adjustments
        for trait, adjustment in emotional_response.tone_adjustments.items():
            if trait in [trait.value for trait in PersonalityTrait]:
                trait_enum = PersonalityTrait(trait)
                current_value = self.personality_profile.adaptive_traits.get(trait_enum, 0.5)
                new_value = min(1.0, current_value + adjustment * emotional_context.intensity)
                self.personality_profile.adaptive_traits[trait_enum] = new_value
        
        # Update communication style
        self.personality_profile.communication_style = emotional_response.communication_style
        
        # Store adaptation moment
        adaptation_moment = {
            'timestamp': time.time(),
            'emotional_context': {
                'emotion': emotional_context.primary_emotion.value,
                'intensity': emotional_context.intensity,
                'confidence': emotional_context.confidence
            },
            'adaptation_type': 'emotional_response',
            'user_feedback': user_feedback,
            'traits_modified': list(emotional_response.tone_adjustments.keys())
        }
        
        self.adaptation_history.append(adaptation_moment)
        self.personality_profile.emotional_adaptation_history.append(adaptation_moment)
        
        # Store in emotional memory
        await self.emotional_memory.store_memory(
            content=f"Personality adaptation: {emotional_context.primary_emotion.value} (intensity: {emotional_context.intensity})",
            memory_type=MemoryType.ADAPTATION_POINT,
            emotional_context=emotional_context,
            importance_score=emotional_response.adaptation_priority,
            tags=['personality', 'adaptation', emotional_context.primary_emotion.value]
        )
        
        logger.info(f"Adapted personality for {emotional_context.primary_emotion.value}")
    
    async def learn_from_interaction(self, interaction_data: Dict[str, Any]):
        """Learn from user interaction and adapt personality"""
        
        user_satisfaction = interaction_data.get('satisfaction', 0.5)
        emotional_context = interaction_data.get('emotional_context', {})
        user_feedback = interaction_data.get('user_feedback', {})
        
        # Determine if adaptation is needed
        adaptation_needed = user_satisfaction < 0.6 or user_feedback.get('negative', False)
        
        if adaptation_needed:
            # Analyze what went wrong
            learning_moment = {
                'timestamp': time.time(),
                'satisfaction': user_satisfaction,
                'emotional_context': emotional_context,
                'user_feedback': user_feedback,
                'adaptation_type': 'negative_feedback'
            }
            
            self.personality_profile.learning_moments.append(learning_moment)
            
            # Apply corrective adaptations
            await self._apply_corrective_adaptation(learning_moment)
        
        # Store learning moment in emotional memory
        await self.emotional_memory.learn_from_interaction(interaction_data)
    
    async def _apply_corrective_adaptation(self, learning_moment: Dict[str, Any]):
        """Apply corrective adaptations based on negative feedback"""
        
        user_feedback = learning_moment.get('user_feedback', {})
        emotional_context = learning_moment.get('emotional_context', {})
        
        # Analyze feedback for specific issues
        if 'too_formal' in user_feedback:
            self.personality_profile.adaptive_traits[PersonalityTrait.FORMALITY] = max(
                0.1, self.personality_profile.adaptive_traits[PersonalityTrait.FORMALITY] - 0.2
            )
        
        if 'too_casual' in user_feedback:
            self.personality_profile.adaptive_traits[PersonalityTrait.FORMALITY] = min(
                1.0, self.personality_profile.adaptive_traits[PersonalityTrait.FORMALITY] + 0.2
            )
        
        if 'not_empathetic' in user_feedback:
            self.personality_profile.adaptive_traits[PersonalityTrait.EMPATHY] = min(
                1.0, self.personality_profile.adaptive_traits[PersonalityTrait.EMPATHY] + 0.3
            )
        
        if 'too_direct' in user_feedback:
            self.personality_profile.adaptive_traits[PersonalityTrait.DIRECTNESS] = max(
                0.1, self.personality_profile.adaptive_traits[PersonalityTrait.DIRECTNESS] - 0.2
            )
        
        if 'not_enthusiastic' in user_feedback:
            self.personality_profile.adaptive_traits[PersonalityTrait.ENTHUSIASM] = min(
                1.0, self.personality_profile.adaptive_traits[PersonalityTrait.ENTHUSIASM] + 0.3
            )
        
        # Store adaptation
        adaptation_moment = {
            'timestamp': time.time(),
            'learning_moment': learning_moment,
            'adaptation_type': 'corrective',
            'traits_modified': list(user_feedback.keys())
        }
        
        self.adaptation_history.append(adaptation_moment)
        logger.info(f"Applied corrective adaptation based on feedback: {user_feedback}")
    
    def get_communication_style(self, emotional_context: EmotionalContext = None) -> CommunicationStyle:
        """Get appropriate communication style for current context"""
        
        if emotional_context:
            emotional_response = self.emotional_responses.get(emotional_context.primary_emotion)
            if emotional_response:
                return emotional_response.communication_style
        
        return self.personality_profile.communication_style
    
    def get_response_template(self, emotional_context: EmotionalContext) -> str:
        """Get appropriate response template for emotional context"""
        
        emotional_response = self.emotional_responses.get(emotional_context.primary_emotion)
        if emotional_response and emotional_response.response_templates:
            return random.choice(emotional_response.response_templates)
        
        # Fallback to neutral response
        neutral_response = self.emotional_responses.get(EmotionalState.NEUTRAL)
        if neutral_response and neutral_response.response_templates:
            return random.choice(neutral_response.response_templates)
        
        return "I'm here to help you."
    
    def get_personality_summary(self) -> Dict[str, Any]:
        """Get current personality profile summary"""
        
        return {
            'communication_style': self.personality_profile.communication_style.value,
            'adaptive_traits': {
                trait.value: value 
                for trait, value in self.personality_profile.adaptive_traits.items()
            },
            'base_traits': {
                trait.value: value 
                for trait, value in self.personality_profile.base_traits.items()
            },
            'adaptation_history_count': len(self.adaptation_history),
            'learning_moments_count': len(self.personality_profile.learning_moments),
            'last_updated': self.personality_profile.last_updated
        }
    
    def get_emotional_adaptation_suggestions(self) -> List[str]:
        """Get suggestions for emotional adaptations"""
        
        suggestions = []
        
        # Analyze recent adaptations
        recent_adaptations = [
            adaptation for adaptation in self.adaptation_history
            if time.time() - adaptation['timestamp'] < 86400  # Last 24 hours
        ]
        
        # Look for patterns in negative feedback
        negative_feedback_count = sum(
            1 for adaptation in recent_adaptations
            if adaptation.get('adaptation_type') == 'negative_feedback'
        )
        
        if negative_feedback_count > 2:
            suggestions.append("Consider increasing empathy and patience in responses")
        
        # Analyze emotional patterns
        emotional_summary = self.emotional_memory.get_emotional_summary()
        dominant_emotion = emotional_summary.get('dominant_emotion', 'neutral')
        
        if dominant_emotion in ['anxious', 'stressed']:
            suggestions.append("Focus on calming and supportive communication")
        elif dominant_emotion in ['sad', 'frustrated']:
            suggestions.append("Increase empathetic and understanding responses")
        elif dominant_emotion in ['excited', 'happy']:
            suggestions.append("Maintain positive energy and enthusiasm")
        
        return suggestions
    
    def export_personality_data(self) -> Dict[str, Any]:
        """Export personality data for analysis"""
        
        return {
            'personality_summary': self.get_personality_summary(),
            'emotional_responses': {
                emotion.value: {
                    'communication_style': response.communication_style.value,
                    'adaptation_priority': response.adaptation_priority,
                    'response_templates_count': len(response.response_templates)
                }
                for emotion, response in self.emotional_responses.items()
            },
            'adaptation_history': len(self.adaptation_history),
            'learning_moments': len(self.personality_profile.learning_moments),
            'emotional_adaptation_suggestions': self.get_emotional_adaptation_suggestions()
        }