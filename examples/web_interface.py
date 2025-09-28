"""
Simple Streamlit web interface for the parking system.
"""
import streamlit as st
import asyncio
from src.runner import ParkingSystem
import json

@st.cache_resource
def get_parking_system():
    """Get cached parking system instance."""
    return ParkingSystem()

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Agentic AI Parking System",
        page_icon="🚗",
        layout="wide"
    )
    
    st.title("🚗 Agentic AI Frictionless Parking System")
    st.markdown("*Intelligent multi-agent parking assistance based on IEEE research*")
    
    # Sidebar - User Profile Selection
    st.sidebar.header("User Profile")
    system = get_parking_system()
    profiles = system.get_user_profiles()
    
    profile_names = ["None"] + list(profiles.keys())
    selected_profile = st.sidebar.selectbox(
        "Choose your profile:",
        options=profile_names,
        format_func=lambda x: "Default" if x == "None" else profiles[x]["name"] if x != "None" else x
    )
    
    if selected_profile != "None":
        st.sidebar.markdown(f"**Description:** {profiles[selected_profile]['description']}")
    
    # Main Interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Find Parking")
        
        # Destination input
        destination = st.text_input(
            "Where are you going?",
            placeholder="e.g., Toronto City Hall, CN Tower, etc.",
            help="Enter your destination to find nearby parking"
        )
        
        # Advanced preferences
        with st.expander("Advanced Preferences"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                ev_charging = st.checkbox("EV Charging Required")
                accessibility = st.checkbox("Accessibility Required")
                max_price = st.number_input("Max Price per Hour (CAD)", min_value=0.0, max_value=50.0, value=10.0)
                
            with col_b:
                max_walk_dist = st.slider("Max Walking Distance (m)", 50, 1000, 300)
                rating_priority = st.selectbox("Rating Priority", ["Low", "Medium", "High"])
                valet_service = st.checkbox("Valet Service Preferred")
        
        # Search button
        if st.button("🔍 Find Parking", type="primary"):
            if destination:
                with st.spinner("Searching for optimal parking spots..."):
                    # Prepare preferences
                    preferences = {
                        "ev_charging": "required" if ev_charging else "optional",
                        "accessibility": "required" if accessibility else "optional", 
                        "max_price": max_price,
                        "max_walking_distance": max_walk_dist,
                        "rating_priority": rating_priority.lower(),
                        "valet_service": "preferred" if valet_service else "optional"
                    }
                    
                    # Execute search
                    try:
                        result = system.find_parking_sync(
                            destination=destination,
                            preferences=preferences,
                            user_profile=selected_profile if selected_profile != "None" else None
                        )
                        
                        if result.get("status") == "completed":
                            search_results = result.get("search_results", {})
                            if search_results.get("results"):
                                st.success(f"Found {len(search_results['results'])} parking options!")
                                
                                # Display results
                                for i, spot in enumerate(search_results["results"][:5]):
                                    with st.container():
                                        st.markdown(f"### {i+1}. {spot['name']}")
                                        
                                        col_info, col_details, col_action = st.columns([2, 2, 1])
                                        
                                        with col_info:
                                            st.write(f"📍 **Address:** {spot['address']}")
                                            st.write(f"🚶 **Walk:** {spot.get('walk_distance', 'N/A')}")
                                            st.write(f"💰 **Price:** {spot['price']}")
                                            
                                        with col_details:
                                            st.write(f"⚡ **EV Charging:** {'✅' if spot['ev_charging'] else '❌'}")
                                            st.write(f"♿ **Accessible:** {'✅' if spot['accessibility'] else '❌'}")
                                            st.write(f"⭐ **Rating:** {spot['rating']}/5")
                                            
                                        with col_action:
                                            if st.button(f"Navigate", key=f"nav_{i}"):
                                                st.success("Navigation started!")
                                        
                                        st.divider()
                            else:
                                st.warning("No parking spots found matching your criteria.")
                        else:
                            st.error(f"Search failed: {result.get('error', 'Unknown error')}")
                            
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            else:
                st.warning("Please enter a destination.")
    
    with col2:
        st.header("System Info")
        
        # Agent status
        with st.container():
            st.subheader("🤖 Active Agents")
            agents = ["Interaction", "Search", "Routing", "Access", "Micro-routing", "On-spot", "Departure"]
            for agent in agents:
                status = "🟢 Active" if agent in ["Interaction", "Search"] else "🟡 Ready"
                st.write(f"**{agent}:** {status}")
        
        # Performance metrics
        with st.container():
            st.subheader("📊 Performance")
            st.write("**Model:** GPT-4o-mini")
            st.write("**Latency:** ~3.7s avg")
            st.write("**Consistency:** 0.66 avg")
            st.write("**Optimization:** Chain-of-Thought")
        
        # Research info
        with st.expander("📋 Research Base"):
            st.markdown("""
            This system implements the architecture from:
            
            **"Agentic AI Systems: Architecture and Evaluation Using a Frictionless Parking Scenario"**
            
            *IEEE Access, 2025*
            
            Key optimizations:
            - GPT-4o-mini for best latency/consistency
            - Low entropy settings
            - Medium prompt specificity
            - Chain-of-Thought reasoning
            """)

if __name__ == "__main__":
    main()
