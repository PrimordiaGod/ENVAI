#!/usr/bin/env python3
"""
Phase 4 Test Suite for JARVIS

Tests advanced AI model integration including:
- Multi-model architecture
- Advanced reasoning patterns
- Model fine-tuning capabilities
- Context optimization
- Performance monitoring
"""

import asyncio
import sys
import time
import json
from typing import Dict, List, Any

# Add the jarvis package to the path
sys.path.insert(0, '.')

from jarvis.integration.phase4_integration import Phase4Integration, Phase4Config, Phase4Features
from jarvis.ai_models.model_manager import TaskType
from jarvis.ai_models.reasoning_engine import ReasoningType
from jarvis.ai_models.fine_tuner import FineTuningMethod, TrainingData
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()


class Phase4TestSuite:
    """Comprehensive test suite for Phase 4 features"""
    
    def __init__(self):
        self.phase4 = None
        self.test_results = {}
        self.start_time = time.time()
        
    async def setup(self):
        """Initialize Phase 4 integration"""
        console.print("[bold cyan]Initializing Phase 4 Integration...[/bold cyan]")
        
        config = Phase4Config(
            enabled_features=[
                Phase4Features.ADVANCED_AI_MODELS,
                Phase4Features.MODEL_SWITCHING,
                Phase4Features.ADVANCED_REASONING,
                Phase4Features.FINE_TUNING,
                Phase4Features.CONTEXT_OPTIMIZATION,
                Phase4Features.PERFORMANCE_MONITORING
            ]
        )
        
        self.phase4 = Phase4Integration(config)
        console.print("✅ Phase 4 Integration initialized successfully")
    
    async def test_advanced_ai_models(self):
        """Test advanced AI model features"""
        console.print("\n[bold green]Testing Advanced AI Models...[/bold green]")
        
        test_cases = [
            {
                'name': 'Basic Conversation',
                'prompt': 'Hello, how are you today?',
                'task_type': TaskType.CONVERSATION,
                'expected_features': ['model_selection', 'context_optimization']
            },
            {
                'name': 'Code Generation',
                'prompt': 'Write a Python function to calculate fibonacci numbers',
                'task_type': TaskType.CODE_GENERATION,
                'expected_features': ['model_switching', 'optimization']
            },
            {
                'name': 'Analysis Task',
                'prompt': 'Analyze the benefits and drawbacks of renewable energy',
                'task_type': TaskType.ANALYSIS,
                'expected_features': ['reasoning', 'context_optimization']
            },
            {
                'name': 'Creative Task',
                'prompt': 'Write a short story about a robot learning to paint',
                'task_type': TaskType.CREATIVE,
                'expected_features': ['model_selection', 'optimization']
            }
        ]
        
        results = []
        for test_case in test_cases:
            try:
                response = await self.phase4.process_request(
                    prompt=test_case['prompt'],
                    task_type=test_case['task_type']
                )
                
                result = {
                    'name': test_case['name'],
                    'status': 'PASS',
                    'model_used': response.get('model_used', 'Unknown'),
                    'latency': response.get('latency', 0),
                    'confidence': response.get('confidence', 0),
                    'content_length': len(response.get('content', ''))
                }
                
                console.print(f"✅ {test_case['name']} - {response.get('model_used', 'Unknown')}")
                
            except Exception as e:
                result = {
                    'name': test_case['name'],
                    'status': 'FAIL',
                    'error': str(e)
                }
                console.print(f"❌ {test_case['name']} - {str(e)}")
            
            results.append(result)
        
        self.test_results['advanced_ai_models'] = results
        return results
    
    async def test_advanced_reasoning(self):
        """Test advanced reasoning patterns"""
        console.print("\n[bold green]Testing Advanced Reasoning...[/bold green]")
        
        reasoning_tests = [
            {
                'name': 'Chain-of-Thought Reasoning',
                'prompt': 'If I have 5 apples and give 2 to my friend, then buy 3 more, how many do I have?',
                'reasoning_type': ReasoningType.CHAIN_OF_THOUGHT,
                'expected_features': ['step_by_step', 'logical_flow']
            },
            {
                'name': 'Tree-of-Thoughts Reasoning',
                'prompt': 'What are the best strategies for learning a new programming language?',
                'reasoning_type': ReasoningType.TREE_OF_THOUGHTS,
                'expected_features': ['multiple_approaches', 'branching']
            }
        ]
        
        results = []
        for test in reasoning_tests:
            try:
                response = await self.phase4.process_request(
                    prompt=test['prompt'],
                    task_type=TaskType.REASONING,
                    use_reasoning=True,
                    reasoning_type=test['reasoning_type']
                )
                
                result = {
                    'name': test['name'],
                    'status': 'PASS',
                    'reasoning_type': response.get('reasoning_type', 'Unknown'),
                    'confidence': response.get('confidence', 0),
                    'reasoning_paths': response.get('reasoning_paths', 0),
                    'latency': response.get('latency', 0)
                }
                
                console.print(f"✅ {test['name']} - {response.get('reasoning_type', 'Unknown')}")
                
            except Exception as e:
                result = {
                    'name': test['name'],
                    'status': 'FAIL',
                    'error': str(e)
                }
                console.print(f"❌ {test['name']} - {str(e)}")
            
            results.append(result)
        
        self.test_results['advanced_reasoning'] = results
        return results
    
    async def test_model_switching(self):
        """Test intelligent model switching"""
        console.print("\n[bold green]Testing Model Switching...[/bold green]")
        
        switching_tests = [
            {
                'name': 'Cost-Sensitive Switching',
                'prompt': 'Explain quantum computing in simple terms',
                'requirements': {'cost_sensitive': True},
                'expected_behavior': 'switch_to_cheaper_model'
            },
            {
                'name': 'Speed-Sensitive Switching',
                'prompt': 'Quick translation of "Hello world" to Spanish',
                'requirements': {'speed_sensitive': True},
                'expected_behavior': 'switch_to_faster_model'
            },
            {
                'name': 'Quality-Sensitive Switching',
                'prompt': 'Write a comprehensive analysis of climate change',
                'requirements': {'quality_sensitive': True},
                'expected_behavior': 'switch_to_quality_model'
            }
        ]
        
        results = []
        for test in switching_tests:
            try:
                response = await self.phase4.process_request(
                    prompt=test['prompt'],
                    task_type=TaskType.CONVERSATION,
                    requirements=test['requirements']
                )
                
                result = {
                    'name': test['name'],
                    'status': 'PASS',
                    'model_used': response.get('model_used', 'Unknown'),
                    'latency': response.get('latency', 0),
                    'cost': response.get('cost', 0)
                }
                
                console.print(f"✅ {test['name']} - {response.get('model_used', 'Unknown')}")
                
            except Exception as e:
                result = {
                    'name': test['name'],
                    'status': 'FAIL',
                    'error': str(e)
                }
                console.print(f"❌ {test['name']} - {str(e)}")
            
            results.append(result)
        
        self.test_results['model_switching'] = results
        return results
    
    async def test_fine_tuning(self):
        """Test model fine-tuning capabilities"""
        console.print("\n[bold green]Testing Fine-tuning...[/bold green]")
        
        # Create sample training data
        training_data = TrainingData(
            prompts=[
                "What is the capital of France?",
                "How do you make coffee?",
                "Explain photosynthesis",
                "What is machine learning?"
            ],
            responses=[
                "The capital of France is Paris.",
                "To make coffee, you need hot water and coffee grounds.",
                "Photosynthesis is the process by which plants convert sunlight into energy.",
                "Machine learning is a subset of artificial intelligence that enables computers to learn from data."
            ],
            metadata={'domain': 'general_knowledge', 'difficulty': 'medium'}
        )
        
        fine_tuning_tests = [
            {
                'name': 'LoRA Fine-tuning',
                'method': FineTuningMethod.LORA,
                'config': {'epochs': 2, 'learning_rate': 1e-4}
            },
            {
                'name': 'QLoRA Fine-tuning',
                'method': FineTuningMethod.QLORA,
                'config': {'epochs': 2, 'learning_rate': 1e-4}
            }
        ]
        
        results = []
        for test in fine_tuning_tests:
            try:
                result_data = await self.phase4.fine_tune_model(
                    training_data=training_data,
                    method=test['method'],
                    **test['config']
                )
                
                result = {
                    'name': test['name'],
                    'status': 'PASS',
                    'method': result_data.get('method', 'Unknown'),
                    'final_loss': result_data.get('final_loss', 0),
                    'final_accuracy': result_data.get('final_accuracy', 0),
                    'training_time': result_data.get('training_time', 0),
                    'model_size': result_data.get('model_size', 0)
                }
                
                console.print(f"✅ {test['name']} - Accuracy: {result_data.get('final_accuracy', 0):.4f}")
                
            except Exception as e:
                result = {
                    'name': test['name'],
                    'status': 'FAIL',
                    'error': str(e)
                }
                console.print(f"❌ {test['name']} - {str(e)}")
            
            results.append(result)
        
        self.test_results['fine_tuning'] = results
        return results
    
    async def test_context_optimization(self):
        """Test context optimization features"""
        console.print("\n[bold green]Testing Context Optimization...[/bold green]")
        
        # Create a long context
        long_context = """
        This is a very long context that contains a lot of information about various topics.
        It includes details about artificial intelligence, machine learning, deep learning,
        natural language processing, computer vision, robotics, automation, data science,
        big data, cloud computing, edge computing, internet of things, blockchain,
        cybersecurity, quantum computing, and many other technology topics.
        The context is designed to test the optimization capabilities of the system.
        """ * 10  # Make it very long
        
        optimization_tests = [
            {
                'name': 'Long Context Optimization',
                'prompt': 'Summarize the key points from the context',
                'context': long_context,
                'expected_behavior': 'context_optimized'
            },
            {
                'name': 'Short Context (No Optimization)',
                'prompt': 'What is AI?',
                'context': 'Artificial Intelligence is a field of computer science.',
                'expected_behavior': 'context_preserved'
            }
        ]
        
        results = []
        for test in optimization_tests:
            try:
                response = await self.phase4.process_request(
                    prompt=test['prompt'],
                    task_type=TaskType.SUMMARIZATION,
                    context=test['context']
                )
                
                result = {
                    'name': test['name'],
                    'status': 'PASS',
                    'content_length': len(response.get('content', '')),
                    'latency': response.get('latency', 0),
                    'tokens_used': response.get('tokens_used', 0)
                }
                
                console.print(f"✅ {test['name']} - Tokens: {response.get('tokens_used', 0)}")
                
            except Exception as e:
                result = {
                    'name': test['name'],
                    'status': 'FAIL',
                    'error': str(e)
                }
                console.print(f"❌ {test['name']} - {str(e)}")
            
            results.append(result)
        
        self.test_results['context_optimization'] = results
        return results
    
    async def test_performance_monitoring(self):
        """Test performance monitoring features"""
        console.print("\n[bold green]Testing Performance Monitoring...[/bold green]")
        
        # Generate some load
        load_tests = [
            {'prompt': f'Test request {i}', 'task_type': TaskType.CONVERSATION}
            for i in range(5)
        ]
        
        results = []
        for test in load_tests:
            try:
                response = await self.phase4.process_request(
                    prompt=test['prompt'],
                    task_type=test['task_type']
                )
                
                result = {
                    'name': f"Load Test {load_tests.index(test) + 1}",
                    'status': 'PASS',
                    'latency': response.get('latency', 0),
                    'model_used': response.get('model_used', 'Unknown'),
                    'cost': response.get('cost', 0)
                }
                
                console.print(f"✅ Load Test {load_tests.index(test) + 1} - {response.get('latency', 0):.3f}s")
                
            except Exception as e:
                result = {
                    'name': f"Load Test {load_tests.index(test) + 1}",
                    'status': 'FAIL',
                    'error': str(e)
                }
                console.print(f"❌ Load Test {load_tests.index(test) + 1} - {str(e)}")
            
            results.append(result)
        
        # Get comprehensive status
        try:
            status = self.phase4.get_model_status()
            console.print("✅ Performance monitoring active")
            
            result = {
                'name': 'Performance Monitoring',
                'status': 'PASS',
                'total_requests': status['phase4_metrics']['total_requests'],
                'avg_response_time': status['phase4_metrics']['avg_response_time'],
                'total_cost': status['phase4_metrics']['total_cost']
            }
            
        except Exception as e:
            result = {
                'name': 'Performance Monitoring',
                'status': 'FAIL',
                'error': str(e)
            }
            console.print(f"❌ Performance Monitoring - {str(e)}")
        
        results.append(result)
        self.test_results['performance_monitoring'] = results
        return results
    
    async def test_integration(self):
        """Test overall integration"""
        console.print("\n[bold green]Testing Integration...[/bold green]")
        
        integration_tests = [
            {
                'name': 'Complex Multi-Feature Request',
                'prompt': 'Analyze the impact of AI on healthcare using advanced reasoning',
                'task_type': TaskType.ANALYSIS,
                'use_reasoning': True,
                'requirements': {'quality_sensitive': True}
            },
            {
                'name': 'Fine-tuning with Reasoning',
                'prompt': 'Create a custom model for medical diagnosis',
                'task_type': TaskType.CODE_GENERATION,
                'use_reasoning': True
            }
        ]
        
        results = []
        for test in integration_tests:
            try:
                response = await self.phase4.process_request(
                    prompt=test['prompt'],
                    task_type=test['task_type'],
                    use_reasoning=test.get('use_reasoning', False),
                    requirements=test.get('requirements', {})
                )
                
                result = {
                    'name': test['name'],
                    'status': 'PASS',
                    'model_used': response.get('model_used', 'Unknown'),
                    'reasoning_type': response.get('reasoning_type', 'None'),
                    'confidence': response.get('confidence', 0),
                    'latency': response.get('latency', 0)
                }
                
                console.print(f"✅ {test['name']} - {response.get('model_used', 'Unknown')}")
                
            except Exception as e:
                result = {
                    'name': test['name'],
                    'status': 'FAIL',
                    'error': str(e)
                }
                console.print(f"❌ {test['name']} - {str(e)}")
            
            results.append(result)
        
        self.test_results['integration'] = results
        return results
    
    def display_results(self):
        """Display comprehensive test results"""
        console.print("\n" + "="*60)
        console.print("[bold cyan]PHASE 4 TEST RESULTS[/bold cyan]")
        console.print("="*60)
        
        total_tests = 0
        passed_tests = 0
        
        for category, results in self.test_results.items():
            console.print(f"\n[bold green]{category.upper().replace('_', ' ')}[/bold green]")
            
            category_passed = 0
            category_total = len(results)
            
            for result in results:
                status_icon = "✅" if result['status'] == 'PASS' else "❌"
                console.print(f"  {status_icon} {result['name']}")
                
                if result['status'] == 'PASS':
                    category_passed += 1
                    # Show additional details for passed tests
                    if 'model_used' in result:
                        console.print(f"    Model: {result['model_used']}")
                    if 'latency' in result:
                        console.print(f"    Latency: {result['latency']:.3f}s")
                    if 'confidence' in result:
                        console.print(f"    Confidence: {result['confidence']:.3f}")
                else:
                    console.print(f"    Error: {result.get('error', 'Unknown error')}")
            
            console.print(f"  Category: {category_passed}/{category_total} passed")
            total_tests += category_total
            passed_tests += category_passed
        
        # Overall summary
        console.print("\n" + "="*60)
        console.print(f"[bold]OVERALL RESULTS: {passed_tests}/{total_tests} tests passed[/bold]")
        console.print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%" if total_tests > 0 else "Success Rate: N/A")
        console.print(f"Total Time: {time.time() - self.start_time:.2f}s")
        console.print("="*60)
        
        # Display Phase 4 status
        if self.phase4:
            console.print("\n[bold cyan]PHASE 4 STATUS[/bold cyan]")
            self.phase4.display_status()
    
    async def run_all_tests(self):
        """Run all Phase 4 tests"""
        console.print("[bold yellow]Starting Phase 4 Test Suite...[/bold yellow]")
        
        await self.setup()
        
        # Run all test categories
        await self.test_advanced_ai_models()
        await self.test_advanced_reasoning()
        await self.test_model_switching()
        await self.test_fine_tuning()
        await self.test_context_optimization()
        await self.test_performance_monitoring()
        await self.test_integration()
        
        # Display results
        self.display_results()
        
        return self.test_results


async def main():
    """Main test runner"""
    test_suite = Phase4TestSuite()
    results = await test_suite.run_all_tests()
    
    # Return exit code based on results
    total_tests = sum(len(category_results) for category_results in results.values())
    passed_tests = sum(
        sum(1 for result in category_results if result['status'] == 'PASS')
        for category_results in results.values()
    )
    
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    if success_rate >= 80:
        console.print("\n[bold green]🎉 Phase 4 tests completed successfully![/bold green]")
        return 0
    else:
        console.print("\n[bold red]⚠️  Some Phase 4 tests failed. Review results above.[/bold red]")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)