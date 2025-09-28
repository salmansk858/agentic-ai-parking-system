"""
Interaction Agent - Primary orchestration and user interface agent.
Manages user interactions and coordinates other specialized agents.
"""
import logging
from typing import Dict, List, Optional, Any
from .base_agent import BaseAgent
from ..config.agent_configs import AgentConfigs
from ..config.settings import settings

logger = logging.getLogger(__name__)

class InteractionAgent(BaseAgent):
    """
    Primary interface between user and system.
    Orchestrates activities of other specialized agents.
    """
    
    def __init__(self):
        config = AgentConfigs.INTERACTION_AGENT
        super().__init__(
            name=config.name,
            instructions=config.instructions, 
            model_config=config.model_config,
            tools=config.tools
        )
        self.user_profiles = settings.USER_PROFILES
        self.active_session = None
        
    def _get_tool_functions(self) -> List:
        """Get tool functions for interaction agent."""
        return [
            self.get_user_preferences,
            self.update_user_preferences,
            self.handoff_to_search,
            self.handoff_to_routing,
            self.collect_feedback
        ]
    
    async def get_user_preferences(self, user_id: str = None, profile_type: str = None) -> Dict[str, Any]:
        """
        Retrieve user preferences from profile or detect from query.
        
        Args:
            user_id: Optional user identifier
            profile_type: One of the research user profiles
            
        Returns:
            User preferences dictionary
        """
        try:
            if profile_type and profile_type in self.user_profiles:
                profile = self.user_profiles[profile_type]
                logger.info(f"Retrieved profile: {profile.name}")
                return {
                    "profile_type": profile_type,
                    "name": profile.name,
                    "description": profile.description,
                    "preferences": profile.preferences
                }
            
            # Default to balanced preferences if no profile specified
            return {
                "profile_type": "balanced",
                "preferences": {
                    "price_priority": "medium",
                    "time_priority": "medium", 
                    "distance": "reasonable",
                    "ev_charging": "optional",
                    "accessibility": "standard"
                }
            }
            
        except Exception as e:
            logger.error(f"Error retrieving user preferences: {e}")
            return {"error": str(e)}
    
    async def update_user_preferences(self, preferences: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update user preferences based on feedback.
        
        Args:
            preferences: Updated preference dictionary
            
        Returns:
            Confirmation of update
        """
        try:
            # In production, this would update a database
            logger.info(f"Updated user preferences: {preferences}")
            return {
                "status": "success",
                "message": "Preferences updated successfully",
                "preferences": preferences
            }
        except Exception as e:
            logger.error(f"Error updating preferences: {e}")
            return {"error": str(e)}
    
    async def handoff_to_search(self, search_criteria: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handoff parking search task to Informative Search Agent.
        
        Args:
            search_criteria: Search parameters and constraints
            
        Returns:
            Search results from Informative Search Agent
        """
        try:
            logger.info(f"Handing off search task: {search_criteria}")
            
            # In production, this would create and call the search agent
            # For now, return mock results based on research paper example
            mock_results = [
                {
                    "name": "Green P Carpark 36 (Nathan Phillips Square)",
                    "address": "110 Queen St W, Toronto", 
                    "coordinates": {"lat": 43.6517, "lng": -79.3844},
                    "walk_distance": "87m",
                    "price": "CA$4.00 per half-hour",
                    "ev_charging": True,
                    "accessibility": True,
                    "rating": 4.2,
                    "booking_url": "https://parking.greenp.com/book/36"
                },
                {
                    "name": "Parking Town Hall Garage",
                    "address": "361 University Ave, Toronto",
                    "coordinates": {"lat": 43.6532, "lng": -79.3859}, 
                    "walk_distance": "200m",
                    "price": "CA$2.50 per half-hour",
                    "ev_charging": True,
                    "accessibility": True,
                    "rating": 4.8,
                    "booking_url": "https://parktownhall.com/book"
                },
                {
                    "name": "Bell Trinity Square – Lot 235",
                    "address": "483 Bay St, Toronto",
                    "coordinates": {"lat": 43.6544, "lng": -79.3828},
                    "walk_distance": "240m", 
                    "price": "CA$1.76 per half-hour",
                    "ev_charging": True,
                    "accessibility": False,
                    "rating": 4.0,
                    "booking_url": "https://belltrinity.com/book/235"
                }
            ]
            
            return {
                "status": "success",
                "results": mock_results,
                "total_found": len(mock_results),
                "search_criteria": search_criteria
            }
            
        except Exception as e:
            logger.error(f"Error in search handoff: {e}")
            return {"error": str(e)}
    
    async def handoff_to_routing(self, destination: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handoff navigation task to On-Route Guidance Agent.
        
        Args:
            destination: Selected parking destination
            
        Returns:
            Navigation and routing information
        """
        try:
            logger.info(f"Handing off routing task to: {destination}")
            
            # Mock routing response
            return {
                "status": "success", 
                "navigation": {
                    "destination": destination,
                    "eta": "12 minutes",
                    "distance": "3.2 km",
                    "route": "via University Ave",
                    "traffic_status": "light",
                    "weather": "clear"
                }
            }
            
        except Exception as e:
            logger.error(f"Error in routing handoff: {e}")
            return {"error": str(e)}
    
    async def collect_feedback(self, session_data: Dict[str, Any], rating: int, comments: str = "") -> Dict[str, Any]:
        """
        Collect user feedback for post-trip learning.
        
        Args:
            session_data: Session information
            rating: User rating (1-5)
            comments: Optional feedback comments
            
        Returns:
            Feedback processing confirmation
        """
        try:
            feedback = {
                "session_id": session_data.get("session_id"),
                "rating": rating,
                "comments": comments,
                "timestamp": "now",  # In production, use proper timestamp
                "parking_location": session_data.get("selected_parking")
            }
            
            logger.info(f"Collected feedback: {feedback}")
            
            # In production, this would update ML models for personalization
            return {
                "status": "success",
                "message": "Thank you for your feedback!",
                "feedback_id": "fb_" + str(hash(str(feedback)))
            }
            
        except Exception as e:
            logger.error(f"Error collecting feedback: {e}")
            return {"error": str(e)}
    
    async def execute_specialized_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute interaction-specific tasks.
        
        Args:
            task_data: Task parameters
            
        Returns:
            Task execution results
        """
        task_type = task_data.get("task_type")
        
        if task_type == "find_parking":
            # Coordinate full parking search workflow
            user_prefs = await self.get_user_preferences(
                profile_type=task_data.get("profile_type")
            )
            
            search_results = await self.handoff_to_search({
                "destination": task_data.get("destination"),
                "preferences": user_prefs["preferences"],
                "constraints": task_data.get("constraints", {})
            })
            
            return {
                "workflow": "find_parking",
                "user_preferences": user_prefs,
                "search_results": search_results,
                "status": "completed"
            }
            
        elif task_type == "navigate_to_parking":
            return await self.handoff_to_routing(task_data.get("destination"))
            
        else:
            return {"error": f"Unknown task type: {task_type}"}
