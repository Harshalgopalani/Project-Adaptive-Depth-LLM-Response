# Comprehensive AI & Business Analysis Glossary

This document serves as the central reference guide for all acronyms, technical machine learning (ML) terminology, software engineering concepts, and business analysis frameworks used throughout the **Project Adaptive Depth** repository.

---

## 1. Domain Acronyms & AI Terminology

| Term / Acronym | Full Form / Concept | Description |
| :--- | :--- | :--- |
| **AI** | Artificial Intelligence | Computer systems capable of performing tasks that historically required human intelligence, such as reasoning, learning, and decision-making. |
| **API** | Application Programming Interface | A software intermediary that allows two applications or models to communicate and exchange data securely. |
| **COGS** | Cost of Goods Sold | Direct expenses associated with producing and delivering a service. In GenAI platforms, COGS is primarily driven by inference compute costs per query. |
| **CSAT** | Customer Satisfaction Score | A metric measuring user satisfaction with a product, service, or feature interaction. |
| **DCD** | Dynamic Contextual Depth | The architectural framework that dynamically routes prompts and modulates LLM output depth according to calculated task complexity. |
| **DAU / MAU** | Daily Active Users / Monthly Active Users | A key product engagement metric evaluating user retention and platform adoption over daily and monthly periods. |
| **EU AI Act** | European Union Artificial Intelligence Act | A comprehensive legal framework regulating AI deployments based on risk categories, transparency requirements, and auditability. |
| **F1-Score** | F1-Score Metric | The harmonic mean of Precision and Recall used in machine learning to evaluate classification accuracy on imbalanced datasets. |
| **GDPR** | General Data Protection Regulation | A European privacy law governing data collection, user consent, data anonymization, and information handling. |
| **GenAI** | Generative Artificial Intelligence | Artificial intelligence models (such as LLMs) capable of generating novel text, code, images, or structured data based on input prompts. |
| **GenUI** | Generative User Interface | A dynamic UI paradigm where components (tables, accordions, code snippets) are generated or rendered dynamically from model outputs. |
| **Groq LPU** | Groq Language Processing Unit | High-speed, low-latency hardware designed specifically for ultra-fast LLM and SLM inference execution. |
| **HITL** | Human-in-the-Loop | A governance and oversight design pattern where human feedback or intervention is integrated into automated AI workflow loops. |
| **JSON** | JavaScript Object Notation | A lightweight data-interchange format easily parsed by frontend software applications and strictly enforced on LLM outputs. |
| **KPI** | Key Performance Indicator | A quantifiable metric used to evaluate success in achieving key business objectives. |
| **LLM** | Large Language Model | A deep learning model trained on massive text datasets capable of general-purpose natural language processing and generation (e.g., GPT-4, Claude). |
| **MAE** | Mean Absolute Error | An ML evaluation metric measuring the average magnitude of errors between predicted values and actual values without considering direction. |
| **ML** | Machine Learning | A branch of AI focused on building algorithms that learn from data to make predictions or decisions without being explicitly programmed. |
| **MoSCoW** | Must have, Should have, Could have, Won't have | A prioritization framework used in business analysis and agile product development to manage requirements scope. |
| **NER** | Named Entity Recognition | An NLP technique used to locate and classify key entities (names, addresses, dates) in unstructured text for PII scrubbing. |
| **NLP** | Natural Language Processing | A field of AI focused on enabling computers to understand, interpret, process, and generate human language. |
| **NFR** | Non-Functional Requirement | System operational constraints such as latency, security, model explainability, availability, and error fallback limits. |
| **PII** | Personally Identifiable Information | Sensitive information that can identify an individual (names, emails, phone numbers) which must be masked for data privacy. |
| **RACI** | Responsible, Accountable, Consulted, Informed | A responsibility assignment matrix clarifying roles across cross-functional teams in business analysis initiatives. |
| **ROI** | Return on Investment | A financial ratio comparing net benefits derived from a initiative relative to its overall capital and operational expenditure. |
| **RTTA** | Read-Time-to-Action | A user experience metric measuring the time required for a user to digest model output and take a productive operational step. |
| **SLM** | Small Language Model | Lightweight, highly optimized language models fine-tuned for specific high-speed classification or routing tasks (e.g., Phi-3, Llama 8B). |
| **TCI** | Task Complexity Index | A numeric score (1–5) assigned by the router model quantifying the reasoning complexity and required depth for a prompt response. |
| **TTFM** | Time-to-First-Meaningful-Content | UX latency benchmark measuring the time elapsed before actionable information is displayed to the user. |
| **TTFT** | Time-to-First-Token | Machine learning latency metric evaluating the time between sending a prompt and receiving the very first output token from the model. |
| **UAT** | User Acceptance Testing | Final testing phase validating that the solution meets business requirements, user expectations, and edge-case handling rules. |
| **UI / UX** | User Interface / User Experience | The visual elements and interactive design of a system, and the overall quality of the end user's interaction with it. |
| **ZDR** | Zero Data Retention | Enterprise API security compliance parameter where third-party model providers guarantee no user data is saved or stored. |

---

## 2. Updated Repository Navigation Map

When incorporating this glossary into your repo, update your main `README.md` navigation block to include the link:

- **`README.md`**: Main Portfolio Landing Page
- **`docs/Business_Requirements_Document.md`**: Core BRD & Requirements Catalog
- **`docs/Architecture_and_Governance.md`**: Data Pipeline & EU AI Act Governance
- **`docs/User_Stories_And_Gherkin.feature`**: Agile Stories & ML Acceptance Criteria
- **`docs/GLOSSARY.md`**: **Central Domain Acronym & Technical Glossary (This Document)**
- **`validation/UAT_Test_Script.md`**: User Acceptance Testing Script
- **`validation/Business_ROI_Matrix.md`**: Financial ROI & ML Success Metrics