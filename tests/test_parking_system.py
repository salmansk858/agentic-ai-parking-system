"""
Integration tests for the parking system.
"""
import pytest
import asyncio
from src.runner import ParkingSystem

class TestParkingSystem:
    """Test cases for the high-level parking system."""
    
    @pytest.fixture
    def system(self):
        return ParkingSystem()
    
    @pytest.mark.asyncio
    async def test_find_parking_basic(self, system):
        """Test basic parking search."""
        result = await system.find_parking(
            destination="Toronto City Hall"
        )
        
        assert "workflow" in result
        assert result["workflow"] == "find_parking"
        assert result["status"] == "completed"
    
    @pytest.mark.asyncio
    async def test_find_parking_with_profile(self, system):
        """Test parking search with user profile."""
        result = await system.find_parking(
            destination="CN Tower", 
            user_profile="commuter_saver"
        )
        
        assert "user_preferences" in result
        user_prefs = result["user_preferences"]
        assert user_prefs["profile_type"] == "commuter_saver"
        assert user_prefs["preferences"]["price_priority"] == "highest"
    
    @pytest.mark.asyncio
    async def test_find_parking_with_preferences(self, system):
        """Test parking search with custom preferences.""" 
        preferences = {
            "ev_charging": "required",
            "max_price": 5.0,
            "accessibility": "preferred"
        }
        
        result = await system.find_parking(
            destination="Eaton Centre",
            preferences=preferences
        )
        
        assert result["status"] == "completed"
        assert "search_results" in result
    
    def test_find_parking_sync(self, system):
        """Test synchronous parking search."""
        result = system.find_parking_sync(
            destination="Union Station",
            user_profile="efficient_multitasker"
        )
        
        assert "workflow" in result
        assert result["workflow"] == "find_parking"
    
    def test_get_user_profiles(self, system):
        """Test user profile retrieval."""
        profiles = system.get_user_profiles()
        
        assert isinstance(profiles, dict)
        assert "commuter_saver" in profiles
        assert "green_professional" in profiles
        
        # Check profile structure
        commuter = profiles["commuter_saver"]
        assert "name" in commuter
        assert "description" in commuter
        assert "preferences" in commuter
    
    @pytest.mark.asyncio
    async def test_navigate_to_parking(self, system):
        """Test navigation functionality."""
        destination = {
            "name": "Test Parking",
            "address": "123 Test St",
            "coordinates": {"lat": 43.6532, "lng": -79.3844}
        }
        
        result = await system.navigate_to_parking(destination)
        
        assert "navigation" in result
        nav_info = result["navigation"]
        assert "eta" in nav_info
        assert "distance" in nav_info

@pytest.mark.integration
class TestAPIIntegration:
    """Integration tests requiring external APIs."""
    
    @pytest.mark.skipif("not config.getoption('--run-integration')")
    def test_real_api_calls(self):
        """Test with real API calls (requires API keys)."""
        # These tests would run with real API keys in CI/CD
        pass

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
