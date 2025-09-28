"""
Test suite for agent functionality.
"""
import pytest
import asyncio
from unittest.mock import Mock, patch
from src.agents.interaction_agent import InteractionAgent
from src.agents.informative_search_agent import InformativeSearchAgent
from src.agents.agent_registry import AgentRegistry

class TestInteractionAgent:
    """Test cases for Interaction Agent."""
    
    @pytest.fixture
    def agent(self):
        return InteractionAgent()
    
    @pytest.mark.asyncio
    async def test_get_user_preferences(self, agent):
        """Test user preference retrieval."""
        # Test with known profile
        result = await agent.get_user_preferences(profile_type="commuter_saver")
        assert result["profile_type"] == "commuter_saver"
        assert "preferences" in result
        assert result["preferences"]["price_priority"] == "highest"
        
        # Test with default profile
        result = await agent.get_user_preferences()
        assert result["profile_type"] == "balanced"
        assert "preferences" in result
    
    @pytest.mark.asyncio
    async def test_handoff_to_search(self, agent):
        """Test search handoff functionality."""
        search_criteria = {
            "destination": "Toronto City Hall",
            "preferences": {"ev_charging": True}
        }
        
        result = await agent.handoff_to_search(search_criteria)
        assert result["status"] == "success"
        assert "results" in result
        assert len(result["results"]) > 0
        
        # Verify first result structure
        first_result = result["results"][0]
        required_fields = ["name", "address", "coordinates", "price", "ev_charging"]
        for field in required_fields:
            assert field in first_result

class TestInformativeSearchAgent:
    """Test cases for Informative Search Agent."""
    
    @pytest.fixture  
    def agent(self):
        return InformativeSearchAgent()
    
    @pytest.mark.asyncio
    async def test_calculate_walking_distance(self, agent):
        """Test walking distance calculation."""
        origin = {"lat": 43.6532, "lng": -79.3844}
        destination = {"lat": 43.6517, "lng": -79.3844}
        
        distance = await agent.calculate_walking_distance(origin, destination)
        assert isinstance(distance, float)
        assert distance > 0
        assert distance < 1000  # Should be reasonable distance
    
    @pytest.mark.asyncio
    async def test_evaluate_constraints(self, agent):
        """Test constraint evaluation."""
        parking_spot = {
            "ev_charging": True,
            "accessibility": True, 
            "price_per_half_hour": 3.0,
            "walking_distance": 200,
            "rating": 4.5
        }
        
        constraints = {
            "ev_charging": "required",
            "accessibility": "required",
            "max_price": 5.0,
            "max_walking_distance": 300,
            "rating_priority": "high"
        }
        
        meets_hard, soft_score = await agent.evaluate_constraints(parking_spot, constraints)
        assert meets_hard == True
        assert 0 <= soft_score <= 1
    
    @pytest.mark.asyncio
    async def test_web_search(self, agent):
        """Test web search functionality."""
        results = await agent.web_search("parking", "toronto")
        assert isinstance(results, list)
        
        if len(results) > 0:
            first_result = results[0]
            assert "name" in first_result
            assert "coordinates" in first_result
            assert "source" in first_result
            assert first_result["source"] == "web_search"

class TestAgentRegistry:
    """Test cases for Agent Registry."""
    
    @pytest.fixture
    def registry(self):
        return AgentRegistry()
    
    def test_agent_initialization(self, registry):
        """Test that agents are properly initialized."""
        assert "interaction" in registry.agents
        assert "informative_search" in registry.agents
        assert len(registry.agents) >= 2
    
    def test_get_agent(self, registry):
        """Test agent retrieval."""
        interaction_agent = registry.get_agent("interaction")
        assert interaction_agent is not None
        assert isinstance(interaction_agent, InteractionAgent)
        
        # Test non-existent agent
        non_existent = registry.get_agent("non_existent")
        assert non_existent is None
    
    @pytest.mark.asyncio
    async def test_handoff(self, registry):
        """Test agent handoff mechanism."""
        task_data = {
            "destination": "Test Location",
            "preferences": {"ev_charging": True}
        }
        
        result = await registry.handoff(
            from_agent="interaction",
            to_agent="informative_search", 
            task_data=task_data
        )
        
        assert "status" in result
        # Should either succeed or have a controlled error
        assert result.get("status") in ["success", "error"] or "error" in result
    
    @pytest.mark.asyncio
    async def test_cue(self, registry):
        """Test agent cueing mechanism."""
        context_data = {"upcoming_task": "parking_search"}
        
        success = await registry.cue(
            cuer_agent="interaction",
            cued_agent="informative_search",
            context_data=context_data
        )
        
        assert isinstance(success, bool)
        
        # Check that context was stored
        if success:
            search_agent = registry.get_agent("informative_search")
            assert hasattr(search_agent, "_cue_context")
            assert search_agent._cue_context["upcoming_task"] == "parking_search"

@pytest.mark.asyncio 
async def test_integration_workflow():
    """Test complete parking search workflow."""
    registry = AgentRegistry()
    interaction_agent = registry.get_agent("interaction")
    
    # Execute full parking search
    task_data = {
        "task_type": "find_parking",
        "destination": "Toronto City Hall",
        "profile_type": "green_professional"
    }
    
    result = await interaction_agent.execute_specialized_task(task_data)
    
    assert "workflow" in result
    assert result["workflow"] == "find_parking"
    assert "user_preferences" in result
    assert "search_results" in result
    assert result["status"] == "completed"

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
