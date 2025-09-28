"""
Informative Search Agent - Intelligent parking spot optimization.
Formulates parking search as multi-criteria constrained optimization problem.
"""
import logging
from typing import Dict, List, Optional, Any, Tuple
import math
from .base_agent import BaseAgent  
from ..config.agent_configs import AgentConfigs

logger = logging.getLogger(__name__)

class InformativeSearchAgent(BaseAgent):
    """
    Intelligent search and optimization agent for parking spots.
    Implements multi-criteria constrained optimization.
    """
    
    def __init__(self):
        config = AgentConfigs.INFORMATIVE_SEARCH_AGENT
        super().__init__(
            name=config.name,
            instructions=config.instructions,
            model_config=config.model_config,
            tools=config.tools
        )
        
    def _get_tool_functions(self) -> List:
        """Get tool functions for search agent."""
        return [
            self.web_search,
            self.parking_api_search,
            self.calculate_walking_distance,
            self.optimize_parking_spots,
            self.evaluate_constraints
        ]
    
    async def web_search(self, query: str, location: str) -> List[Dict[str, Any]]:
        """
        Search for parking information via web search.
        
        Args:
            query: Search query
            location: Location context
            
        Returns:
            List of parking facilities found
        """
        try:
            # Mock web search results based on research paper example
            if "toronto" in location.lower():
                return [
                    {
                        "name": "Green P Carpark 36 (Nathan Phillips Square)",
                        "address": "110 Queen St W, Toronto",
                        "coordinates": {"lat": 43.6517, "lng": -79.3844},
                        "price_per_half_hour": 4.00,
                        "ev_charging": True,
                        "accessibility": True, 
                        "rating": 4.2,
                        "amenities": ["covered", "security", "24/7"],
                        "source": "web_search"
                    },
                    {
                        "name": "Parking Town Hall Garage", 
                        "address": "361 University Ave, Toronto",
                        "coordinates": {"lat": 43.6532, "lng": -79.3859},
                        "price_per_half_hour": 2.50,
                        "ev_charging": True,
                        "accessibility": True,
                        "rating": 4.8,
                        "amenities": ["underground", "valet", "security"],
                        "source": "web_search"
                    },
                    {
                        "name": "Bell Trinity Square – Lot 235",
                        "address": "483 Bay St, Toronto", 
                        "coordinates": {"lat": 43.6544, "lng": -79.3828},
                        "price_per_half_hour": 1.76,
                        "ev_charging": True,
                        "accessibility": False,
                        "rating": 4.0,
                        "amenities": ["outdoor", "basic"],
                        "source": "web_search"
                    }
                ]
            
            return []
            
        except Exception as e:
            logger.error(f"Web search error: {e}")
            return []
    
    async def parking_api_search(self, location: Dict[str, float], radius: float = 1000) -> List[Dict[str, Any]]:
        """
        Search parking APIs for real-time availability.
        
        Args:
            location: {"lat": float, "lng": float}
            radius: Search radius in meters
            
        Returns:
            List of available parking spots
        """
        try:
            # Mock API search - in production would call real parking APIs
            logger.info(f"Searching parking APIs near {location} within {radius}m")
            
            # Return mock real-time availability data
            return [
                {
                    "api_id": "api_001",
                    "name": "City Hall Parking Garage",
                    "coordinates": location,  # Near search location
                    "available_spots": 23,
                    "total_spots": 100,
                    "current_rate": 3.50,
                    "ev_charging_available": 5,
                    "last_updated": "2 minutes ago",
                    "source": "parking_api"
                }
            ]
            
        except Exception as e:
            logger.error(f"Parking API search error: {e}")
            return []
    
    async def calculate_walking_distance(self, origin: Dict[str, float], destination: Dict[str, float]) -> float:
        """
        Calculate walking distance between two points.
        
        Args:
            origin: {"lat": float, "lng": float} 
            destination: {"lat": float, "lng": float}
            
        Returns:
            Walking distance in meters
        """
        try:
            # Haversine formula for distance calculation
            R = 6371000  # Earth's radius in meters
            
            lat1_rad = math.radians(origin["lat"])
            lat2_rad = math.radians(destination["lat"]) 
            delta_lat = math.radians(destination["lat"] - origin["lat"])
            delta_lng = math.radians(destination["lng"] - origin["lng"])
            
            a = (math.sin(delta_lat/2) * math.sin(delta_lat/2) + 
                 math.cos(lat1_rad) * math.cos(lat2_rad) * 
                 math.sin(delta_lng/2) * math.sin(delta_lng/2))
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
            
            distance = R * c
            return round(distance, 1)
            
        except Exception as e:
            logger.error(f"Distance calculation error: {e}")
            return float('inf')  # Return infinite distance on error
    
    async def evaluate_constraints(self, parking_spot: Dict[str, Any], constraints: Dict[str, Any]) -> Tuple[bool, float]:
        """
        Evaluate parking spot against hard and soft constraints.
        
        Args:
            parking_spot: Parking spot data
            constraints: User constraints and preferences
            
        Returns:
            Tuple of (meets_hard_constraints, soft_constraint_score)
        """
        try:
            hard_constraints_met = True
            soft_score = 0.0
            
            # Hard Constraints (must be satisfied)
            if constraints.get("ev_charging") == "required":
                if not parking_spot.get("ev_charging", False):
                    hard_constraints_met = False
                    
            if constraints.get("accessibility") == "required":
                if not parking_spot.get("accessibility", False):
                    hard_constraints_met = False
                    
            if constraints.get("max_price"):
                if parking_spot.get("price_per_half_hour", 0) > constraints["max_price"]:
                    hard_constraints_met = False
                    
            if constraints.get("max_walking_distance"):
                walking_dist = parking_spot.get("walking_distance", float('inf'))
                if walking_dist > constraints["max_walking_distance"]:
                    hard_constraints_met = False
            
            # Soft Constraints (preferences - contribute to score)
            if constraints.get("price_priority") == "high":
                # Lower price = higher score
                price = parking_spot.get("price_per_half_hour", 10)
                soft_score += max(0, (10 - price) / 10) * 0.3
                
            if constraints.get("rating_priority") == "high":
                rating = parking_spot.get("rating", 0)
                soft_score += (rating / 5.0) * 0.3
                
            if constraints.get("distance_priority") == "high":
                # Shorter distance = higher score
                distance = parking_spot.get("walking_distance", 1000)
                soft_score += max(0, (500 - distance) / 500) * 0.4
                
            return hard_constraints_met, min(soft_score, 1.0)
            
        except Exception as e:
            logger.error(f"Constraint evaluation error: {e}") 
            return False, 0.0
    
    async def optimize_parking_spots(self, spots: List[Dict[str, Any]], constraints: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Multi-criteria optimization of parking spots.
        
        Args:
            spots: List of candidate parking spots
            constraints: User constraints and preferences
            
        Returns:
            Ranked list of optimal parking spots
        """
        try:
            # Evaluate each spot against constraints
            evaluated_spots = []
            
            for spot in spots:
                hard_ok, soft_score = await self.evaluate_constraints(spot, constraints)
                
                if hard_ok:  # Only include spots that meet hard constraints
                    spot_copy = spot.copy()
                    spot_copy["optimization_score"] = soft_score
                    spot_copy["meets_hard_constraints"] = True
                    evaluated_spots.append(spot_copy)
                    
            # Sort by optimization score (descending)
            optimized_spots = sorted(
                evaluated_spots, 
                key=lambda x: x["optimization_score"], 
                reverse=True
            )
            
            logger.info(f"Optimized {len(optimized_spots)} spots from {len(spots)} candidates")
            return optimized_spots
            
        except Exception as e:
            logger.error(f"Optimization error: {e}")
            return spots  # Return original list on error
    
    async def execute_specialized_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute parking search optimization task.
        
        Args:
            task_data: Search parameters including destination, preferences, constraints
            
        Returns:
            Optimized parking search results
        """
        try:
            destination = task_data.get("destination")
            preferences = task_data.get("preferences", {})
            constraints = task_data.get("constraints", {})
            
            # Step 1: Gather parking data from multiple sources
            web_results = await self.web_search(f"parking near {destination}", destination)
            
            # Mock destination coordinates (in production, would geocode)
            dest_coords = {"lat": 43.6532, "lng": -79.3844}  # Toronto City Hall
            api_results = await self.parking_api_search(dest_coords)
            
            # Step 2: Combine and enhance results
            all_spots = web_results + api_results
            
            # Calculate walking distances
            for spot in all_spots:
                if "coordinates" in spot:
                    distance = await self.calculate_walking_distance(
                        dest_coords, spot["coordinates"]
                    )
                    spot["walking_distance"] = distance
                    
            # Step 3: Apply multi-criteria optimization
            constraints_merged = {**preferences, **constraints}
            optimized_spots = await self.optimize_parking_spots(all_spots, constraints_merged)
            
            return {
                "status": "success",
                "destination": destination,
                "total_spots_found": len(all_spots),
                "spots_meeting_constraints": len(optimized_spots),
                "recommended_spots": optimized_spots[:5],  # Top 5 recommendations
                "search_metadata": {
                    "web_results": len(web_results),
                    "api_results": len(api_results),
                    "optimization_applied": True
                }
            }
            
        except Exception as e:
            logger.error(f"Search task execution error: {e}")
            return {
                "status": "error",
                "error": str(e),
                "destination": task_data.get("destination")
            }
