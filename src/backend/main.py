"""
Dynamic Contextual Depth (DCD) - API Orchestration Layer
Author: Harshal Gopalani
Description: FastAPI backend coordinating the Speed Layer (Groq Router) 
and Logic Layer (Heavy LLM). Implements singleton resource management, 
dependency injection, and asynchronous request handling.
"""

import time
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from typing import Optional

# Assuming the router script is in the same module path
# from src.router.groq_intent_classifier import GroqIntentRouter, RoutingTelemetry

# ---------------------------------------------------------
# 1. Pydantic Schemas (API Contracts)
# ---------------------------------------------------------

class UserQueryRequest(BaseModel):
    query: str = Field(..., min_length=2, max_length=2000, description="The user's input prompt.")
    user_id: str = Field(..., description="Unique identifier for telemetry and rate limiting.")

class ProgressiveUIResponse(BaseModel):
    executive_anchor: str = Field(..., description="Bold, 2-sentence summary for immediate RTTA.")
    collapsible_content: Optional[str] = Field(None, description="Detailed text for deep-dives, revealed on-demand.")
    task_complexity: int = Field(..., description="TCI score returned by the router.")
    total_latency_ms: float = Field(..., description="Total time taken for the entire pipeline.")

# ---------------------------------------------------------
# 2. Resource Management (Singleton Pattern via Lifespan)
# ---------------------------------------------------------
# FAANG Practice: Never initialize database connections or ML models globally.
# Use ASGI lifespan events to manage state and ensure clean tear-downs.

class AppState:
    router = None # Will hold our GroqIntentRouter instance

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize the router and its thread-safe LRU Cache once.
    logging.info("Initializing Groq Intent Router and LRU Cache...")
    # AppState.router = GroqIntentRouter() 
    yield
    # Shutdown: Clean up resources, flush logs, close client connections.
    logging.info("Tearing down backend connections...")
    AppState.router = None

# Initialize FastAPI with the lifespan manager
app = FastAPI(
    title="Project Adaptive Depth API",
    version="1.0.0",
    lifespan=lifespan
)
logger = logging.getLogger("DCD_Backend")

# ---------------------------------------------------------
# 3. Heavy LLM Interface (Decoupled Logic Layer)
# ---------------------------------------------------------

class HeavyLLMService:
    """
    Interface for the primary text LLM (Claude/GPT-4). 
    Abstracted to allow easy swapping of foundational models without breaking the API.
    """
    @staticmethod
    async def generate_constrained_response(prompt: str, telemetry: dict) -> dict: # telemetry: RoutingTelemetry
        # Mocking network I/O for the primary LLM
        # In production, this passes telemetry.suggested_max_tokens to the LLM's API
        logger.info(f"Generating content constrained to {telemetry.get('suggested_max_tokens', 150)} tokens.")
        
        # Simulate network latency based on complexity
        await asyncio.sleep(0.5 if telemetry.get("task_complexity_index", 1) < 5 else 1.5)
        
        return {
            "executive_anchor": "This is the ultra-fast, strictly bounded core answer.",
            "collapsible_content": "This is the deeper context generated only because the TCI demanded it." 
                                   if telemetry.get("task_complexity_index", 1) >= 5 else None
        }

# Dependency Injection for the service
def get_llm_service() -> HeavyLLMService:
    return HeavyLLMService()

# ---------------------------------------------------------
# 4. Main API Endpoint
# ---------------------------------------------------------

@app.post("/api/v1/query", response_model=ProgressiveUIResponse)
async def handle_query(
    request_data: UserQueryRequest,
    llm_service: HeavyLLMService = Depends(get_llm_service)
):
    """
    Primary orchestration endpoint. 
    1. Intercepts query. 2. Classifies intent. 3. Bounds heavy generation.
    """
    start_time = time.perf_counter()
    logger.info(f"Received query from user: {request_data.user_id}")

    try:
        # Step 1: Speed Layer (Sub-50ms Routing)
        # telemetry = await AppState.router.classify_intent(request_data.query)
        
        # Mocking telemetry for this code block's execution
        mock_telemetry = {
            "task_complexity_index": 7,
            "suggested_max_tokens": 500,
            "requires_json_schema": True
        }

        # Step 2: Logic Layer (Constrained Generation)
        llm_payload = await llm_service.generate_constrained_response(
            request_data.query, 
            mock_telemetry
        )

        total_latency = (time.perf_counter() - start_time) * 1000

        # Step 3: Presentation Layer Payload
        return ProgressiveUIResponse(
            executive_anchor=llm_payload["executive_anchor"],
            collapsible_content=llm_payload["collapsible_content"],
            task_complexity=mock_telemetry["task_complexity_index"],
            total_latency_ms=total_latency
        )

    except Exception as e:
        logger.error(f"Pipeline failure: {str(e)}")
        # Never leak raw stack traces to the client in production
        raise HTTPException(
            status_code=500, 
            detail="An error occurred while generating the adaptive response."
        )
