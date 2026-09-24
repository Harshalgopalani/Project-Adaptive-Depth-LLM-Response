# Stakeholder Alignment & FAQ

This document outlines key pushbacks from executive leadership and the approved strategic responses regarding the DCD Architecture.

### Q1 (CEO): Will adding a routing model before the main LLM increase Time-to-First-Token (TTFT) and make the app feel sluggish?
**Response:** We are utilizing hyper-fast inference (Groq LPU) for the router, taking only ~50ms. Because the router aggressively restricts the `max_tokens` the heavy LLM needs to generate, the Time-to-Value actually drops. The user gets their core answer much faster because the text stream isn't blocked by the LLM generating a useless 150-token preamble.

### Q2 (VP of AI Engineering): If we force a text LLM to output strict JSON schemas instead of free-flowing text, will we degrade its reasoning capabilities?
**Response:** We only enforce tight token constraints and rigid schemas on low-complexity factual queries. For queries requiring multi-hop reasoning, Agentic workflows, or complex synthesis, the SLM Router detects the high complexity (TCI > 7) and grants the primary LLM a massive token budget and a flexible schema to "think" before it outputs the final text.

### Q3 (VP of Finance): Why build this complex UI layer? Can't we just put a system prompt in the background that says 'be concise'?
**Response:** A static 'be concise' prompt permanently lobotomizes the LLM. If a user actually needs a deep, comprehensive answer, a globally concise LLM will fail them. Our architecture dynamically scales the text depth per query, allowing us to serve both the novice and the expert seamlessly without requiring manual prompt-engineering.
