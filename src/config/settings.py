"""
Application configuration settings based on research paper findings.
Optimized for gpt-4o-mini with low entropy and short verbosity.
"""
import os
from typing import Dict, List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class ModelConfig(BaseModel):
    """LLM configuration optimized based on research findings."""
    model: str = "gpt-4o-mini"  # Optimal latency/consistency balance
    temperature: float = 0.2    # Low entropy for consistency  
    max_tokens: int = 150       # Short verbosity for minimal latency
    top_p: float = 0.8         # Low entropy setting
    
class UserProfile(BaseModel):
    """User profile configurations from research paper."""
    name: str
    description: str
    preferences: Dict[str, any]

class AgentConfig(BaseModel):
    """Base agent configuration."""
    name: str
    instructions: str
    model_config: ModelConfig = ModelConfig()
    tools: List[str] = []
    
class Settings:
    """Application settings."""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GOOGLE_MAPS_API_KEY: str = os.getenv("GOOGLE_MAPS_API_KEY", "")
    PARKING_API_KEY: str = os.getenv("PARKING_API_KEY", "")
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")
    
    # Model Configuration (research optimized)
    MODEL_CONFIG = ModelConfig()
    
    # User Profiles from Research Paper
    USER_PROFILES = {
        "commuter_saver": UserProfile(
            name="Commuter Saver", 
            description="Drives an EV on a tight budget. Prioritizes lowest half-hour rate and a working charger.",
            preferences={
                "price_priority": "highest",
                "ev_charging": "required", 
                "walk_distance": "flexible",
                "amenities": "irrelevant"
            }
        ),
        "efficient_multitasker": UserProfile(
            name="Efficient Multitasker",
            description="Values time over money. Seeks closest, top-reviewed space with valet service.",
            preferences={
                "time_priority": "highest",
                "distance": "minimal",
                "rating": "high",
                "valet_service": "preferred",
                "price": "flexible"
            }
        ),
        "creative_wanderer": UserProfile(
            name="Creative Wanderer", 
            description="Wants memorable, off-beat location in artsy, less-touristy area.",
            preferences={
                "atmosphere": "quirky",
                "area_type": "artsy", 
                "tourist_level": "low",
                "price": "flexible",
                "ev_charging": "optional"
            }
        ),
        "independent_elder": UserProfile(
            name="Independent Elder",
            description="Uses wheelchair and avoids crowds. Requires accessible ground-level space.",
            preferences={
                "accessibility": "required",
                "crowd_level": "low", 
                "ground_level": "required",
                "wide_bays": "required",
                "entrance_proximity": "critical"
            }
        ),
        "green_professional": UserProfile(
            name="Green Professional",
            description="Business traveler with electric company car. Needs reliable fast charger.",
            preferences={
                "ev_charging": "fast_required",
                "reliability": "critical",
                "location": "central",
                "lighting": "good",
                "price": "mid_range"
            }
        )
    }
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///parking_system.db")
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "json")

settings = Settings()
