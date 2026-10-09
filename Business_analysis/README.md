# Project Adaptive Depth: Evolving Text-LLM Interfaces Beyond the "Wall of Text"

![AI Domain](https://img.shields.io/badge/Domain-Enterprise_AI_%26_GenUI-blue)
![Architecture](https://img.shields.io/badge/Architecture-Decoupled_SLM%2FLLM-orange)
![Lifecycle](https://img.shields.io/badge/Lifecycle-End--to--End_AI_Business_Analysis-green)
![Status](https://img.shields.io/badge/Status-Recruiter--Ready_Case_Study-brightgreen)

## Executive Summary
Traditional LLM interfaces default to exhaustive verbosity, serving 500+ word "walls of text" regardless of user query complexity. This creates cognitive friction for users and inflates inference API expenditures on redundant tokens. 

**Project Adaptive Depth** introduces **Dynamic Contextual Depth (DCD)**—a decoupled AI architecture that pairs an ultra-fast **Small Language Model (SLM) Intent Router** running on low-latency infrastructure with a **Heavy Primary LLM**. The router evaluates prompt complexity in under 50ms and dynamically constrains output formats, cutting inference COGS by **15–22%** and reducing user **Read-Time-to-Action (RTTA)** by **40%**.

---

## Strategic Highlights & Core Metrics

| Key Metric | Baseline (Traditional LLM) | Target Outcome (DCD Architecture) |
| :--- | :--- | :--- |
| **Average Output Tokens** | 800 tokens / query | **180 tokens / query** (Low-complexity queries) |
| **Inference Compute COGS** | 100% baseline expense | **15–22% net cost reduction** per session |
| **Time-to-First-Meaningful-Content** | High (delayed by preambles) | **35% faster execution** |
| **User Engagement (DAU/MAU)** | Baseline retention | **18% increase** in task completion rates |

---

## Repository Artifact Navigation

- **[Business Requirements Document (BRD)](docs/Business_Requirements_Document.md):** Problem statement, RACI matrix, and prioritized Functional/Non-Functional requirements catalog.
- **[Architecture & AI Governance](docs/Architecture_and_Governance.md):** Data strategy, dual-state workflows (As-Is vs. To-Be), safety guardrails, and EU AI Act alignment.
- **[Agile User Stories & Gherkin Specs](docs/User_Stories_And_Gherkin.feature):** Functional requirements translated into Gherkin syntax with ML model benchmarks.
- **[UAT Test Script & Edge Cases](validation/UAT_Test_Script.md):** Model validation scenarios covering adversarial inputs and system fallbacks.
- **[Business ROI & Technical Validation](validation/Business_ROI_Matrix.md):** Dual-sided success matrix mapping ML metrics to financial value.

---

## Architecture Overview