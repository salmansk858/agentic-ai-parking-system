"""
Base agent class implementing common functionality.
Based on OpenAI Agents SDK with research optimizations.
"""
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
import asyncio
import logging
from agents import Agent, Runner
from ..config.settings import ModelConfig, settings

logger = logging.getLogger(__name__)

class BaseAgentError(Exception):
    """Base exception for agent errors."""
    pass

class BaseAgent(ABC):
    """
    Base agent class with common functionality.
    Implements Chain-of-Thought reasoning and guardrails.
    """
    
    def __init__(self, name: str, instructions: str, model_config: ModelConfig, tools: List[str] = None):
        self.name = name
        self.instructions = instructions
        self.model_config = model_config
        self.tools = tools or []
        self.agent = None
        self._initialize_agent()
        
    def _initialize_agent(self):
        """Initialize the OpenAI Agent with optimized configuration."""
        try:
            self.agent = Agent(
                name=self.name,
                instructions=self._enhance_instructions_with_cot(),
                model=self.model_config.model,
                temperature=self.model_config.temperature,
                max_tokens=self.model_config.max_tokens,
                top_p=self.model_config.top_p,
                tools=self._get_tool_functions()
            )
            logger.info(f"Initialized agent: {self.name}")
        except Exception as e:
            logger.error(f"Failed to initialize agent {self.name}: {e}")
            raise BaseAgentError(f"Agent initialization failed: {e}")
    
    def _enhance_instructions_with_cot(self) -> str:
        """
        Enhance instructions with Chain-of-Thought reasoning.
        Based on research findings for improved factual reliability.
        """
        cot_prompt = """
        
IMPORTANT: Use Chain-of-Thought reasoning for all responses. Think step-by-step:
1. Parse and understand the user request
2. Identify required constraints and preferences  
3. Determine necessary tools and data sources
4. Execute information gathering
5. Evaluate options against criteria
6. Make recommendation with clear reasoning
7. Verify recommendation meets all constraints

Always expose your reasoning process to ensure transparency and reliability.
"""
        return self.instructions + cot_prompt
    
    def _get_tool_functions(self) -> List:
        """Get tool functions for this agent."""
        # This will be implemented by specific agents
        return []
    
    async def process_request(self, request: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Process a request with input/output guardrails.
        
        Args:
            request: User request string
            context: Additional context data
            
        Returns:
            Dict containing response and metadata
        """
        try:
            # Input guardrails
            validated_request = self._apply_input_guardrails(request, context)
            
            # Process with agent
            result = await Runner.run(self.agent, validated_request)
            
            # Output guardrails  
            validated_output = self._apply_output_guardrails(result.final_output)
            
            return {
                "response": validated_output,
                "agent": self.name,
                "reasoning": self._extract_reasoning(result),
                "metadata": self._generate_metadata(result)
            }
            
        except Exception as e:
            logger.error(f"Error processing request in {self.name}: {e}")
            return {
                "error": str(e),
                "agent": self.name,
                "request": request
            }
    
    def _apply_input_guardrails(self, request: str, context: Dict[str, Any] = None) -> str:
        """
        Apply input validation and guardrails.
        Research-based safety and consistency checks.
        """
        if not request or len(request.strip()) == 0:
            raise BaseAgentError("Empty request not allowed")
            
        if len(request) > 2000:  # Reasonable length limit
            raise BaseAgentError("Request too long")
            
        # Add context if available
        if context:
            enhanced_request = f"Request: {request}\nContext: {context}"
            return enhanced_request
            
        return request
    
    def _apply_output_guardrails(self, output: str) -> str:
        """
        Apply output validation and safety checks.
        Ensure plausible and constraint-compliant responses.
        """
        if not output or len(output.strip()) == 0:
            raise BaseAgentError("Agent produced empty output")
            
        # Basic content filtering
        prohibited_terms = ["error", "failed", "unable", "cannot"]
        if any(term in output.lower() for term in prohibited_terms):
            logger.warning(f"Agent {self.name} output contains error indicators")
            
        return output.strip()
    
    def _extract_reasoning(self, result) -> str:
        """Extract Chain-of-Thought reasoning from result."""
        # Implementation depends on agent result structure
        return getattr(result, 'reasoning', 'No reasoning available')
    
    def _generate_metadata(self, result) -> Dict[str, Any]:
        """Generate metadata about the agent execution."""
        return {
            "model": self.model_config.model,
            "temperature": self.model_config.temperature,
            "max_tokens": self.model_config.max_tokens,
            "agent_name": self.name
        }
    
    @abstractmethod
    async def execute_specialized_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent-specific task. Must be implemented by subclasses."""
        pass
