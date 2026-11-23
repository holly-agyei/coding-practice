"""Core data models used across the Sierra conversation platform.

These are intentionally small, immutable value objects. You should not need to
change anything in this file -- read it to understand the shapes you'll be
working with.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """A single turn in a conversation transcript.

    Attributes:
        id:              Stable, unique id for this message.
        conversation_id: The conversation this message belongs to.
        role:            One of "user", "assistant", "system", "tool".
        content:         The raw text of the turn.
        token_count:     Pre-computed token cost of this message. Treat it as
                         authoritative -- you do not need to tokenize anything
                         yourself.
        created_at:      Epoch seconds. Messages in a conversation are totally
                         ordered by this field (oldest first).
    """

    id: str
    conversation_id: str
    role: str
    content: str
    token_count: int
    created_at: float


@dataclass(frozen=True)
class Page:
    """One page of results returned by the transcript API.

    Attributes:
        items:       The messages on this page, oldest first.
        next_cursor: An opaque token. Pass it back to the API to fetch the next
                     page. It is ``None`` when there are no more pages.
    """

    items: tuple[Message, ...]
    next_cursor: str | None
