# Part 1 — Cursor Pagination

## Context

The transcript service never returns a whole conversation in one shot. It hands
back **pages**. Your first task is to use the provided `ConversationClient` to
retrieve a **complete** conversation transcript.

## Task

Implement in `candidate.py`:

```python
def fetch_all_messages(client: ConversationClient, conversation_id: str) -> list[Message]:
    ...
```

Return every message in the conversation, oldest first.

## Before you start

Read `sierra/client.py`. The method you'll call and the pagination contract
(what a page contains, and how to ask for the next one) are documented there.
Don't assume — read it. You can also poke at it live:

```bash
python -m sierra.sandbox
```

## Requirements

- Return **all** messages for the conversation, in oldest-first order.
- No duplicates and no missing messages across page boundaries.
- Must be correct when the transcript length is an exact multiple of the page
  size, and when it's one more or one less.
- An **empty but existing** conversation returns an empty list.
- An **unknown** conversation should surface the service's error (don't swallow
  it).

## Run

```bash
pytest tests/test_part1.py -q
```

When these pass, move on to Part 2.
