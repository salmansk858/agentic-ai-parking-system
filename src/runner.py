"""
High-level runner for the parking system.
Provides simple interface for integration.
"""
import asyncio
import logging
from typing import Dict, Any, Optional

from .agents.agent_registry import agent_registry

logger = logging.getLogger(__name__)

class ParkingSystem:
    """
    High-level interface for the agentic parking system.
    Simplifies interaction with the multi-agent architecture.
    """
    
    def __init__(self):
        self.registry = agent_registry
        
    async def find_parking(
        self, 
        destination: str, 
        preferences: Optional[Dict[str, Any]] = None,
        user_profile: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Find optimal parking spots for a destination.
        
        Args:
            destination: Target destination
            preferences: User preferences dictionary  
            user_profile: User profile type (research-based)
            
        Returns:
            Parking search results
        """
        try:
            interaction_agent = self.registry.get_agent("interaction")
            
            task_data = {
                "task_type": "find_parking",
                "destination": destination,
                "preferences": preferences or {},
                "profile_type": user_profile
            }
            
            result = await interaction_agent.execute_specialized_task(task_data)
            return result
            
        except Exception as e:
            logger.error(f"Find parking error: {e}")
            return {"error": str(e)}
    
    async def navigate_to_parking(self, destination: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get navigation to selected parking location.
        
        Args:
            destination: Selected parking destination
            
        Returns:
            Navigation information
        """
        try:
            interaction_agent = self.registry.get_agent("interaction")
            
            task_data = {
                "task_type": "navigate_to_parking",
                "destination": destination
            }
            
            result = await interaction_agent.execute_specialized_task(task_data)
            return result
            
        except Exception as e:
            logger.error(f"Navigation error: {e}")
            return {"error": str(e)}
    
    def find_parking_sync(
        self, 
        destination: str,
        preferences: Optional[Dict[str, Any]] = None,
        user_profile: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Synchronous wrapper for find_parking.
        
        Args:
            destination: Target destination
            preferences: User preferences
            user_profile: User profile type
            
        Returns:
            Parking search results
        """
        return asyncio.run(self.find_parking(destination, preferences, user_profile))
    
    def get_user_profiles(self) -> Dict[str, Any]:
        """
        Get all available user profiles from research.
        
        Returns:
            Dictionary of user profiles
        """
        from .config.settings import settings
        return {
            name: {
                "name": profile.name,
                "description": profile.description,
                "preferences": profile.preferences
            }
            for name, profile in settings.USER_PROFILES.items()
        }

# Global system instance
parking_system = ParkingSystem()
