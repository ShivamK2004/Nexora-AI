# Testing Strategy

## Run current tests

```bash
python -m unittest discover -s tests -v
```

The API test uses a temporary directory and mock provider. It should not require Ollama or GPU hardware.

## Current coverage

- Arithmetic tool accepts simple arithmetic and rejects code-like expressions.
- Text chunking creates non-empty chunks.
- Byte tokenizer round-trips Unicode text.
- Health route returns a successful status.
- Chat API responds in mock mode.
- Calculator API returns expected result.

## Add before production

- Provider contract tests against mocked HTTP responses.
- File parser tests for malformed PDFs and maximum-size boundary.
- Retrieval precision/recall and citation correctness.
- Memory deletion and conversation isolation tests.
- Agent prompt-injection and permission-boundary tests.
- AuthN/AuthZ and cross-tenant IDOR tests.
- Concurrency, load, soak, failure-recovery, and backup restore tests.
- Model evaluation suite covering factuality, coding, reasoning, multilingual behavior, and safety.
