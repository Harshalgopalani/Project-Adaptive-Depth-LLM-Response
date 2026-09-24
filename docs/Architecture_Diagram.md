# System Architecture Flow

```mermaid
graph TD
    A[User Query] --> B[FastAPI Backend]
    B --> C{Groq Intent Router}
    C -- TCI 1-3 (Fact) --> D[Heavy LLM: 150 Token Limit]
    C -- TCI 8-10 (Deep) --> E[Heavy LLM: 2000 Token Limit]
    D --> F[JSON: Executive Anchor Only]
    E --> G[JSON: Anchor + Collapsible Deep Dive]
    F --> H[GenUI Frontend Render]
    G --> H
