"""
Phase 4 Integration Module for JARVIS

Integrates advanced AI model features including:
- Multi-model architecture
- Advanced reasoning patterns
- Model fine-tuning capabilities
- Context optimization
- Performance monitoring
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import time
import json

from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from ..ai_models.model_manager import AdvancedAIModelManager, TaskType, ModelType
from ..ai_models.model_switcher import ModelSwitcher
from ..ai_models.reasoning_engine import AdvancedReasoningEngine, ReasoningType
from ..ai_models.fine_tuner import ModelFineTuner, FineTuningMethod, FineTuningConfig, TrainingData

console = Console()
logger = logging.getLogger(__name__)


class Phase4Features(Enum):
    """Phase 4 feature flags"""
    ADVANCED_AI_MODELS = "advanced_ai_models"
    MODEL_SWITCHING = "model_switching"
    ADVANCED_REASONING = "advanced_reasoning"
    FINE_TUNING = "fine_tuning"
    CONTEXT_OPTIMIZATION = "context_optimization"
    PERFORMANCE_MONITORING = "performance_monitoring"


@dataclass
class Phase4Config:
    """Configuration for Phase 4 features"""
    enabled_features: List[Phase4Features]
    auto_model_switching: bool = True
    reasoning_enabled: bool = True
    fine_tuning_enabled: bool = True
    context_optimization: bool = True
    performance_monitoring: bool = True


@dataclass
class Phase4Metrics:
    """Metrics for Phase 4 performance"""
    total_requests: int = 0
    model_switches: int = 0
    reasoning_sessions: int = 0
    fine_tuning_sessions: int = 0
    avg_response_time: float = 0.0
    total_cost: float = 0.0
    context_optimizations: int = 0


class Phase4Integration:
    """Phase 4 Integration Manager"""
    
    def __init__(self, config: Phase4Config = None):
        self.config = config or Phase4Config(
            enabled_features=[
                Phase4Features.ADVANCED_AI_MODELS,
                Phase4Features.MODEL_SWITCHING,
                Phase4Features.ADVANCED_REASONING,
                Phase4Features.FINE_TUNING,
                Phase4Features.CONTEXT_OPTIMIZATION,
                Phase4Features.PERFORMANCE_MONITORING
            ]
        )
        
        # Initialize components
        self.ai_model_manager = AdvancedAIModelManager()
        self.model_switcher = ModelSwitcher(self.ai_model_manager)
        self.reasoning_engine = AdvancedReasoningEngine(self.ai_model_manager)
        self.fine_tuner = ModelFineTuner()
        
        # Initialize fine-tuners
        self._initialize_fine_tuners()
        
        # Metrics
        self.metrics = Phase4Metrics()
        self.start_time = time.time()
        
        logger.info("Phase 4 Integration initialized")
    
    def _initialize_fine_tuners(self):
        """Initialize fine-tuning methods"""
        # Register LoRA fine-tuner
        lora_config = FineTuningConfig(
            method=FineTuningMethod.LORA,
            base_model="gpt-3.5-turbo"
        )
        from ..ai_models.fine_tuner import LoRAFineTuner
        self.fine_tuner.register_fine_tuner(FineTuningMethod.LORA, LoRAFineTuner(lora_config))
        
        # Register QLoRA fine-tuner
        qlora_config = FineTuningConfig(
            method=FineTuningMethod.QLORA,
            base_model="gpt-3.5-turbo"
        )
        from ..ai_models.fine_tuner import QLoRAFineTuner
        self.fine_tuner.register_fine_tuner(FineTuningMethod.QLORA, QLoRAFineTuner(qlora_config))
        
        logger.info("Fine-tuners initialized")
    
    async def process_request(self, prompt: str, 
                            task_type: TaskType = TaskType.CONVERSATION,
                            context: Optional[str] = None,
                            requirements: Dict[str, Any] = None,
                            use_reasoning: bool = False,
                            reasoning_type: ReasoningType = None) -> Dict[str, Any]:
        """Process a request with Phase 4 features"""
        
        start_time = time.time()
        self.metrics.total_requests += 1
        
        # Context optimization
        if self.config.context_optimization and context:
            optimized_context = self.ai_model_manager.optimize_context(context)
            self.metrics.context_optimizations += 1
        else:
            optimized_context = context
        
        # Model selection and switching
        selected_model = None
        if self.config.auto_model_switching:
            selected_model = await self.model_switcher.auto_switch_for_task(task_type, requirements)
        
        # Check if we should switch models
        if self.config.auto_model_switching and selected_model:
            current_model = "GPT-4"  # Assume current model
            switch_decision = await self.model_switcher.should_switch_model(
                current_model, task_type, requirements
            )
            
            if switch_decision:
                selected_model = switch_decision.to_model
                self.model_switcher.record_switch(switch_decision)
                self.metrics.model_switches += 1
                logger.info(f"Model switched: {switch_decision.from_model} -> {switch_decision.to_model}")
        
        # Generate response
        if use_reasoning and self.config.reasoning_enabled:
            # Use advanced reasoning
            reasoning_result = await self.reasoning_engine.reason(
                prompt, reasoning_type or ReasoningType.CHAIN_OF_THOUGHT, optimized_context
            )
            
            response = {
                'content': reasoning_result.answer,
                'confidence': reasoning_result.confidence,
                'reasoning_type': reasoning_result.reasoning_type.value,
                'reasoning_paths': len(reasoning_result.reasoning_paths),
                'model_used': 'Advanced Reasoning Engine',
                'tokens_used': 0,  # Will be calculated
                'cost': 0.0,
                'latency': time.time() - start_time
            }
            
            self.metrics.reasoning_sessions += 1
            
        else:
            # Standard AI model response
            model_response = await self.ai_model_manager.generate_response(
                prompt, task_type, optimized_context, selected_model, requirements
            )
            
            response = {
                'content': model_response.content,
                'confidence': model_response.confidence,
                'model_used': model_response.model_used,
                'tokens_used': model_response.tokens_used,
                'cost': model_response.cost,
                'latency': model_response.latency
            }
        
        # Update metrics
        self.metrics.total_cost += response.get('cost', 0.0)
        self.metrics.avg_response_time = (
            (self.metrics.avg_response_time * (self.metrics.total_requests - 1) + response['latency']) 
            / self.metrics.total_requests
        )
        
        return response
    
    async def fine_tune_model(self, training_data: TrainingData,
                            method: FineTuningMethod = FineTuningMethod.LORA,
                            **config_kwargs) -> Dict[str, Any]:
        """Fine-tune a model with specified data and method"""
        
        if not self.config.fine_tuning_enabled:
            raise ValueError("Fine-tuning is not enabled")
        
        # Create fine-tuning configuration
        config = self.fine_tuner.create_fine_tuning_config(method, "gpt-3.5-turbo", **config_kwargs)
        
        # Execute fine-tuning
        result = await self.fine_tuner.fine_tune(training_data, config)
        
        self.metrics.fine_tuning_sessions += 1
        
        return {
            'model_path': result.model_path,
            'method': result.method.value,
            'final_loss': result.final_loss,
            'final_accuracy': result.final_accuracy,
            'training_time': result.training_time,
            'model_size': result.model_size,
            'is_successful': result.is_successful
        }
    
    async def evaluate_model(self, model_path: str, test_data: TrainingData,
                           method: FineTuningMethod) -> Dict[str, float]:
        """Evaluate a fine-tuned model"""
        
        return await self.fine_tuner.evaluate_model(model_path, method, test_data)
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get comprehensive model status"""
        return {
            'available_models': self.ai_model_manager.get_available_models(),
            'usage_stats': self.ai_model_manager.get_usage_stats(),
            'switch_stats': self.model_switcher.get_switch_statistics(),
            'reasoning_stats': self.reasoning_engine.get_reasoning_statistics(),
            'fine_tuning_stats': self.fine_tuner.get_training_statistics(),
            'phase4_metrics': {
                'total_requests': self.metrics.total_requests,
                'model_switches': self.metrics.model_switches,
                'reasoning_sessions': self.metrics.reasoning_sessions,
                'fine_tuning_sessions': self.metrics.fine_tuning_sessions,
                'avg_response_time': self.metrics.avg_response_time,
                'total_cost': self.metrics.total_cost,
                'context_optimizations': self.metrics.context_optimizations,
                'uptime': time.time() - self.start_time
            }
        }
    
    def display_status(self):
        """Display comprehensive Phase 4 status"""
        
        # Model Status Table
        console.print("\n[bold cyan]Phase 4 AI Model Status[/bold cyan]")
        self.ai_model_manager.display_model_status()
        
        # Phase 4 Metrics
        metrics_table = Table(title="Phase 4 Metrics")
        metrics_table.add_column("Metric", style="cyan")
        metrics_table.add_column("Value", style="green")
        
        metrics_table.add_row("Total Requests", str(self.metrics.total_requests))
        metrics_table.add_row("Model Switches", str(self.metrics.model_switches))
        metrics_table.add_row("Reasoning Sessions", str(self.metrics.reasoning_sessions))
        metrics_table.add_row("Fine-tuning Sessions", str(self.metrics.fine_tuning_sessions))
        metrics_table.add_row("Avg Response Time", f"{self.metrics.avg_response_time:.3f}s")
        metrics_table.add_row("Total Cost", f"${self.metrics.total_cost:.6f}")
        metrics_table.add_row("Context Optimizations", str(self.metrics.context_optimizations))
        metrics_table.add_row("Uptime", f"{(time.time() - self.start_time):.1f}s")
        
        console.print(metrics_table)
        
        # Feature Status
        features_table = Table(title="Phase 4 Features")
        features_table.add_column("Feature", style="cyan")
        features_table.add_column("Status", style="green")
        
        for feature in Phase4Features:
            status = "✅ Enabled" if feature in self.config.enabled_features else "❌ Disabled"
            features_table.add_row(feature.value, status)
        
        console.print(features_table)
    
    async def run_diagnostic(self) -> Dict[str, Any]:
        """Run comprehensive diagnostic of Phase 4 features"""
        
        diagnostic = {
            'timestamp': time.time(),
            'phase4_config': {
                'enabled_features': [f.value for f in self.config.enabled_features],
                'auto_model_switching': self.config.auto_model_switching,
                'reasoning_enabled': self.config.reasoning_enabled,
                'fine_tuning_enabled': self.config.fine_tuning_enabled
            },
            'model_status': {
                'available_models': self.ai_model_manager.get_available_models(),
                'total_models': len(self.ai_model_manager.models)
            },
            'performance': {
                'avg_response_time': self.metrics.avg_response_time,
                'total_requests': self.metrics.total_requests,
                'success_rate': 1.0 if self.metrics.total_requests > 0 else 0.0
            },
            'cost_analysis': {
                'total_cost': self.metrics.total_cost,
                'avg_cost_per_request': self.metrics.total_cost / max(self.metrics.total_requests, 1)
            },
            'feature_usage': {
                'model_switches': self.metrics.model_switches,
                'reasoning_sessions': self.metrics.reasoning_sessions,
                'fine_tuning_sessions': self.metrics.fine_tuning_sessions
            }
        }
        
        return diagnostic
    
    def export_configuration(self) -> Dict[str, Any]:
        """Export current Phase 4 configuration"""
        return {
            'enabled_features': [f.value for f in self.config.enabled_features],
            'auto_model_switching': self.config.auto_model_switching,
            'reasoning_enabled': self.config.reasoning_enabled,
            'fine_tuning_enabled': self.config.fine_tuning_enabled,
            'context_optimization': self.config.context_optimization,
            'performance_monitoring': self.config.performance_monitoring
        }
    
    def import_configuration(self, config_data: Dict[str, Any]):
        """Import Phase 4 configuration"""
        if 'enabled_features' in config_data:
            self.config.enabled_features = [
                Phase4Features(f) for f in config_data['enabled_features']
            ]
        
        if 'auto_model_switching' in config_data:
            self.config.auto_model_switching = config_data['auto_model_switching']
        
        if 'reasoning_enabled' in config_data:
            self.config.reasoning_enabled = config_data['reasoning_enabled']
        
        if 'fine_tuning_enabled' in config_data:
            self.config.fine_tuning_enabled = config_data['fine_tuning_enabled']
        
        if 'context_optimization' in config_data:
            self.config.context_optimization = config_data['context_optimization']
        
        if 'performance_monitoring' in config_data:
            self.config.performance_monitoring = config_data['performance_monitoring']
        
        logger.info("Phase 4 configuration imported")