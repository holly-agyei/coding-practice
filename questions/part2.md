# Part 2 — Context Compaction

## Context

An LLM agent has a bounded context window measured in tokens. As a conversation
grows, you can't keep every message in context — once the running total exceeds
the budget, the **oldest** messages must be dropped. This is "compaction".

You'll build a component that ingests messages one at a time (for example, the
transcript you assembled in Part 1) and maintains a bounded, token-limited view
of the most recent history.

## Task

Implement the `ContextWindow` class in `candidate.py`:

```python
class ContextWindow:
    def __init__(self, max_tokens: int) -> None: ...
    def add(self, message: Message) -> None: ...
    @property
    def messages(self) -> list[Message]: ...        # retained, oldest first
    @property
    def total_tokens(self) -> int: ...
```

Each `Message` carries an authoritative `token_count` (see `sierra/models.py`) —
use it; you do not tokenize anything yourself.

## Required behavior (spec)

- `add(message)` appends the message, then evicts the **oldest** messages until
  the retained messages' combined `token_count` is **at most** `max_tokens`.
- The retained messages are always a **contiguous suffix** of the messages added
  (you never drop a newer message to keep an older one).
- **Boundary:** a total exactly equal to `max_tokens` is fine — no eviction.
- **Oversized message:** the single most-recently-added message is **always**
  retained, even if its own `token_count` exceeds `max_tokens`. In that case it
  is the only message in the window.
- `total_tokens` always reflects the currently retained messages.

> These rules are a constructed spec for the mock (the original interview's exact
> edge-case rules weren't reported). The tests encode them precisely.

## Run

```bash
pytest tests/test_part2.py -q
```

When these pass, move on to Part 3.
