"""
Advanced Reasoning Engine for JARVIS Phase 4

Provides advanced reasoning patterns including:
- Chain-of-thought reasoning
- Tree-of-thoughts reasoning
- Multi-step reasoning
- Confidence estimation
- Reasoning validation
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass
from enum import Enum
import json
import time
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ReasoningType(Enum):
    """Types of reasoning patterns"""
    CHAIN_OF_THOUGHT = "chain_of_thought"
    TREE_OF_THOUGHTS = "tree_of_thoughts"
    MULTI_STEP = "multi_step"
    BACKWARD_CHAINING = "backward_chaining"
    ANALOGICAL = "analogical"
    DEDUCTIVE = "deductive"


@dataclass
class ReasoningStep:
    """A single step in the reasoning process"""
    step_id: str
    thought: str
    reasoning_type: ReasoningType
    confidence: float
    evidence: List[str]
    next_steps: List[str]
    timestamp: float


@dataclass
class ReasoningPath:
    """A complete reasoning path"""
    path_id: str
    steps: List[ReasoningStep]
    final_answer: str
    confidence: float
    reasoning_type: ReasoningType
    total_time: float


@dataclass
class ReasoningResult:
    """Result of advanced reasoning"""
    answer: str
    confidence: float
    reasoning_paths: List[ReasoningPath]
    best_path: ReasoningPath
    reasoning_type: ReasoningType
    metadata: Dict[str, Any]


class BaseReasoningPattern(ABC):
    """Base class for reasoning patterns"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.reasoning_type: ReasoningType = None
        
    @abstractmethod
    async def reason(self, question: str, context: Optional[str] = None) -> ReasoningResult:
        """Execute reasoning pattern"""
        pass
    
    @abstractmethod
    def validate_reasoning(self, reasoning_path: ReasoningPath) -> bool:
        """Validate the reasoning path"""
        pass


class ChainOfThoughtReasoning(BaseReasoningPattern):
    """Chain-of-thought reasoning implementation"""
    
    def __init__(self, model_manager):
        super().__init__(model_manager)
        self.reasoning_type = ReasoningType.CHAIN_OF_THOUGHT
        
    async def reason(self, question: str, context: Optional[str] = None) -> ReasoningResult:
        """Execute chain-of-thought reasoning"""
        start_time = time.time()
        
        # Generate reasoning prompt
        reasoning_prompt = self._create_reasoning_prompt(question, context)
        
        # Get response from model
        from .model_manager import TaskType
        response = await self.model_manager.generate_response(
            reasoning_prompt,
            task_type=TaskType.REASONING,
            context=context
        )
        
        # Parse reasoning steps
        steps = self._parse_reasoning_steps(response.content)
        
        # Create reasoning path
        reasoning_path = ReasoningPath(
            path_id=f"cot_{int(time.time())}",
            steps=steps,
            final_answer=self._extract_final_answer(response.content),
            confidence=self._calculate_confidence(steps),
            reasoning_type=self.reasoning_type,
            total_time=time.time() - start_time
        )
        
        return ReasoningResult(
            answer=reasoning_path.final_answer,
            confidence=reasoning_path.confidence,
            reasoning_paths=[reasoning_path],
            best_path=reasoning_path,
            reasoning_type=self.reasoning_type,
            metadata={'steps_count': len(steps)}
        )
    
    def _create_reasoning_prompt(self, question: str, context: Optional[str] = None) -> str:
        """Create a chain-of-thought reasoning prompt"""
        prompt = f"""
Let's approach this step by step:

Question: {question}

{context if context else ''}

Please think through this step by step, showing your reasoning process:

"""
        return prompt
    
    def _parse_reasoning_steps(self, response: str) -> List[ReasoningStep]:
        """Parse reasoning steps from response"""
        steps = []
        lines = response.split('\n')
        current_step = None
        step_counter = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for step indicators
            if any(indicator in line.lower() for indicator in ['step', 'thought', 'reasoning']):
                if current_step:
                    steps.append(current_step)
                
                step_counter += 1
                current_step = ReasoningStep(
                    step_id=f"step_{step_counter}",
                    thought=line,
                    reasoning_type=self.reasoning_type,
                    confidence=0.8,  # Default confidence
                    evidence=[],
                    next_steps=[],
                    timestamp=time.time()
                )
            elif current_step:
                current_step.thought += f" {line}"
        
        if current_step:
            steps.append(current_step)
        
        return steps
    
    def _extract_final_answer(self, response: str) -> str:
        """Extract final answer from response"""
        # Look for answer indicators
        answer_indicators = ['answer:', 'conclusion:', 'therefore:', 'final answer:']
        
        lines = response.split('\n')
        for line in reversed(lines):
            line = line.strip().lower()
            for indicator in answer_indicators:
                if indicator in line:
                    return line.split(indicator, 1)[1].strip()
        
        # Fallback: return last non-empty line
        for line in reversed(lines):
            if line.strip():
                return line.strip()
        
        return "No clear answer found"
    
    def _calculate_confidence(self, steps: List[ReasoningStep]) -> float:
        """Calculate confidence based on reasoning steps"""
        if not steps:
            return 0.0
        
        # Simple confidence calculation
        avg_step_confidence = sum(step.confidence for step in steps) / len(steps)
        step_count_factor = min(len(steps) / 5, 1.0)  # More steps = higher confidence
        
        return min(0.95, avg_step_confidence * step_count_factor)
    
    def validate_reasoning(self, reasoning_path: ReasoningPath) -> bool:
        """Validate chain-of-thought reasoning"""
        if not reasoning_path.steps:
            return False
        
        # Check for logical flow
        for i, step in enumerate(reasoning_path.steps):
            if not step.thought.strip():
                return False
            
            # Check if step builds on previous steps
            if i > 0:
                prev_step = reasoning_path.steps[i-1]
                if not any(word in step.thought.lower() for word in prev_step.thought.lower().split()[:5]):
                    return False
        
        return True


