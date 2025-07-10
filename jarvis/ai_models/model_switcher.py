"""
Model Switcher for JARVIS Phase 4

Provides intelligent model switching based on task requirements,
performance metrics, and cost optimization.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import time
import json

from .model_manager import TaskType, ModelType, ModelConfig

logger = logging.getLogger(__name__)


class SwitchReason(Enum):
    """Reasons for model switching"""
    PERFORMANCE = "performance"
    COST = "cost"
    CAPABILITY = "capability"
    AVAILABILITY = "availability"
    USER_PREFERENCE = "user_preference"
    TASK_REQUIREMENT = "task_requirement"


@dataclass
class SwitchDecision:
    """Decision to switch models"""
    from_model: str
    to_model: str
    reason: SwitchReason
    confidence: float
    expected_improvement: Dict[str, float]
    timestamp: float


class ModelSwitcher:
    """Intelligent model switching based on performance and requirements"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.switch_history: List[SwitchDecision] = []
        self.performance_thresholds = {
            'latency': 2.0,  # seconds
            'cost_per_token': 0.00005,  # dollars
            'success_rate': 0.95
        }
        self.switch_cooldown = 300  # 5 minutes between switches
        
    async def should_switch_model(self, current_model: str, 
                                task_type: TaskType,
                                requirements: Dict[str, Any] = None) -> Optional[SwitchDecision]:
        """Determine if we should switch to a different model"""
        
        current_time = time.time()
        
        # Check cooldown period
        if self.switch_history:
            last_switch = self.switch_history[-1]
            if current_time - last_switch.timestamp < self.switch_cooldown:
                return None
        
        # Get current model performance
        current_stats = self.model_manager.usage_stats.get(current_model, {})
        
        # Check performance thresholds
        if current_stats.get('avg_latency', 0) > self.performance_thresholds['latency']:
            return await self._create_switch_decision(
                current_model, task_type, SwitchReason.PERFORMANCE, requirements
            )
        
        # Check cost optimization
        current_config = self.model_manager.model_configs.get(current_model)
        if current_config and current_config.cost_per_token > self.performance_thresholds['cost_per_token']:
            return await self._create_switch_decision(
                current_model, task_type, SwitchReason.COST, requirements
            )
        
        # Check for better models for the task
        better_models = await self._find_better_models(current_model, task_type, requirements)
        if better_models:
            return await self._create_switch_decision(
                current_model, task_type, SwitchReason.CAPABILITY, requirements,
                preferred_model=better_models[0]
            )
        
        return None
    
    async def _create_switch_decision(self, current_model: str, task_type: TaskType,
                                    reason: SwitchReason, requirements: Dict[str, Any] = None,
                                    preferred_model: str = None) -> SwitchDecision:
        """Create a switch decision"""
        
        if preferred_model:
            target_model = preferred_model
        else:
            # Find best alternative
            alternatives = await self._find_better_models(current_model, task_type, requirements)
            target_model = alternatives[0] if alternatives else current_model
        
        # Calculate expected improvements
        improvements = await self._calculate_improvements(current_model, target_model, task_type)
        
        return SwitchDecision(
            from_model=current_model,
            to_model=target_model,
            reason=reason,
            confidence=min(0.9, improvements.get('overall', 0.5)),
            expected_improvement=improvements,
            timestamp=time.time()
        )
    
    async def _find_better_models(self, current_model: str, task_type: TaskType,
                                requirements: Dict[str, Any] = None) -> List[str]:
        """Find models that might be better for the current task"""
        
        available_models = self.model_manager.get_models_for_task(task_type)
        better_models = []
        
        current_config = self.model_manager.model_configs.get(current_model)
        if not current_config:
            return available_models
        
        for model_name in available_models:
            if model_name == current_model:
                continue
                
            model_config = self.model_manager.model_configs.get(model_name)
            if not model_config:
                continue
            
            # Check if this model is better based on requirements
            if requirements:
                if requirements.get('cost_sensitive') and model_config.cost_per_token < current_config.cost_per_token:
                    better_models.append(model_name)
                elif requirements.get('speed_sensitive') and model_config.model_type in [ModelType.LOCAL_LLAMA, ModelType.LOCAL_MISTRAL]:
                    better_models.append(model_name)
                elif requirements.get('quality_sensitive') and model_config.model_type in [ModelType.GPT_4, ModelType.CLAUDE_3]:
                    better_models.append(model_name)
            else:
                # Default: prefer cheaper models with similar capabilities
                if model_config.cost_per_token < current_config.cost_per_token:
                    better_models.append(model_name)
        
        return better_models
    
    async def _calculate_improvements(self, from_model: str, to_model: str, 
                                   task_type: TaskType) -> Dict[str, float]:
        """Calculate expected improvements from switching models"""
        
        from_config = self.model_manager.model_configs.get(from_model)
        to_config = self.model_manager.model_configs.get(to_model)
        
        if not from_config or not to_config:
            return {'overall': 0.0}
        
        improvements = {}
        
        # Cost improvement
        if from_config.cost_per_token > 0:
            cost_improvement = (from_config.cost_per_token - to_config.cost_per_token) / from_config.cost_per_token
            improvements['cost'] = max(0, cost_improvement)
        
        # Speed improvement (estimated)
        speed_improvement = 0.0
        if from_config.model_type in [ModelType.GPT_4, ModelType.CLAUDE_3] and to_config.model_type in [ModelType.LOCAL_LLAMA, ModelType.LOCAL_MISTRAL]:
            speed_improvement = 0.3  # Local models are faster
        elif from_config.model_type in [ModelType.LOCAL_LLAMA, ModelType.LOCAL_MISTRAL] and to_config.model_type in [ModelType.GPT_4, ModelType.CLAUDE_3]:
            speed_improvement = -0.2  # Cloud models are slower but more capable
        
        improvements['speed'] = speed_improvement
        
        # Capability improvement
        capability_improvement = 0.0
        if to_config.model_type in [ModelType.GPT_4, ModelType.CLAUDE_3]:
            capability_improvement = 0.2
        elif from_config.model_type in [ModelType.GPT_4, ModelType.CLAUDE_3] and to_config.model_type in [ModelType.GPT_3_5, ModelType.LOCAL_LLAMA]:
            capability_improvement = -0.1
        
        improvements['capability'] = capability_improvement
        
        # Overall improvement
        overall = sum(improvements.values()) / len(improvements)
        improvements['overall'] = max(0, overall)
        
        return improvements
    
    def record_switch(self, decision: SwitchDecision):
        """Record a model switch decision"""
        self.switch_history.append(decision)
        logger.info(f"Model switch recorded: {decision.from_model} -> {decision.to_model} ({decision.reason.value})")
    
    def get_switch_history(self, limit: int = 10) -> List[SwitchDecision]:
        """Get recent switch history"""
        return self.switch_history[-limit:] if self.switch_history else []
    
    def get_switch_statistics(self) -> Dict[str, Any]:
        """Get statistics about model switching"""
        if not self.switch_history:
            return {}
        
        total_switches = len(self.switch_history)
        reasons = {}
        
        for decision in self.switch_history:
            reason = decision.reason.value
            reasons[reason] = reasons.get(reason, 0) + 1
        
        return {
            'total_switches': total_switches,
            'reasons': reasons,
            'avg_confidence': sum(d.confidence for d in self.switch_history) / total_switches,
            'last_switch': self.switch_history[-1].timestamp if self.switch_history else None
        }
    
    async def auto_switch_for_task(self, task_type: TaskType, 
                                 requirements: Dict[str, Any] = None) -> str:
        """Automatically select the best model for a task"""
        
        # Get available models for the task
        available_models = self.model_manager.get_models_for_task(task_type)
        
        if not available_models:
            # Fallback to any available model
            available_models = self.model_manager.get_available_models()
        
        if not available_models:
            raise ValueError("No available models found")
        
        # Apply requirements-based selection
        if requirements:
            if requirements.get('cost_sensitive'):
                # Choose cheapest model
                return min(available_models, 
                          key=lambda m: self.model_manager.model_configs[m].cost_per_token)
            elif requirements.get('speed_sensitive'):
                # Choose fastest model (local models)
                local_models = [m for m in available_models 
                              if self.model_manager.model_configs[m].model_type in 
                              [ModelType.LOCAL_LLAMA, ModelType.LOCAL_MISTRAL]]
                return local_models[0] if local_models else available_models[0]
            elif requirements.get('quality_sensitive'):
                # Choose highest quality model
                quality_models = [m for m in available_models 
                                if self.model_manager.model_configs[m].model_type in 
                                [ModelType.GPT_4, ModelType.CLAUDE_3]]
                return quality_models[0] if quality_models else available_models[0]
        
        # Default: choose first available model
        return available_models[0]