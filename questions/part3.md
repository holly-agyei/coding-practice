# Part 3 — Query Retention

## Context

Beyond the live context window, the agent wants a longer-lived memory of **what
users keep asking for** — the most frequent user queries over the whole
conversation, even after those messages have scrolled out of the live window.
You'll extend Part 2 to maintain this.

## Task

Implement `RetainingContextWindow` in `candidate.py`. It **subclasses**
`ContextWindow`, so all of Part 2's compaction behavior must keep working:

```python
class RetainingContextWindow(ContextWindow):
    MAX_RETAINED_QUERIES = 20
    def top_queries(self, n: int | None = None) -> list[tuple[str, int]]: ...
```

## Retention policy (mock spec)

> ⚠️ **Provenance:** reported accounts said Part 3 involved *"keep the top ~20
> queries and handle repeated queries,"* but the exact original requirements
> were **not** reported. The policy below is a reasonable, clearly specified
> mock. Treat it as the authoritative contract for this exercise.

- A **query** is the normalized `content` of a **user**-role message. Messages
  with any other role (`assistant`, `tool`, `system`) are ignored for retention.
- **Normalization:** collapse internal whitespace to single spaces, strip the
  ends, and lowercase. Concretely: `" ".join(content.split()).lower()`.
- Every recorded user message **increments the count** for its normalized query.
  Repeated queries therefore accumulate counts.
- `top_queries(n)` returns up to `n` `(normalized_query, count)` pairs, ranked by
  **count descending**, with ties broken by **most recent occurrence first**.
- `top_queries()` with no argument returns at most `MAX_RETAINED_QUERIES` (20).
- Never return more pairs than distinct queries actually seen.
- **Independence:** query retention is separate from window eviction — a query
  still counts even after its message has been evicted from the live window.

## Run

```bash
pytest tests/test_part3.py -q
```

## Stretch (if time allows — not tested)

- How would you bound memory if the number of *distinct* queries were unbounded?
- How would you make retention survive across multiple conversations?
