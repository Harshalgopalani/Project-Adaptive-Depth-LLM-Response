# AI Architecture & Model Governance Framework
**Project Name:** Project Adaptive Depth (DCD)  

---

## 1. Data Strategy & Pipeline Architecture
The system utilizes a dual telemetry pipeline for continuous monitoring and router fine-tuning.

- **Data Ecosystem:**
  - **Historic Interaction Logs:** Anonymized query logs annotated with ground-truth complexity ratings.
  - **Synthetic Dataset:** 50,000+ synthetic prompts across factual, technical, code, and analytical categories.
  - **Human-Annotated Evaluation Set:** 2,500 expert-labeled prompts for router evaluation.
- **Data Quality Benchmarks:** Fleiss' Kappa inter-annotator agreement score $\ge 0.85$.
- **Privacy Controls:** Automatic PII scrubbing layer (regex + NER) executed at ingress before router intake.

---

## 2. Dual-State Process Workflows

### As-Is Workflow (Monolithic Text Stream)

[User Input] ──> [Heavy Primary LLM] ──> [Unconstrained Token Generation (600+ words)] ──> [Wall of Text Interface]

### To-Be Workflow (Dynamic Contextual Depth)

[User Input]
│
▼
[PII Scrubbing Guardrail]
│
▼
[SLM Router (Groq LPU)] ── Evaluates Task Complexity Index (TCI)
│
├───────► TCI ≤ 2 (Low Complexity) ──> Inject JSON Schema & Token Cap ──► [Executive Anchor UI]
│
└───────► TCI ≥ 3 (High Complexity) ──► Unconstrained Token Budget ─────► [Rich Markdown View]


---

## 3. AI Governance & Regulatory Compliance

### Safety & Guardrails
1. **Schema Fallback:** If the primary LLM produces malformed JSON, a lightweight parser repairs it. If unrepairable within 120ms, the system falls back to standard text streaming.
2. **Confidence Badging:** Responses with low log-probability scores display an automated disclaimer anchor: `[AI Generated - Verification Recommended]`.

### Human-in-the-Loop (HITL) Integration
- Embedded UI feedback controls (`Too Brief` / `Too Detailed`) write directly to the router evaluation queue for weekly fine-tuning cycles.

### Regulatory Alignment (EU AI Act & GDPR)
- **EU AI Act Transparency:** Automated classification pathways and TCI logging satisfy transparency obligations for limited-risk AI systems.
- **GDPR Compliance:** Zero data retention (ZDR) policy on third-party model endpoints; raw input prompts are anonymized prior to long-term telemetry storage.