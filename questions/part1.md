# Part 1 — Conversation History

## Context

Sierra's conversational agents interact with customers across multiple turns.
These conversations are stored in a transcript service that returns messages in
pages rather than all at once.

You are provided with a `ConversationClient` that communicates with this service.

## Task

Implement the following function in `candidate.py`:

```python
def fetch_all_messages(client: ConversationClient, conversation_id: str) -> list[Message]:
    ...
```

The function should retrieve the complete conversation history for the given
conversation ID and return all messages in chronological order, from oldest to
newest.

## Requirements

- Return every message in the conversation.
- Preserve the original chronological order.
- Ensure no messages are duplicated or skipped across pages.
- Handle conversations whose lengths fall exactly on page boundaries, as well as
  those with partially filled final pages.
- Return an empty list for an existing conversation containing no messages.
- Propagate the service's error when the conversation ID does not exist.

You may use the existing codebase and provided client interfaces to implement the
solution.

## Run

```bash
pytest tests/test_part1.py -q
```

When these pass, move on to Part 2.
