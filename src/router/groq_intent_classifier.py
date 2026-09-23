"""
Dynamic Contextual Depth (DCD) - Speed Layer Intent Router
Author: Harshal Gopalani
Description: An ultra-low latency (<50ms) intent classifier using Groq LPU.
Implements an O(1) Async LRU Cache, Pydantic strict schemas, and a Circuit Breaker pattern.
"""

import os
import time
import logging
import asyncio
from enum import Enum
from collections import OrderedDict
from typing import Optional
from pydantic import BaseModel, Field, ValidationError
from groq import AsyncGroq, APIError

# ---------------------------------------------------------
# 1. Telemetry Data Structures (Strict Pydantic Validation)
# ---------------------------------------------------------

class IntentType(str, Enum):
    FACTUAL = "FACTUAL"
    SUMMARY = "SUMMARY"
    ANALYTICAL = "ANALYTICAL"
    CODING = "CODING"
    AGENTIC = "AGENTIC"

class RoutingTelemetry(BaseModel):
    intent_type: IntentType = Field(
        ..., description="Classified intent of the prompt."
    )
    task_complexity_index: int = Field(
        ..., ge=1, le=10, description="TCI from 1 (simple fact) to 10 (multi-hop)."
    )
    suggested_max_tokens: int = Field(
        ..., description="Recommended output token budget for the heavy LLM."
    )
    requires_json_schema: bool = Field(
        ..., description="True if the heavy LLM should output strict JSON components."
    )

# ---------------------------------------------------------
# 2. Custom DSA: Thread-Safe Async LRU Cache
# ---------------------------------------------------------
# FAANG Flex: Using an OrderedDict provides O(1) lookups and O(1) updates
# while maintaining insertion order to easily evict the Least Recently Used item.

class AsyncLRUCache:
    def __init__(self, capacity: int = 1000):
        self.cache = OrderedDict()
        self.capacity = capacity
        self.lock = asyncio.Lock() # Prevents race conditions in high-concurrency environments

    async def get(self, key: str) -> Optional[RoutingTelemetry]:
        async with self.lock:
            if key not in self.cache:
                return None
            self.cache.move_to_end(key) # Mark as recently used
            return self.cache[key]

    async def put(self, key: str, value: RoutingTelemetry):
        async with self.lock:
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = value
            if len(self.cache) > self.capacity:
                self.cache.popitem(last=False) # Evict the LRU item

# ---------------------------------------------------------
# 3. The Router Implementation (with Circuit Breaker)
# ---------------------------------------------------------

class GroqIntentRouter:
    def __init__(self, model: str = "llama-3.1-8b-instant"):
        # Asynchronous client for non-blocking network I/O
        self.client = AsyncGroq(
            api_key=os.environ.get("GROQ_API_KEY"),
            max_retries=1,
            timeout=2.0 # Strict 2-second timeout for the routing layer
        )
        self.model = model
        self.cache = AsyncLRUCache(capacity=500)
        
        # Circuit Breaker State
        self._circuit_open = False
        self._circuit_open_time = 0
        self.cooldown_seconds = 30
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("DCD_IntentRouter")

    async def classify_intent(self, prompt: str) -> RoutingTelemetry:
        """Main routing method. Intercepts prompt and calculates TCI."""
        start_time = time.perf_counter()

        # Check Cache first (0ms TTFT)
        cached_result = await self.cache.get(prompt)
        if cached_result:
            self.logger.info("Cache HIT. Bypassing inference.")
            return cached_result

        # Check Circuit Breaker
        if self._circuit_open:
            if time.time() - self._circuit_open_time > self.cooldown_seconds:
                self.logger.info("Circuit half-open, attempting inference...")
                self._circuit_open = False
            else:
                self.logger.warning("Circuit OPEN. Returning O(1) heuristic fallback.")
                return self._get_fallback_telemetry()

        # Construct System Prompt injecting the Pydantic schema
        schema_json = RoutingTelemetry.model_json_schema()
        system_msg = (
            "You are a sub-50ms intent router. Classify the user prompt complexity. "
            f"You MUST output valid JSON strictly matching this schema: {schema_json}"
        )

        try:
            # Groq API Call forcing JSON output
            chat_completion = await self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                response_format={"type": "json_object"},
                temperature=0.0 # Deterministic output
            )
            
            raw_response = chat_completion.choices[0].message.content
            
            # Strict Validation
            telemetry = RoutingTelemetry.model_validate_json(raw_response)
            await self.cache.put(prompt, telemetry)
            
            latency_ms = (time.perf_counter() - start_time) * 1000
            self.logger.info(f"Groq Routing Success | Latency: {latency_ms:.2f}ms | TCI: {telemetry.task_complexity_index}")
            
            return telemetry

        except (APIError, ValidationError, Exception) as e:
            self.logger.error(f"Routing Failed: {str(e)}. Tripping Circuit Breaker.")
            self._circuit_open = True
            self._circuit_open_time = time.time()
            return self._get_fallback_telemetry()

    def _get_fallback_telemetry(self) -> RoutingTelemetry:
        """Safe default parameters if the routing layer goes offline."""
        return RoutingTelemetry(
            intent_type=IntentType.ANALYTICAL,
            task_complexity_index=5,
            suggested_max_tokens=500,
            requires_json_schema=False
        )

# ---------------------------------------------------------
# 4. Local Execution Test
# ---------------------------------------------------------
if __name__ == "__main__":
    async def run_test():
        os.environ["GROQ_API_KEY"] = "dummy_key_for_local_testing"
        router = GroqIntentRouter()
        
        print("\n--- Simulating User Prompt ---")
        prompt = "What is the capital of France?"
        print(f"Prompt: {prompt}")
        
        telemetry = await router.classify_intent(prompt)
        print("\n--- Output Telemetry ---")
        print(telemetry.model_dump_json(indent=2))

    asyncio.run(run_test())
