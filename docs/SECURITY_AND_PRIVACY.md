# Security, Privacy, and Threat Model

## Current security posture

This package is a local development starter. It provides input validation, extension allowlisting, upload-size limits, a calculator AST allowlist, and an optional shared API key. These measures are not a substitute for production identity, authorization, isolation, or security review.

## Main threats and controls

| Threat | Current control | Required production control |
|---|---|---|
| Unauthorized API use | Optional shared API key | OIDC/session auth, roles, per-user and tenant scopes |
| Prompt injection in files | Retrieved content framed as untrusted | Isolation, content screening, tool permission boundaries, adversarial tests |
| Arbitrary code execution | No shell/code execution tool; safe calculator | Keep execution in dedicated sandbox if added |
| Oversized upload | Configured size limit | Proxy limits, scanning, quotas, decompression-bomb controls |
| Data leakage across users | Single-user local prototype | Tenant-scoped DB queries, authorization tests, row-level security |
| Secret exposure | `.env` ignored | Secrets manager, key rotation, secret scanning |
| Provider data exposure | Provider config is explicit | Vendor review, data minimization, contractual controls |
| Availability attacks | No distributed rate limit | WAF, rate limits, queue limits, circuit breakers |
| Data loss | Local SQLite file | Automated encrypted backups and restore drills |

## Required before public release

- Add real user authentication and authorization.
- Ensure every conversation, memory, and document belongs to an authenticated user/tenant.
- Add HTTPS, secure headers, CSRF protection where cookie-based auth is used, rate limiting, quotas, and abuse controls.
- Store credentials in a secret manager and rotate them.
- Add upload malware scanning and secure object storage.
- Add audit logs and retention/deletion workflows.
- Complete privacy impact and legal review for the markets served.
- Perform dependency scanning, SAST, DAST, penetration testing, and incident-response exercises.

## Privacy principles

Collect only what is necessary. Explain what is sent to a model provider. Avoid storing sensitive personal information in memory. Provide access, correction, export, deletion, retention, and consent controls appropriate to applicable law. Encrypt data in transit and at rest in production.
