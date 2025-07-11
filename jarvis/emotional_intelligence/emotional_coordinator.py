"""
Emotional Intelligence Coordinator for JARVIS

Coordinates emotional memory, personality adaptation, and continuous learning
for advanced single-user emotional intelligence and rapport building.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import json
import time

from .emotional_memory import AdvancedEmotionalMemory, EmotionalState, EmotionalContext, MemoryType
from .personality_engine import PersonalityEngine, CommunicationStyle, PersonalityTrait

logger = logging.getLogger(__name__)


@dataclass
class EmotionalAnalysis:
    """Result of emotional analysis"""
    primary_emotion: EmotionalState
    intensity: float
    confidence: float
    triggers: List[str]
    responses: List[str]
    adaptation_suggestions: List[str]
    communication_style: CommunicationStyle


@dataclass
class InteractionContext:
    """Context for user interaction"""
    user_input: str
    emotional_context: EmotionalContext
    personality_adaptation: Dict[str, Any]
    memory_recall: List[Any]
    learning_moment: bool
    adaptation_applied: bool


class EmotionalIntelligenceCoordinator:
    """Main coordinator for emotional intelligence system"""
    
    def __init__(self, db_path: str = "emotional_intelligence.db"):
        self.db_path = db_path
        
        # Initialize core components
        self.emotional_memory = AdvancedEmotionalMemory(db_path)
        self.personality_engine = PersonalityEngine(self.emotional_memory)
        
        # Interaction tracking
        self.interaction_history: List[InteractionContext] = []
        self.learning_sessions: List[Dict[str, Any]] = []
        self.rapport_metrics: Dict[str, Any] = {}
        
        # Performance tracking
        self.adaptation_success_rate = 0.0
        self.emotional_accuracy = 0.0
        self.rapport_score = 0.0
        
        logger.info("Emotional Intelligence Coordinator initialized")
    
    async def process_interaction(self, user_input: str, 
                                detected_emotion: Dict[str, Any] = None,
                                user_feedback: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a user interaction with emotional intelligence"""
        
        # Analyze emotional context
        emotional_context = await self._analyze_emotional_context(user_input, detected_emotion)
        
        # Recall relevant memories
        relevant_memories = await self.emotional_memory.recall_memory(
            user_input, emotional_context, limit=5
        )
        
        # Adapt personality based on emotional context
        await self.personality_engine.adapt_personality(emotional_context, user_feedback)
        
        # Get communication style and response template
        communication_style = self.personality_engine.get_communication_style(emotional_context)
        response_template = self.personality_engine.get_response_template(emotional_context)
        
        # Store interaction context
        interaction_context = InteractionContext(
            user_input=user_input,
            emotional_context=emotional_context,
            personality_adaptation={
                'communication_style': communication_style.value,
                'response_template': response_template,
                'traits_modified': self.personality_engine.personality_profile.adaptive_traits
            },
            memory_recall=relevant_memories,
            learning_moment=bool(user_feedback),
            adaptation_applied=True
        )
        
        self.interaction_history.append(interaction_context)
        
        # Learn from interaction if feedback provided
        if user_feedback:
            await self._learn_from_interaction(user_input, emotional_context, user_feedback)
        
        # Update rapport metrics
        await self._update_rapport_metrics(interaction_context)
        
        return {
            'emotional_context': {
                'emotion': emotional_context.primary_emotion.value,
                'intensity': emotional_context.intensity,
                'confidence': emotional_context.confidence,
                'triggers': emotional_context.triggers
            },
            'communication_style': communication_style.value,
            'response_template': response_template,
            'relevant_memories': len(relevant_memories),
            'personality_adaptation': interaction_context.personality_adaptation,
            'rapport_score': self.rapport_score
        }
    
    async def _analyze_emotional_context(self, user_input: str, 
                                       detected_emotion: Dict[str, Any] = None) -> EmotionalContext:
        """Analyze emotional context from user input and detected emotion"""
        
        # Use detected emotion if available
        if detected_emotion:
            primary_emotion = EmotionalState(detected_emotion.get('emotion', 'neutral'))
            intensity = detected_emotion.get('intensity', 0.5)
            confidence = detected_emotion.get('confidence', 0.7)
            triggers = detected_emotion.get('triggers', [])
            responses = detected_emotion.get('responses', [])
        else:
            # Basic emotion detection from text
            primary_emotion, intensity, confidence, triggers, responses = self._detect_emotion_from_text(user_input)
        
        return EmotionalContext(
            primary_emotion=primary_emotion,
            intensity=intensity,
            confidence=confidence,
            triggers=triggers,
            responses=responses,
            timestamp=time.time()
        )
    
    def _detect_emotion_from_text(self, text: str) -> tuple:
        """Basic emotion detection from text analysis"""
        
        text_lower = text.lower()
        
        # Happy indicators
        happy_words = ['happy', 'excited', 'great', 'wonderful', 'fantastic', 'amazing', 'love', '😊', '😄', '✨']
        if any(word in text_lower for word in happy_words):
            return EmotionalState.HAPPY, 0.8, 0.7, ['positive_words'], ['express_joy']
        
        # Sad indicators
        sad_words = ['sad', 'depressed', 'down', 'unhappy', 'crying', '😢', '😭', '💔']
        if any(word in text_lower for word in sad_words):
            return EmotionalState.SAD, 0.7, 0.8, ['negative_words'], ['offer_support']
        
        # Anxious indicators
        anxious_words = ['anxious', 'worried', 'nervous', 'stress', 'fear', '😰', '😨', '😱']
        if any(word in text_lower for word in anxious_words):
            return EmotionalState.ANXIOUS, 0.8, 0.8, ['anxiety_triggers'], ['provide_calm']
        
        # Angry indicators
        angry_words = ['angry', 'mad', 'furious', 'hate', 'annoyed', '😠', '😡', '💢']
        if any(word in text_lower for word in angry_words):
            return EmotionalState.ANGRY, 0.8, 0.8, ['frustration_triggers'], ['de_escalate']
        
        # Stressed indicators
        stressed_words = ['stressed', 'overwhelmed', 'busy', 'pressure', 'deadline', '😰', '😓']
        if any(word in text_lower for word in stressed_words):
            return EmotionalState.STRESSED, 0.7, 0.7, ['stress_triggers'], ['offer_help']
        
        # Default to neutral
        return EmotionalState.NEUTRAL, 0.5, 0.5, [], []
    
    async def _learn_from_interaction(self, user_input: str, 
                                    emotional_context: EmotionalContext,
                                    user_feedback: Dict[str, Any]):
        """Learn from user interaction and feedback"""
        
        # Create interaction data for learning
        interaction_data = {
            'type': 'conversation',
            'user_response': {
                'input': user_input,
                'satisfaction': user_feedback.get('satisfaction', 0.5),
                'emotional_state': emotional_context.primary_emotion.value
            },
            'ai_response': {
                'communication_style': self.personality_engine.personality_profile.communication_style.value,
                'adaptation_applied': True
            },
            'emotional_context': {
                'emotion': emotional_context.primary_emotion.value,
                'intensity': emotional_context.intensity,
                'confidence': emotional_context.confidence,
                'triggers': emotional_context.triggers
            },
            'success_indicators': user_feedback.get('positive_indicators', []),
            'adaptation_needed': user_feedback.get('negative', False),
            'user_feedback': user_feedback
        }
        
        # Learn in personality engine
        await self.personality_engine.learn_from_interaction(interaction_data)
        
        # Store learning session
        learning_session = {
            'timestamp': time.time(),
            'interaction_data': interaction_data,
            'emotional_context': emotional_context,
            'adaptation_applied': True,
            'learning_outcome': 'positive' if user_feedback.get('satisfaction', 0.5) > 0.6 else 'negative'
        }
        
        self.learning_sessions.append(learning_session)
        
        # Update learning metrics
        await self._update_learning_metrics(learning_session)
    
    async def _update_rapport_metrics(self, interaction_context: InteractionContext):
        """Update rapport building metrics"""
        
        # Calculate rapport score based on interaction quality
        emotional_alignment = 1.0 if interaction_context.adaptation_applied else 0.5
        memory_relevance = min(1.0, len(interaction_context.memory_recall) / 5.0)
        learning_engagement = 1.0 if interaction_context.learning_moment else 0.7
        
        # Weighted rapport score
        self.rapport_score = (
            emotional_alignment * 0.4 +
            memory_relevance * 0.3 +
            learning_engagement * 0.3
        )
        
        # Update rapport metrics
        self.rapport_metrics = {
            'current_score': self.rapport_score,
            'emotional_alignment': emotional_alignment,
            'memory_relevance': memory_relevance,
            'learning_engagement': learning_engagement,
            'total_interactions': len(self.interaction_history),
            'learning_sessions': len(self.learning_sessions)
        }
    
    async def _update_learning_metrics(self, learning_session: Dict[str, Any]):
        """Update learning and adaptation metrics"""
        
        # Calculate adaptation success rate
        recent_sessions = [
            session for session in self.learning_sessions
            if time.time() - session['timestamp'] < 86400  # Last 24 hours
        ]
        
        if recent_sessions:
            successful_adaptations = sum(
                1 for session in recent_sessions
                if session['learning_outcome'] == 'positive'
            )
            self.adaptation_success_rate = successful_adaptations / len(recent_sessions)
        
        # Calculate emotional accuracy
        emotional_accuracy_sum = sum(
            session['emotional_context'].confidence
            for session in recent_sessions
        )
        self.emotional_accuracy = emotional_accuracy_sum / len(recent_sessions) if recent_sessions else 0.0
    
    async def get_emotional_insights(self) -> Dict[str, Any]:
        """Get comprehensive emotional intelligence insights"""
        
        # Get emotional summary
        emotional_summary = self.emotional_memory.get_emotional_summary()
        
        # Get personality summary
        personality_summary = self.personality_engine.get_personality_summary()
        
        # Get adaptation suggestions
        adaptation_suggestions = self.personality_engine.get_emotional_adaptation_suggestions()
        
        # Get memory insights
        memory_data = self.emotional_memory.export_memory_data()
        
        return {
            'emotional_summary': emotional_summary,
            'personality_summary': personality_summary,
            'rapport_metrics': self.rapport_metrics,
            'learning_metrics': {
                'adaptation_success_rate': self.adaptation_success_rate,
                'emotional_accuracy': self.emotional_accuracy,
                'total_learning_sessions': len(self.learning_sessions),
                'recent_interactions': len(self.interaction_history[-10:])  # Last 10
            },
            'adaptation_suggestions': adaptation_suggestions,
            'memory_insights': memory_data,
            'emotional_patterns': {
                'dominant_emotion': emotional_summary.get('dominant_emotion', 'neutral'),
                'average_intensity': emotional_summary.get('average_intensity', 0.0),
                'emotional_distribution': emotional_summary.get('emotional_distribution', {})
            }
        }
    
    async def get_continuous_learning_report(self) -> Dict[str, Any]:
        """Get detailed continuous learning report"""
        
        # Analyze learning patterns
        recent_learning_sessions = [
            session for session in self.learning_sessions
            if time.time() - session['timestamp'] < 604800  # Last week
        ]
        
        # Group by learning outcome
        positive_sessions = [s for s in recent_learning_sessions if s['learning_outcome'] == 'positive']
        negative_sessions = [s for s in recent_learning_sessions if s['learning_outcome'] == 'negative']
        
        # Analyze emotional patterns in learning
        emotional_learning_patterns = {}
        for session in recent_learning_sessions:
            emotion = session['emotional_context'].primary_emotion.value
            if emotion not in emotional_learning_patterns:
                emotional_learning_patterns[emotion] = {'positive': 0, 'negative': 0}
            
            if session['learning_outcome'] == 'positive':
                emotional_learning_patterns[emotion]['positive'] += 1
            else:
                emotional_learning_patterns[emotion]['negative'] += 1
        
        return {
            'learning_period': 'last_week',
            'total_learning_sessions': len(recent_learning_sessions),
            'positive_learning_outcomes': len(positive_sessions),
            'negative_learning_outcomes': len(negative_sessions),
            'success_rate': len(positive_sessions) / len(recent_learning_sessions) if recent_learning_sessions else 0.0,
            'emotional_learning_patterns': emotional_learning_patterns,
            'adaptation_suggestions': self.personality_engine.get_emotional_adaptation_suggestions(),
            'personality_evolution': {
                'base_traits': self.personality_engine.personality_profile.base_traits,
                'current_traits': self.personality_engine.personality_profile.adaptive_traits,
                'adaptation_history_count': len(self.personality_engine.adaptation_history)
            },
            'memory_learning': {
                'total_memories': len(self.emotional_memory.memories),
                'learning_moments': len(self.emotional_memory.learning_moments),
                'patterns_identified': len(self.emotional_memory.patterns)
            }
        }
    
    async def export_emotional_intelligence_data(self) -> Dict[str, Any]:
        """Export comprehensive emotional intelligence data"""
        
        return {
            'emotional_memory': self.emotional_memory.export_memory_data(),
            'personality_engine': self.personality_engine.export_personality_data(),
            'coordinator_metrics': {
                'rapport_score': self.rapport_score,
                'adaptation_success_rate': self.adaptation_success_rate,
                'emotional_accuracy': self.emotional_accuracy,
                'total_interactions': len(self.interaction_history),
                'learning_sessions': len(self.learning_sessions)
            },
            'emotional_insights': await self.get_emotional_insights(),
            'continuous_learning_report': await self.get_continuous_learning_report()
        }