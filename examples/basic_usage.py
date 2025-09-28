"""
Basic usage examples for the Agentic AI Parking System.
"""
import asyncio
from src.runner import ParkingSystem

async def main():
    """Demonstrate basic usage of the parking system."""
    
    # Initialize system
    system = ParkingSystem()
    
    print("🚗 Agentic AI Frictionless Parking System Demo")
    print("=" * 50)
    
    # Example 1: Basic parking search
    print("\n1. Basic parking search near Toronto City Hall")
    result1 = await system.find_parking(
        destination="Toronto City Hall",
        preferences={"price_tier": "affordable", "ev_charging": True}
    )
    print(f"Found {len(result1.get('search_results', {}).get('results', []))} parking options")
    
    # Example 2: Using specific user profile
    print("\n2. Search with commuter_saver profile")
    result2 = await system.find_parking(
        destination="Toronto Eaton Centre", 
        user_profile="commuter_saver"
    )
    print(f"Commuter saver results: {result2.get('status', 'unknown')}")
    
    # Example 3: Navigation to selected parking
    if result1.get('search_results', {}).get('results'):
        selected_parking = result1['search_results']['results'][0]
        print(f"\n3. Getting navigation to: {selected_parking['name']}")
        
        nav_result = await system.navigate_to_parking(selected_parking)
        if 'navigation' in nav_result:
            print(f"ETA: {nav_result['navigation'].get('eta', 'unknown')}")
            print(f"Route: {nav_result['navigation'].get('route', 'unknown')}")
    
    # Example 4: List available user profiles
    print("\n4. Available user profiles:")
    profiles = system.get_user_profiles()
    for profile_name, profile_data in profiles.items():
        print(f"  - {profile_data['name']}: {profile_data['description']}")

def sync_example():
    """Synchronous usage example."""
    system = ParkingSystem()
    
    # Use synchronous wrapper
    result = system.find_parking_sync(
        destination="CN Tower, Toronto",
        user_profile="green_professional"
    )
    
    print(f"\nSync example result: {result.get('status', 'unknown')}")

if __name__ == "__main__":
    # Run async examples
    asyncio.run(main())
    
    # Run sync example  
    sync_example()
