"""
Agent Registry - Central management of all agents.
Implements handoff and cueing mechanisms.
"""
import logging
from typing import Dict, Optional, Any
from .interaction_agent import InteractionAgent
from .informative_search_agent import InformativeSearchAgent

logger = logging.getLogger(__name__)

class AgentRegistry:
    """
    Central registry for all agents with handoff and cueing support.
    Implements the cooperation patterns from the research paper.
    """
    
    def __init__(self):
        self.agents = {}
        self.active_sessions = {}
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all agents."""
        try:
            self.agents["interaction"] = InteractionAgent()
            self.agents["informative_search"] = InformativeSearchAgent()
            
            # Additional agents would be initialized here
            # self.agents["on_route_guidance"] = OnRouteGuidanceAgent()
            # self.agents["access"] = AccessAgent() 
            # self.agents["micro_routing"] = MicroRoutingAgent()
            # self.agents["on_spot"] = OnSpotAgent()
            # self.agents["departure"] = DepartureAgent()
            
            logger.info(f"Initialized {len(self.agents)} agents")
            
        except Exception as e:
            logger.error(f"Failed to initialize agents: {e}")
            raise
    
    def get_agent(self, agent_name: str):
        """Get agent by name."""
        return self.agents.get(agent_name)
    
    async def handoff(self, from_agent: str, to_agent: str, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute handoff between agents.
        
        Args:
            from_agent: Source agent name
            to_agent: Target agent name 
            task_data: Task data to transfer
            
        Returns:
            Result from target agent
        """
        try:
            logger.info(f"Handoff: {from_agent} -> {to_agent}")
            
            target_agent = self.get_agent(to_agent)
            if not target_agent:
                return {"error": f"Agent {to_agent} not found"}
                
            # Execute task on target agent
            result = await target_agent.execute_specialized_task(task_data)
            
            # Log handoff completion
            logger.info(f"Handoff completed: {from_agent} -> {to_agent}")
            return result
            
        except Exception as e:
            logger.error(f"Handoff error {from_agent} -> {to_agent}: {e}")
            return {"error": str(e)}
    
    async def cue(self, cuer_agent: str, cued_agent: str, context_data: Dict[str, Any]) -> bool:
        """
        Implement cueing mechanism - prepare agent for upcoming task.
        
        Args:
            cuer_agent: Agent providing the cue
            cued_agent: Agent receiving the cue
            context_data: Context information for preparation
            
        Returns:
            Success status of cueing
        """
        try:
            logger.info(f"Cueing: {cuer_agent} -> {cued_agent}")
            
            target_agent = self.get_agent(cued_agent)
            if not target_agent:
                logger.error(f"Cued agent {cued_agent} not found")
                return False
                
            # Store context for the cued agent
            if not hasattr(target_agent, '_cue_context'):
                target_agent._cue_context = {}
                
            target_agent._cue_context.update(context_data)
            
            logger.info(f"Cuing completed: {cuer_agent} -> {cued_agent}")
            return True
            
        except Exception as e:
            logger.error(f"Cueing error {cuer_agent} -> {cued_agent}: {e}")
            return False

# Global registry instance
agent_registry = AgentRegistry()