class TreeOfThoughtsReasoning(BaseReasoningPattern):
    """Tree-of-thoughts reasoning implementation"""
    
    def __init__(self, model_manager, max_branches: int = 5, max_depth: int = 3):
        super().__init__(model_manager)
        self.reasoning_type = ReasoningType.TREE_OF_THOUGHTS
        self.max_branches = max_branches
        self.max_depth = max_depth
        
    async def reason(self, question: str, context: Optional[str] = None) -> ReasoningResult:
        """Execute tree-of-thoughts reasoning"""
        start_time = time.time()
        
        # Generate initial thoughts
        initial_thoughts = await self._generate_initial_thoughts(question, context)
        
        # Build reasoning tree
        reasoning_tree = await self._build_reasoning_tree(question, initial_thoughts, context)
        
        # Find best path
        best_path = await self._find_best_path(reasoning_tree)
        
        return ReasoningResult(
            answer=best_path.final_answer,
            confidence=best_path.confidence,
            reasoning_paths=[best_path],
            best_path=best_path,
            reasoning_type=self.reasoning_type,
            metadata={'tree_depth': len(best_path.steps), 'total_branches': len(reasoning_tree)}
        )
    
    async def _generate_initial_thoughts(self, question: str, context: Optional[str] = None) -> List[str]:
        """Generate initial thoughts for the question"""
        prompt = f"""
Given this question: {question}

{context if context else ''}

Generate {self.max_branches} different initial approaches or thoughts to solve this problem. 
Each should be a different perspective or strategy.

"""
        
        response = await self.model_manager.generate_response(
            prompt,
            task_type=self.model_manager.TaskType.REASONING,
            context=context
        )
        
        # Parse thoughts from response
        thoughts = []
        lines = response.content.split('\n')
        for line in lines:
            line = line.strip()
            if line and any(indicator in line.lower() for indicator in ['approach', 'thought', 'strategy', 'perspective']):
                thoughts.append(line)
        
        return thoughts[:self.max_branches]
    
    async def _build_reasoning_tree(self, question: str, initial_thoughts: List[str], context: Optional[str] = None) -> List[ReasoningPath]:
        """Build a tree of reasoning paths"""
        all_paths = []
        
        for i, thought in enumerate(initial_thoughts):
            path = await self._develop_thought_path(question, thought, context, depth=0)
            all_paths.append(path)
        
        return all_paths
    
    async def _develop_thought_path(self, question: str, thought: str, context: Optional[str] = None, depth: int = 0) -> ReasoningPath:
        """Develop a single thought path"""
        if depth >= self.max_depth:
            # Create final step
            final_step = ReasoningStep(
                step_id=f"final_{depth}",
                thought=thought,
                reasoning_type=self.reasoning_type,
                confidence=0.7,
                evidence=[],
                next_steps=[],
                timestamp=time.time()
            )
            
            return ReasoningPath(
                path_id=f"tot_{int(time.time())}_{depth}",
                steps=[final_step],
                final_answer=self._extract_answer_from_thought(thought),
                confidence=0.7,
                reasoning_type=self.reasoning_type,
                total_time=0.0
            )
        
        # Generate next thoughts
        next_thoughts = await self._generate_next_thoughts(question, thought, context)
        
        # Create current step
        current_step = ReasoningStep(
            step_id=f"step_{depth}",
            thought=thought,
            reasoning_type=self.reasoning_type,
            confidence=0.8,
            evidence=[],
            next_steps=next_thoughts,
            timestamp=time.time()
        )
        
        # Recursively develop paths
        best_sub_path = None
        best_confidence = 0.0
        
        for next_thought in next_thoughts[:2]:  # Limit branches
            sub_path = await self._develop_thought_path(question, next_thought, context, depth + 1)
            if sub_path.confidence > best_confidence:
                best_confidence = sub_path.confidence
                best_sub_path = sub_path
        
        if best_sub_path:
            steps = [current_step] + best_sub_path.steps
            return ReasoningPath(
                path_id=best_sub_path.path_id,
                steps=steps,
                final_answer=best_sub_path.final_answer,
                confidence=best_confidence * 0.9,  # Slight penalty for depth
                reasoning_type=self.reasoning_type,
                total_time=0.0
            )
        else:
            return ReasoningPath(
                path_id=f"tot_{int(time.time())}_{depth}",
                steps=[current_step],
                final_answer=self._extract_answer_from_thought(thought),
                confidence=0.6,
                reasoning_type=self.reasoning_type,
                total_time=0.0
            )
    
    async def _generate_next_thoughts(self, question: str, current_thought: str, context: Optional[str] = None) -> List[str]:
        """Generate next thoughts based on current thought"""
        prompt = f"""
Question: {question}

Current thought: {current_thought}

{context if context else ''}

Based on this current thought, generate 2-3 next logical steps or considerations to further develop this line of reasoning.

"""
        
        response = await self.model_manager.generate_response(
            prompt,
            task_type=self.model_manager.TaskType.REASONING,
            context=context
        )
        
        # Parse next thoughts
        thoughts = []
        lines = response.content.split('\n')
        for line in lines:
            line = line.strip()
            if line and len(line) > 10:
                thoughts.append(line)
        
        return thoughts[:3]
    
    def _extract_answer_from_thought(self, thought: str) -> str:
        """Extract answer from a thought"""
        # Look for conclusion indicators
        conclusion_indicators = ['therefore', 'thus', 'conclusion', 'answer is', 'result is']
        
        thought_lower = thought.lower()
        for indicator in conclusion_indicators:
            if indicator in thought_lower:
                parts = thought.split(indicator, 1)
                if len(parts) > 1:
                    return parts[1].strip()
        
        return thought
    
    async def _find_best_path(self, paths: List[ReasoningPath]) -> ReasoningPath:
        """Find the best reasoning path"""
        if not paths:
            raise ValueError("No reasoning paths available")
        
        # Sort by confidence
        sorted_paths = sorted(paths, key=lambda p: p.confidence, reverse=True)
        return sorted_paths[0]
    
    def validate_reasoning(self, reasoning_path: ReasoningPath) -> bool:
        """Validate tree-of-thoughts reasoning"""
        if not reasoning_path.steps:
            return False
        
        # Check for logical progression
        for i, step in enumerate(reasoning_path.steps):
            if not step.thought.strip():
                return False
            
            # Check if step has next steps (except final step)
            if i < len(reasoning_path.steps) - 1 and not step.next_steps:
                return False
        
        return True


