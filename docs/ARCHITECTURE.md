# Architecture

React browser -> Django REST API -> Authentication -> Tenant membership/role policy -> RAG service -> hybrid retrieval (PostgreSQL full-text + pgvector) -> evidence-bounded OpenAI generation -> citation payload -> React.

Ingestion: multipart upload -> validation -> private media volume -> Celery task -> extraction (PDF/DOCX/TXT) -> chunking -> embeddings -> PostgreSQL chunks/vector + lexical generated column -> document status.

Security invariants: the client never supplies trusted membership; tenant membership is resolved server-side. Retrieval starts from tenant-filtered chunks and approved/indexed documents. Evidence text is untrusted and cannot override system policy. Missing provider configuration yields a transparent no-answer response.
