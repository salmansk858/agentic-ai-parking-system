"""
Main application entry point.
FastAPI server implementing the agentic AI parking system.
"""
import logging
import asyncio
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

from .agents.agent_registry import agent_registry
from .config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Agentic AI Frictionless Parking System",
    description="Production-ready multi-agent AI system for intelligent parking management",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# Request/Response Models
class ParkingRequest(BaseModel):
    """Parking search request model."""
    destination: str
    user_profile: Optional[str] = None
    constraints: Optional[Dict[str, Any]] = {}
    preferences: Optional[Dict[str, Any]] = {}

class ParkingResponse(BaseModel):
    """Parking search response model."""
    status: str
    results: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class NavigationRequest(BaseModel):
    """Navigation request model."""
    destination: Dict[str, Any]
    current_location: Optional[Dict[str, float]] = None

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "service": "Agentic AI Frictionless Parking System",
        "status": "running",
        "version": "1.0.0",
        "agents_loaded": len(agent_registry.agents)
    }

@app.get("/agents")
async def list_agents():
    """List all available agents."""
    return {
        "agents": list(agent_registry.agents.keys()),
        "total": len(agent_registry.agents)
    }

@app.get("/profiles")
async def list_user_profiles():
    """List all available user profiles."""
    return {
        "profiles": {
            name: {
                "name": profile.name,
                "description": profile.description
            }
            for name, profile in settings.USER_PROFILES.items()
        }
    }

@app.post("/parking/search", response_model=ParkingResponse)
async def search_parking(request: ParkingRequest):
    """
    Search for optimal parking spots using the multi-agent system.
    """
    try:
        logger.info(f"Parking search request: {request.destination}")
        
        # Get interaction agent
        interaction_agent = agent_registry.get_agent("interaction")
        if not interaction_agent:
            raise HTTPException(status_code=500, detail="Interaction agent not available")
        
        # Execute parking search workflow
        task_data = {
            "task_type": "find_parking",
            "destination": request.destination,
            "profile_type": request.user_profile,
            "constraints": request.constraints,
            "preferences": request.preferences
        }
        
        result = await interaction_agent.execute_specialized_task(task_data)
        
        if "error" in result:
            return ParkingResponse(status="error", error=result["error"])
        
        return ParkingResponse(status="success", results=result)
        
    except Exception as e:
        logger.error(f"Parking search error: {e}")
        return ParkingResponse(status="error", error=str(e))

@app.post("/navigation/start")
async def start_navigation(request: NavigationRequest):
    """
    Start navigation to selected parking destination.
    """
    try:
        logger.info(f"Navigation request to: {request.destination}")
        
        # Get interaction agent for coordination
        interaction_agent = agent_registry.get_agent("interaction")
        if not interaction_agent:
            raise HTTPException(status_code=500, detail="Interaction agent not available")
        
        # Execute navigation workflow
        task_data = {
            "task_type": "navigate_to_parking", 
            "destination": request.destination,
            "current_location": request.current_location
        }
        
        result = await interaction_agent.execute_specialized_task(task_data)
        
        return {"status": "success", "navigation": result}
        
    except Exception as e:
        logger.error(f"Navigation error: {e}")
        return {"status": "error", "error": str(e)}

@app.post("/feedback")
async def submit_feedback(session_id: str, rating: int, comments: str = ""):
    """
    Submit user feedback for post-trip learning.
    """
    try:
        interaction_agent = agent_registry.get_agent("interaction")
        if not interaction_agent:
            raise HTTPException(status_code=500, detail="Interaction agent not available")
        
        feedback_result = await interaction_agent.collect_feedback(
            {"session_id": session_id}, rating, comments
        )
        
        return feedback_result
        
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/system/metrics") 
async def get_system_metrics():
    """
    Get system performance metrics.
    """
    return {
        "model_config": {
            "model": settings.MODEL_CONFIG.model,
            "temperature": settings.MODEL_CONFIG.temperature,
            "max_tokens": settings.MODEL_CONFIG.max_tokens,
            "top_p": settings.MODEL_CONFIG.top_p
        },
        "agents_status": {
            name: "active" for name in agent_registry.agents.keys()
        },
        "performance_optimizations": {
            "entropy_setting": "low",
            "verbosity": "short",
            "prompt_specificity": "medium",
            "chain_of_thought": "enabled"
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
