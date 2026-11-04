# Architecture Decision Records (ADRs)

## ADR-001 — FastAPI for the backend

**Decision:** Use FastAPI for the first integrated service.  
**Reason:** Typed request schemas, OpenAPI generation, async HTTP calls, and a straightforward Python integration path.  
**Trade-off:** A single API process is not a complete distributed architecture.

## ADR-002 — SQLite for the local starter

**Decision:** Use SQLite for local persistence.  
**Reason:** No external database is required to run the prototype.  
**Trade-off:** Use PostgreSQL and migrations before multi-user production or multi-worker scaling.

## ADR-003 — Provider abstraction

**Decision:** Support mock, Gemini, and Ollama inference through one adapter.  
**Reason:** Enables local mock-mode testing, cloud testing through Gemini, local inference through Ollama, and a future native NexoraLM implementation without rewriting the product UI/API.  
**Trade-off:** Provider-specific features such as streaming/tool-call formats need normalized adapters later.

## ADR-004 — Explicit memory

**Decision:** Memory is created and deleted by explicit user action in the initial version.  
**Reason:** Predictable privacy and inspectability.  
**Trade-off:** Less automatic personalization until consented extraction and review workflows are designed.

## ADR-005 — Bounded agents

**Decision:** Specialist agents generate text but cannot execute arbitrary code or external side effects.  
**Reason:** Keeps the initial agent system testable and reduces risk.  
**Trade-off:** Future automation needs typed tools, sandboxing, user approval, and audit trails.

## ADR-006 — Small standalone NexoraLM prototype

**Decision:** Include a minimal educational Transformer separate from the serving provider.  
**Reason:** Makes model architecture and training mechanics inspectable without claiming a large pretrained model.  
**Trade-off:** It has toy-scale capacity and must not be positioned as production intelligence.
