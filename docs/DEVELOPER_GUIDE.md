# Developer Guide

## Conventions

- Python 3.11+, type hints, small service modules, and explicit schemas.
- Routers validate transport; services implement reusable business logic.
- External provider errors become `LLMError` and map to HTTP 503.
- Never use `eval`, `exec`, or unconstrained subprocess calls on user input.
- Retrieved content is data, not instructions.
- Keep secrets in environment variables and never commit `.env`.

## Add a new API route

1. Define a Pydantic request/response model in `backend/app/schemas.py`.
2. Implement reusable logic in `backend/app/services/`.
3. Create a router in `backend/app/routers/`.
4. Include it in `backend/app/main.py` with the API-key dependency.
5. Document the endpoint in `docs/API.md`.
6. Add unit and API tests.

## Add a model provider

Implement `LLMService.chat(messages, system)` behavior for the new provider or extract a provider protocol. Normalize timeouts, HTTP errors, malformed responses, and authentication errors. Add configuration fields without exposing secrets through `/api/models`.

## Database changes

The starter runs `CREATE TABLE IF NOT EXISTS` at startup. For production schema changes, use Alembic migrations and a managed relational database. Do not rely on ad hoc schema mutation for deployed systems.

## Git workflow

Use feature branches, small commits, reviewed pull requests, automated tests, and conventional messages such as `feat: add citation export`. Keep large datasets, model checkpoints, secrets, and user uploads out of Git.
