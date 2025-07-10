"""
Advanced AI Model Manager for JARVIS Phase 4

Provides multi-model architecture with dynamic model selection,
context optimization, and advanced reasoning capabilities.
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import json
import time

from rich.console import Console
from rich.table import Table

console = Console()
logger = logging.getLogger(__name__)


class ModelType(Enum):
    """Supported AI model types"""
    GPT_4 = "gpt-4"
    GPT_3_5 = "gpt-3.5-turbo"
    CLAUDE_3 = "claude-3"
    CLAUDE_2 = "claude-2"
    LOCAL_LLAMA = "llama-2"
    LOCAL_MISTRAL = "mistral"
    CUSTOM = "custom"


class TaskType(Enum):
    """Task types for model selection"""
    CONVERSATION = "conversation"
    CODE_GENERATION = "code_generation"
    ANALYSIS = "analysis"
    CREATIVE = "creative"
    REASONING = "reasoning"
    TRANSLATION = "translation"
    SUMMARIZATION = "summarization"


@dataclass
class ModelConfig:
    """Configuration for an AI model"""
    name: str
    model_type: ModelType
    api_key: Optional[str] = None
    endpoint: Optional[str] = None
    max_tokens: int = 4096
    temperature: float = 0.7
    context_window: int = 8192
    cost_per_token: float = 0.0
    capabilities: List[str] = None
    is_available: bool = True


@dataclass
class ModelResponse:
    """Response from an AI model"""
    content: str
    model_used: str
    tokens_used: int
    cost: float
    latency: float
    reasoning_steps: Optional[List[str]] = None
    confidence: float = 1.0


class BaseAIModel(ABC):
    """Base class for AI model implementations"""
    
    def __init__(self, config: ModelConfig):
        self.config = config
        self.name = config.name
        self.model_type = config.model_type
        
    @abstractmethod
    async def generate(self, prompt: str, context: Optional[str] = None) -> ModelResponse:
        """Generate response from the model"""
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        """Check if model is available"""
        pass
    
    def get_capabilities(self) -> List[str]:
        """Get model capabilities"""
        return self.config.capabilities or []


class GPTModel(BaseAIModel):
    """OpenAI GPT model implementation"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        self.client = None  # Will be initialized when needed
        
    async def generate(self, prompt: str, context: Optional[str] = None) -> ModelResponse:
        start_time = time.time()
        
        try:
            # Simulate OpenAI API call
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Simulate response generation
            await asyncio.sleep(0.1)  # Simulate API latency
            
            response_content = f"GPT Response to: {prompt[:50]}..."
            tokens_used = len(full_prompt.split()) + len(response_content.split())
            cost = tokens_used * self.config.cost_per_token
            
            return ModelResponse(
                content=response_content,
                model_used=self.name,
                tokens_used=tokens_used,
                cost=cost,
                latency=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Error generating response with {self.name}: {e}")
            raise
    
    async def is_available(self) -> bool:
        return self.config.is_available


class ClaudeModel(BaseAIModel):
    """Anthropic Claude model implementation"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        
    async def generate(self, prompt: str, context: Optional[str] = None) -> ModelResponse:
        start_time = time.time()
        
        try:
            # Simulate Claude API call
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Simulate response generation
            await asyncio.sleep(0.15)  # Simulate API latency
            
            response_content = f"Claude Response to: {prompt[:50]}..."
            tokens_used = len(full_prompt.split()) + len(response_content.split())
            cost = tokens_used * self.config.cost_per_token
            
            return ModelResponse(
                content=response_content,
                model_used=self.name,
                tokens_used=tokens_used,
                cost=cost,
                latency=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Error generating response with {self.name}: {e}")
            raise
    
    async def is_available(self) -> bool:
        return self.config.is_available


class LocalModel(BaseAIModel):
    """Local model implementation"""
    
    def __init__(self, config: ModelConfig):
        super().__init__(config)
        
    async def generate(self, prompt: str, context: Optional[str] = None) -> ModelResponse:
        start_time = time.time()
        
        try:
            # Simulate local model inference
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            # Simulate response generation
            await asyncio.sleep(0.5)  # Simulate local inference time
            
            response_content = f"Local Model Response to: {prompt[:50]}..."
            tokens_used = len(full_prompt.split()) + len(response_content.split())
            cost = 0.0  # Local models have no API cost
            
            return ModelResponse(
                content=response_content,
                model_used=self.name,
                tokens_used=tokens_used,
                cost=cost,
                latency=time.time() - start_time
            )
            
        except Exception as e:
            logger.error(f"Error generating response with {self.name}: {e}")
            raise
    
    async def is_available(self) -> bool:
        return self.config.is_available


class AdvancedAIModelManager:
    """Advanced AI Model Manager with multi-model support"""
    
    def __init__(self):
        self.models: Dict[str, BaseAIModel] = {}
        self.model_configs: Dict[str, ModelConfig] = {}
        self.task_model_mapping: Dict[TaskType, List[str]] = {}
        self.context_cache: Dict[str, str] = {}
        self.usage_stats: Dict[str, Dict] = {}
        
        # Initialize default models
        self._initialize_default_models()
        
    def _initialize_default_models(self):
        """Initialize default model configurations"""
        
        # GPT Models
        gpt4_config = ModelConfig(
            name="GPT-4",
            model_type=ModelType.GPT_4,
            max_tokens=8192,
            temperature=0.7,
            context_window=8192,
            cost_per_token=0.00003,
            capabilities=["conversation", "analysis", "reasoning", "creative"],
            is_available=True
        )
        
        gpt35_config = ModelConfig(
            name="GPT-3.5",
            model_type=ModelType.GPT_3_5,
            max_tokens=4096,
            temperature=0.7,
            context_window=4096,
            cost_per_token=0.000002,
            capabilities=["conversation", "analysis", "code_generation"],
            is_available=True
        )
        
        # Claude Models
        claude3_config = ModelConfig(
            name="Claude-3",
            model_type=ModelType.CLAUDE_3,
            max_tokens=4096,
            temperature=0.7,
            context_window=100000,
            cost_per_token=0.000015,
            capabilities=["conversation", "analysis", "reasoning", "creative"],
            is_available=True
        )
        
        # Local Models
        llama_config = ModelConfig(
            name="Llama-2",
            model_type=ModelType.LOCAL_LLAMA,
            max_tokens=4096,
            temperature=0.7,
            context_window=4096,
            cost_per_token=0.0,
            capabilities=["conversation", "analysis", "code_generation"],
            is_available=True
        )
        
        # Register models
        self.register_model(GPTModel(gpt4_config))
        self.register_model(GPTModel(gpt35_config))
        self.register_model(ClaudeModel(claude3_config))
        self.register_model(LocalModel(llama_config))
        
        # Setup task-model mapping
        self._setup_task_mapping()
        
    def _setup_task_mapping(self):
        """Setup mapping between task types and suitable models"""
        self.task_model_mapping = {
            TaskType.CONVERSATION: ["GPT-4", "Claude-3", "GPT-3.5"],
            TaskType.CODE_GENERATION: ["GPT-4", "GPT-3.5", "Llama-2"],
            TaskType.ANALYSIS: ["Claude-3", "GPT-4", "GPT-3.5"],
            TaskType.CREATIVE: ["GPT-4", "Claude-3"],
            TaskType.REASONING: ["Claude-3", "GPT-4"],
            TaskType.TRANSLATION: ["GPT-4", "GPT-3.5"],
            TaskType.SUMMARIZATION: ["Claude-3", "GPT-4"]
        }
        
    def register_model(self, model: BaseAIModel):
        """Register a new model"""
        self.models[model.name] = model
        self.model_configs[model.name] = model.config
        self.usage_stats[model.name] = {
            'total_requests': 0,
            'total_tokens': 0,
            'total_cost': 0.0,
            'avg_latency': 0.0
        }
        logger.info(f"Registered model: {model.name}")
        
    def get_available_models(self) -> List[str]:
        """Get list of available models"""
        return [name for name, model in self.models.items() 
                if model.config.is_available]
        
    def get_models_for_task(self, task_type: TaskType) -> List[str]:
        """Get suitable models for a specific task"""
        return self.task_model_mapping.get(task_type, [])
        
    async def select_best_model(self, task_type: TaskType, 
                               requirements: Dict[str, Any] = None) -> str:
        """Select the best model for a given task"""
        
        available_models = self.get_models_for_task(task_type)
        if not available_models:
            # Fallback to any available model
            available_models = self.get_available_models()
            
        if not available_models:
            raise ValueError("No available models found")
            
        # Simple selection logic - can be enhanced with ML
        if requirements and requirements.get('cost_sensitive'):
            # Choose cheapest available model
            return min(available_models, 
                      key=lambda m: self.model_configs[m].cost_per_token)
        elif requirements and requirements.get('speed_sensitive'):
            # Choose fastest available model (local models)
            local_models = [m for m in available_models 
                          if self.model_configs[m].model_type in 
                          [ModelType.LOCAL_LLAMA, ModelType.LOCAL_MISTRAL]]
            return local_models[0] if local_models else available_models[0]
        else:
            # Choose first available model
            return available_models[0]
            
    async def generate_response(self, prompt: str, 
                              task_type: TaskType = TaskType.CONVERSATION,
                              context: Optional[str] = None,
                              model_name: Optional[str] = None,
                              requirements: Dict[str, Any] = None) -> ModelResponse:
        """Generate response using the best available model"""
        
        # Select model
        if model_name:
            if model_name not in self.models:
                raise ValueError(f"Model {model_name} not found")
            selected_model = model_name
        else:
            selected_model = await self.select_best_model(task_type, requirements)
            
        # Get model instance
        model = self.models[selected_model]
        
        # Generate response
        response = await model.generate(prompt, context)
        
        # Update usage statistics
        self._update_usage_stats(selected_model, response)
        
        return response
        
    def _update_usage_stats(self, model_name: str, response: ModelResponse):
        """Update usage statistics for a model"""
        stats = self.usage_stats[model_name]
        stats['total_requests'] += 1
        stats['total_tokens'] += response.tokens_used
        stats['total_cost'] += response.cost
        
        # Update average latency
        current_avg = stats['avg_latency']
        total_requests = stats['total_requests']
        stats['avg_latency'] = (current_avg * (total_requests - 1) + response.latency) / total_requests
        
    def get_usage_stats(self) -> Dict[str, Dict]:
        """Get usage statistics for all models"""
        return self.usage_stats.copy()
        
    def optimize_context(self, context: str, max_tokens: int = 1000) -> str:
        """Optimize context for token efficiency"""
        if len(context.split()) <= max_tokens:
            return context
            
        # Simple truncation - can be enhanced with semantic compression
        words = context.split()
        return ' '.join(words[:max_tokens])
        
    def display_model_status(self):
        """Display current model status"""
        table = Table(title="AI Model Status")
        table.add_column("Model", style="cyan")
        table.add_column("Type", style="magenta")
        table.add_column("Status", style="green")
        table.add_column("Cost/Token", style="yellow")
        table.add_column("Requests", style="blue")
        table.add_column("Avg Latency", style="red")
        
        for name, model in self.models.items():
            stats = self.usage_stats[name]
            status = "🟢 Available" if model.config.is_available else "🔴 Unavailable"
            
            table.add_row(
                name,
                model.config.model_type.value,
                status,
                f"${model.config.cost_per_token:.6f}",
                str(stats['total_requests']),
                f"{stats['avg_latency']:.3f}s"
            )
            
        console.print(table)