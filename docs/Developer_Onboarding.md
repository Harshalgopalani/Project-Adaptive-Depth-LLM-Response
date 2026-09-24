# Developer Onboarding & Execution Runbook

Welcome to the Project Adaptive Depth repository. This guide explains the exact lifecycle of a user query flowing through the DCD architecture to help you onboard quickly.

## The DCD Request Lifecycle

1. **Server Initialization (Lifespan Event):** 
   Upon FastAPI boot, the `lifespan` context manager initializes the `GroqIntentRouter` singleton and allocates the `AsyncLRUCache`. This ensures resources are not wastefully re-initialized per request.
2. **Request Intercept & Validation:** 
   A POST request hits `/api/v1/query`. Pydantic strictly validates the payload. If the payload is malformed, a 422 Unprocessable Entity is returned immediately.
3. **Speed Layer (Routing Classification):** 
   The request is passed to the Groq Router. It first checks the $O(1)$ LRU Cache. On a cache miss, it pings the Groq LPU to calculate the Task Complexity Index (TCI). It returns strict JSON telemetry (token limits, schema requirements).
4. **Logic Layer (Prompt Assembly):** 
   The `PromptManager` reads the TCI score and dynamically injects the correct persona and maximum token budget constraints from `constrained_prompts.json` into the primary LLM system prompt.
5. **Presentation Layer (GenUI Handoff):** 
   The heavy LLM generates a strictly formatted JSON response. FastAPI casts this into the `ProgressiveUIResponse` Pydantic model and returns it to the client for modular, accordion-style rendering.
