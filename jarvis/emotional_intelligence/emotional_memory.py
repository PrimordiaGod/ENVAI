"""
Advanced Emotional Memory System for JARVIS

Provides long-term, context-aware memory with emotional intelligence,
focusing on single-user feedback loops and continuous learning.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import time
import sqlite3
from datetime import datetime, timedelta
import hashlib

logger = logging.getLogger(__name__)


class MemoryType(Enum):
    """Types of memories with emotional context"""
    EMOTIONAL_EXPERIENCE = "emotional_experience"
    PERSONAL_PREFERENCE = "personal_preference"
    CONVERSATION_CONTEXT = "conversation_context"
    BEHAVIORAL_PATTERN = "behavioral_pattern"
    EMOTIONAL_TRIGGER = "emotional_trigger"
    RAPPORT_BUILDER = "rapport_builder"
    LEARNING_MOMENT = "learning_moment"
    ADAPTATION_POINT = "adaptation_point"


class EmotionalState(Enum):
    """Emotional states for memory context"""
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    ANXIOUS = "anxious"
    EXCITED = "excited"
    CALM = "calm"
    FRUSTRATED = "frustrated"
    CONTENT = "content"
    STRESSED = "stressed"
    NEUTRAL = "neutral"


@dataclass
class EmotionalContext:
    """Emotional context for memories"""
    primary_emotion: EmotionalState
    intensity: float  # 0.0 to 1.0
    confidence: float  # 0.0 to 1.0
    triggers: List[str] = field(default_factory=list)
    responses: List[str] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)


@dataclass
class MemoryEntry:
    """A single memory entry with emotional context"""
    id: str
    content: str
    memory_type: MemoryType
    emotional_context: EmotionalContext
    importance_score: float  # 0.0 to 1.0
    access_count: int = 0
    last_accessed: float = field(default_factory=time.time)
    created_at: float = field(default_factory=time.time)
    tags: List[str] = field(default_factory=list)
    related_memories: List[str] = field(default_factory=list)
    user_feedback: Dict[str, Any] = field(default_factory=dict)


@dataclass
class MemoryPattern:
    """Patterns identified in user behavior and emotions"""
    pattern_id: str
    pattern_type: str
    frequency: int
    emotional_context: EmotionalContext
    confidence: float
    last_observed: float
    adaptation_suggestions: List[str] = field(default_factory=list)


class AdvancedEmotionalMemory:
    """Advanced emotional memory system with continuous learning"""
    
    def __init__(self, db_path: str = "emotional_memory.db"):
        self.db_path = db_path
        self.memories: Dict[str, MemoryEntry] = {}
        self.patterns: Dict[str, MemoryPattern] = {}
        self.emotional_history: List[EmotionalContext] = []
        self.learning_moments: List[Dict[str, Any]] = []
        self.adaptation_history: List[Dict[str, Any]] = []
        
        # Initialize database
        self._init_database()
        
        # Load existing memories
        self._load_memories()
        
        logger.info("Advanced Emotional Memory System initialized")
    
    def _init_database(self):
        """Initialize the emotional memory database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create memories table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memories (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                memory_type TEXT NOT NULL,
                emotional_context TEXT NOT NULL,
                importance_score REAL NOT NULL,
                access_count INTEGER DEFAULT 0,
                last_accessed REAL NOT NULL,
                created_at REAL NOT NULL,
                tags TEXT,
                related_memories TEXT,
                user_feedback TEXT
            )
        ''')
        
        # Create patterns table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patterns (
                pattern_id TEXT PRIMARY KEY,
                pattern_type TEXT NOT NULL,
                frequency INTEGER DEFAULT 1,
                emotional_context TEXT NOT NULL,
                confidence REAL NOT NULL,
                last_observed REAL NOT NULL,
                adaptation_suggestions TEXT
            )
        ''')
        
        # Create emotional history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS emotional_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp REAL NOT NULL,
                emotional_context TEXT NOT NULL,
                trigger TEXT,
                response TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def _load_memories(self):
        """Load existing memories from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM memories')
        rows = cursor.fetchall()
        
        for row in rows:
            memory = self._row_to_memory(row)
            self.memories[memory.id] = memory
        
        # Load patterns
        cursor.execute('SELECT * FROM patterns')
        pattern_rows = cursor.fetchall()
        
        for row in pattern_rows:
            pattern = self._row_to_pattern(row)
            self.patterns[pattern.pattern_id] = pattern
        
        conn.close()
        logger.info(f"Loaded {len(self.memories)} memories and {len(self.patterns)} patterns")
    
    def _row_to_memory(self, row) -> MemoryEntry:
        """Convert database row to MemoryEntry"""
        emotional_context_data = json.loads(row[3])
        emotional_context = EmotionalContext(
            primary_emotion=EmotionalState(emotional_context_data['primary_emotion']),
            intensity=emotional_context_data['intensity'],
            confidence=emotional_context_data['confidence'],
            triggers=emotional_context_data.get('triggers', []),
            responses=emotional_context_data.get('responses', []),
            timestamp=emotional_context_data.get('timestamp', time.time())
        )
        
        return MemoryEntry(
            id=row[0],
            content=row[1],
            memory_type=MemoryType(row[2]),
            emotional_context=emotional_context,
            importance_score=row[4],
            access_count=row[5],
            last_accessed=row[6],
            created_at=row[7],
            tags=json.loads(row[8]) if row[8] else [],
            related_memories=json.loads(row[9]) if row[9] else [],
            user_feedback=json.loads(row[10]) if row[10] else {}
        )
    
    def _row_to_pattern(self, row) -> MemoryPattern:
        """Convert database row to MemoryPattern"""
        emotional_context_data = json.loads(row[3])
        emotional_context = EmotionalContext(
            primary_emotion=EmotionalState(emotional_context_data['primary_emotion']),
            intensity=emotional_context_data['intensity'],
            confidence=emotional_context_data['confidence'],
            triggers=emotional_context_data.get('triggers', []),
            responses=emotional_context_data.get('responses', []),
            timestamp=emotional_context_data.get('timestamp', time.time())
        )
        
        return MemoryPattern(
            pattern_id=row[0],
            pattern_type=row[1],
            frequency=row[2],
            emotional_context=emotional_context,
            confidence=row[4],
            last_observed=row[5],
            adaptation_suggestions=json.loads(row[6]) if row[6] else []
        )
    
    async def store_memory(self, content: str, memory_type: MemoryType, 
                          emotional_context: EmotionalContext, 
                          importance_score: float = 0.5,
                          tags: List[str] = None) -> str:
        """Store a new memory with emotional context"""
        
        memory_id = self._generate_memory_id(content, memory_type)
        
        memory = MemoryEntry(
            id=memory_id,
            content=content,
            memory_type=memory_type,
            emotional_context=emotional_context,
            importance_score=importance_score,
            tags=tags or [],
            created_at=time.time(),
            last_accessed=time.time()
        )
        
        # Store in memory
        self.memories[memory_id] = memory
        
        # Store in database
        await self._save_memory_to_db(memory)
        
        # Update emotional history
        self.emotional_history.append(emotional_context)
        
        # Analyze for patterns
        await self._analyze_patterns(memory)
        
        logger.info(f"Stored memory: {memory_id} ({memory_type.value})")
        return memory_id
    
    def _generate_memory_id(self, content: str, memory_type: MemoryType) -> str:
        """Generate unique memory ID"""
        timestamp = str(int(time.time() * 1000))
        content_hash = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"{memory_type.value}_{content_hash}_{timestamp}"
    
    async def _save_memory_to_db(self, memory: MemoryEntry):
        """Save memory to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        emotional_context_json = json.dumps({
            'primary_emotion': memory.emotional_context.primary_emotion.value,
            'intensity': memory.emotional_context.intensity,
            'confidence': memory.emotional_context.confidence,
            'triggers': memory.emotional_context.triggers,
            'responses': memory.emotional_context.responses,
            'timestamp': memory.emotional_context.timestamp
        })
        
        cursor.execute('''
            INSERT OR REPLACE INTO memories 
            (id, content, memory_type, emotional_context, importance_score, 
             access_count, last_accessed, created_at, tags, related_memories, user_feedback)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.id,
            memory.content,
            memory.memory_type.value,
            emotional_context_json,
            memory.importance_score,
            memory.access_count,
            memory.last_accessed,
            memory.created_at,
            json.dumps(memory.tags),
            json.dumps(memory.related_memories),
            json.dumps(memory.user_feedback)
        ))
        
        conn.commit()
        conn.close()
    
    async def recall_memory(self, query: str, emotional_context: EmotionalContext = None,
                           limit: int = 10) -> List[MemoryEntry]:
        """Recall relevant memories based on query and emotional context"""
        
        # Update access counts for frequently accessed memories
        for memory in self.memories.values():
            if query.lower() in memory.content.lower():
                memory.access_count += 1
                memory.last_accessed = time.time()
        
        # Score memories based on relevance and emotional context
        scored_memories = []
        for memory in self.memories.values():
            score = self._calculate_relevance_score(memory, query, emotional_context)
            scored_memories.append((memory, score))
        
        # Sort by score and return top results
        scored_memories.sort(key=lambda x: x[1], reverse=True)
        
        return [memory for memory, score in scored_memories[:limit]]
    
    def _calculate_relevance_score(self, memory: MemoryEntry, query: str, 
                                 emotional_context: EmotionalContext = None) -> float:
        """Calculate relevance score for memory recall"""
        
        # Base score from content relevance
        content_score = 0.0
        query_words = query.lower().split()
        memory_words = memory.content.lower().split()
        
        for word in query_words:
            if word in memory_words:
                content_score += 0.2
        
        # Emotional context score
        emotional_score = 0.0
        if emotional_context and memory.emotional_context:
            if emotional_context.primary_emotion == memory.emotional_context.primary_emotion:
                emotional_score += 0.3
            
            # Intensity similarity
            intensity_diff = abs(emotional_context.intensity - memory.emotional_context.intensity)
            emotional_score += max(0, 0.2 - intensity_diff)
        
        # Recency score
        time_diff = time.time() - memory.last_accessed
        recency_score = max(0, 0.1 - (time_diff / 86400))  # Decay over days
        
        # Importance score
        importance_score = memory.importance_score * 0.3
        
        # Access frequency score
        frequency_score = min(0.2, memory.access_count * 0.01)
        
        return content_score + emotional_score + recency_score + importance_score + frequency_score
    
    async def learn_from_interaction(self, interaction_data: Dict[str, Any]):
        """Learn from user interaction and adapt behavior"""
        
        # Extract learning moments
        learning_moment = {
            'timestamp': time.time(),
            'interaction_type': interaction_data.get('type', 'conversation'),
            'user_response': interaction_data.get('user_response', {}),
            'ai_response': interaction_data.get('ai_response', {}),
            'emotional_context': interaction_data.get('emotional_context', {}),
            'success_indicators': interaction_data.get('success_indicators', []),
            'adaptation_needed': interaction_data.get('adaptation_needed', False)
        }
        
        self.learning_moments.append(learning_moment)
        
        # Store as memory if significant
        if learning_moment['adaptation_needed'] or learning_moment['success_indicators']:
            emotional_context = EmotionalContext(
                primary_emotion=EmotionalState(learning_moment['emotional_context'].get('emotion', 'neutral')),
                intensity=learning_moment['emotional_context'].get('intensity', 0.5),
                confidence=learning_moment['emotional_context'].get('confidence', 0.7),
                triggers=learning_moment['emotional_context'].get('triggers', []),
                responses=learning_moment['emotional_context'].get('responses', [])
            )
            
            await self.store_memory(
                content=f"Learning moment: {learning_moment['interaction_type']} - {learning_moment['user_response']}",
                memory_type=MemoryType.LEARNING_MOMENT,
                emotional_context=emotional_context,
                importance_score=0.8,
                tags=['learning', 'adaptation']
            )
        
        # Analyze for behavioral patterns
        await self._analyze_behavioral_patterns(learning_moment)
    
    async def _analyze_patterns(self, memory: MemoryEntry):
        """Analyze memory for patterns"""
        
        # Look for emotional patterns
        if memory.emotional_context:
            pattern_key = f"emotion_{memory.emotional_context.primary_emotion.value}"
            
            if pattern_key in self.patterns:
                pattern = self.patterns[pattern_key]
                pattern.frequency += 1
                pattern.last_observed = time.time()
                
                # Update emotional context
                pattern.emotional_context.intensity = (
                    pattern.emotional_context.intensity + memory.emotional_context.intensity
                ) / 2
            else:
                pattern = MemoryPattern(
                    pattern_id=pattern_key,
                    pattern_type="emotional_pattern",
                    frequency=1,
                    emotional_context=memory.emotional_context,
                    confidence=0.5,
                    last_observed=time.time()
                )
                self.patterns[pattern_key] = pattern
        
        # Look for behavioral patterns
        if memory.memory_type == MemoryType.BEHAVIORAL_PATTERN:
            pattern_key = f"behavior_{hash(memory.content) % 1000}"
            
            if pattern_key in self.patterns:
                pattern = self.patterns[pattern_key]
                pattern.frequency += 1
                pattern.last_observed = time.time()
            else:
                pattern = MemoryPattern(
                    pattern_id=pattern_key,
                    pattern_type="behavioral_pattern",
                    frequency=1,
                    emotional_context=memory.emotional_context,
                    confidence=0.5,
                    last_observed=time.time()
                )
                self.patterns[pattern_key] = pattern
    
    async def _analyze_behavioral_patterns(self, learning_moment: Dict[str, Any]):
        """Analyze behavioral patterns from learning moments"""
        
        # Extract behavioral insights
        user_response = learning_moment.get('user_response', {})
        emotional_context = learning_moment.get('emotional_context', {})
        
        if user_response.get('satisfaction', 0) < 0.5:
            # Negative interaction - analyze for improvement
            pattern = MemoryPattern(
                pattern_id=f"negative_pattern_{int(time.time())}",
                pattern_type="negative_interaction",
                frequency=1,
                emotional_context=EmotionalContext(
                    primary_emotion=EmotionalState(emotional_context.get('emotion', 'frustrated')),
                    intensity=emotional_context.get('intensity', 0.7),
                    confidence=0.8,
                    triggers=emotional_context.get('triggers', []),
                    responses=emotional_context.get('responses', [])
                ),
                confidence=0.7,
                last_observed=time.time(),
                adaptation_suggestions=[
                    "Adjust response tone",
                    "Provide more empathetic responses",
                    "Ask clarifying questions"
                ]
            )
            self.patterns[pattern.pattern_id] = pattern
    
    def get_emotional_summary(self, time_window_hours: int = 24) -> Dict[str, Any]:
        """Get emotional summary for the specified time window"""
        
        cutoff_time = time.time() - (time_window_hours * 3600)
        
        recent_memories = [
            memory for memory in self.memories.values()
            if memory.last_accessed > cutoff_time
        ]
        
        emotional_counts = {}
        total_intensity = 0
        total_confidence = 0
        
        for memory in recent_memories:
            emotion = memory.emotional_context.primary_emotion.value
            emotional_counts[emotion] = emotional_counts.get(emotion, 0) + 1
            total_intensity += memory.emotional_context.intensity
            total_confidence += memory.emotional_context.confidence
        
        return {
            'time_window_hours': time_window_hours,
            'total_memories': len(recent_memories),
            'emotional_distribution': emotional_counts,
            'average_intensity': total_intensity / len(recent_memories) if recent_memories else 0,
            'average_confidence': total_confidence / len(recent_memories) if recent_memories else 0,
            'dominant_emotion': max(emotional_counts.items(), key=lambda x: x[1])[0] if emotional_counts else 'neutral'
        }
    
    def get_adaptation_suggestions(self) -> List[str]:
        """Get adaptation suggestions based on learned patterns"""
        
        suggestions = []
        
        # Analyze negative patterns
        negative_patterns = [
            pattern for pattern in self.patterns.values()
            if pattern.pattern_type == "negative_interaction" and pattern.frequency > 2
        ]
        
        for pattern in negative_patterns:
            suggestions.extend(pattern.adaptation_suggestions)
        
        # Analyze emotional patterns
        emotional_patterns = [
            pattern for pattern in self.patterns.values()
            if pattern.pattern_type == "emotional_pattern"
        ]
        
        for pattern in emotional_patterns:
            if pattern.emotional_context.primary_emotion in [EmotionalState.STRESSED, EmotionalState.ANXIOUS]:
                suggestions.append("Provide more calming and supportive responses")
            elif pattern.emotional_context.primary_emotion in [EmotionalState.EXCITED, EmotionalState.HAPPY]:
                suggestions.append("Maintain positive energy and enthusiasm")
        
        return list(set(suggestions))  # Remove duplicates
    
    def export_memory_data(self) -> Dict[str, Any]:
        """Export memory data for analysis"""
        
        return {
            'total_memories': len(self.memories),
            'memory_types': {
                memory_type.value: len([m for m in self.memories.values() if m.memory_type == memory_type])
                for memory_type in MemoryType
            },
            'emotional_summary': self.get_emotional_summary(),
            'patterns': {
                pattern_id: {
                    'type': pattern.pattern_type,
                    'frequency': pattern.frequency,
                    'confidence': pattern.confidence,
                    'last_observed': pattern.last_observed
                }
                for pattern_id, pattern in self.patterns.items()
            },
            'learning_moments': len(self.learning_moments),
            'adaptation_suggestions': self.get_adaptation_suggestions()
        }