class AdvancedReasoningEngine:
    """Advanced reasoning engine with multiple reasoning patterns"""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.reasoning_patterns: Dict[ReasoningType, BaseReasoningPattern] = {}
        self.reasoning_history: List[ReasoningResult] = []
        
        # Initialize reasoning patterns
        self._initialize_patterns()
    
    def _initialize_patterns(self):
        """Initialize available reasoning patterns"""
        self.reasoning_patterns[ReasoningType.CHAIN_OF_THOUGHT] = ChainOfThoughtReasoning(self.model_manager)
        self.reasoning_patterns[ReasoningType.TREE_OF_THOUGHTS] = TreeOfThoughtsReasoning(self.model_manager)
    
    async def reason(self, question: str, 
                    reasoning_type: ReasoningType = ReasoningType.CHAIN_OF_THOUGHT,
                    context: Optional[str] = None) -> ReasoningResult:
        """Execute reasoning with specified pattern"""
        
        if reasoning_type not in self.reasoning_patterns:
            raise ValueError(f"Reasoning type {reasoning_type} not supported")
        
        pattern = self.reasoning_patterns[reasoning_type]
        result = await pattern.reason(question, context)
        
        # Validate reasoning
        if not pattern.validate_reasoning(result.best_path):
            logger.warning(f"Reasoning validation failed for {reasoning_type}")
            result.confidence *= 0.8  # Reduce confidence
        
        # Store in history
        self.reasoning_history.append(result)
        
        return result
    
    async def multi_pattern_reasoning(self, question: str, 
                                   patterns: List[ReasoningType] = None,
                                   context: Optional[str] = None) -> ReasoningResult:
        """Execute multiple reasoning patterns and combine results"""
        
        if patterns is None:
            patterns = [ReasoningType.CHAIN_OF_THOUGHT, ReasoningType.TREE_OF_THOUGHTS]
        
        results = []
        for pattern_type in patterns:
            try:
                result = await self.reason(question, pattern_type, context)
                results.append(result)
            except Exception as e:
                logger.error(f"Error in {pattern_type} reasoning: {e}")
        
        if not results:
            raise ValueError("No reasoning patterns succeeded")
        
        # Combine results
        return self._combine_reasoning_results(results)
    
    def _combine_reasoning_results(self, results: List[ReasoningResult]) -> ReasoningResult:
        """Combine multiple reasoning results"""
        if len(results) == 1:
            return results[0]
        
        # Find best result by confidence
        best_result = max(results, key=lambda r: r.confidence)
        
        # Combine all reasoning paths
        all_paths = []
        for result in results:
            all_paths.extend(result.reasoning_paths)
        
        # Calculate combined confidence
        avg_confidence = sum(r.confidence for r in results) / len(results)
        
        return ReasoningResult(
            answer=best_result.answer,
            confidence=avg_confidence,
            reasoning_paths=all_paths,
            best_path=best_result.best_path,
            reasoning_type=ReasoningType.CHAIN_OF_THOUGHT,  # Default
            metadata={'patterns_used': len(results), 'individual_results': results}
        )
    
    def get_reasoning_history(self, limit: int = 10) -> List[ReasoningResult]:
        """Get recent reasoning history"""
        return self.reasoning_history[-limit:] if self.reasoning_history else []
    
    def get_reasoning_statistics(self) -> Dict[str, Any]:
        """Get statistics about reasoning usage"""
        if not self.reasoning_history:
            return {}
        
        stats = {}
        for result in self.reasoning_history:
            reasoning_type = result.reasoning_type.value
            stats[reasoning_type] = stats.get(reasoning_type, 0) + 1
        
        return {
            'total_reasoning_sessions': len(self.reasoning_history),
            'reasoning_type_distribution': stats,
            'avg_confidence': sum(r.confidence for r in self.reasoning_history) / len(self.reasoning_history)
        }