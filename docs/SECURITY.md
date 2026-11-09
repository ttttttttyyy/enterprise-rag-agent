# Security baseline and production checklist

Implemented in core MVP: token auth, password validators, server-side membership checks, tenant-filtered document and conversation queries, role-gated uploads/deletion/member management, upload size/type allowlist, SHA-256 duplicate check, prompt evidence treated as untrusted, no model secrets in frontend, rate throttling, security headers, and no-answer fallback when AI provider is unavailable.

Before production: enforce HTTPS; rotate secret keys; set DEBUG=0 and exact ALLOWED_HOSTS/CORS; use secure cookie/CSRF settings if moving to session auth; add MFA/OIDC/SSO; scan uploads for malware and isolate parsers; move media to private object storage with signed access; encrypt DB/storage/backups; implement immutable audit event writes; add per-tenant quotas; ensure backup restore tests; pin/scan dependencies; add ACL synchronization and stale-ACL fail-closed behavior; add prompt-injection and cross-tenant negative tests; add OpenTelemetry; configure retention/deletion for backups and provider data; conduct independent penetration test.

The local hash embedding fallback is for offline development only and is not a production-quality semantic embedding.
