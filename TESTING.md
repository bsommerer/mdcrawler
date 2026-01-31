# Test Strategy

## Goals
- Verify link extraction and URL normalization without network access.
- Ensure recursive crawling schedules newly discovered URLs in parallel worker flow.
- Validate Markdown rendering for image placeholders.

## Scope
- Unit tests for content extraction, crawler recursion, and Markdown rendering.
- Network-bound behavior is mocked to keep tests fast and deterministic.

## Running tests

```bash
pytest
```
