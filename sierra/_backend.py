"""Simulated transcript storage.

This stands in for a real, remote transcript service. The details of how pages
and cursors are produced are deliberately abstracted away -- in production this
would be a network call to a paginated HTTP endpoint. You generally should not
need to read or depend on anything in here directly; interact with the service
through ``sierra.client.ConversationClient`` instead.
"""

from __future__ import annotations

import base64
import json

from .models import Message, Page


class ConversationNotFound(KeyError):
    """Raised when a conversation id does not exist."""


class InvalidCursor(ValueError):
    """Raised when a cursor is malformed or does not belong to this service."""


def _encode_cursor(offset: int) -> str:
    raw = json.dumps({"o": offset}, separators=(",", ":")).encode("utf-8")
    return base64.urlsafe_b64encode(raw).decode("ascii")


def _decode_cursor(cursor: str) -> int:
    try:
        raw = base64.urlsafe_b64decode(cursor.encode("ascii"))
        offset = json.loads(raw)["o"]
    except Exception as exc:  # noqa: BLE001 - any decode failure is invalid
        raise InvalidCursor(f"malformed cursor: {cursor!r}") from exc
    if not isinstance(offset, int) or offset < 0:
        raise InvalidCursor(f"malformed cursor: {cursor!r}")
    return offset


class InMemoryBackend:
    """Holds conversation transcripts in memory and serves them in pages.

    The store maps ``conversation_id -> list[Message]`` with each list kept
    sorted oldest-first by ``created_at``.
    """

    def __init__(self, store: dict[str, list[Message]] | None = None) -> None:
        self._store: dict[str, list[Message]] = {}
        for cid, messages in (store or {}).items():
            self._store[cid] = sorted(messages, key=lambda m: m.created_at)

    def get_page(self, conversation_id: str, cursor: str | None, limit: int) -> Page:
        if conversation_id not in self._store:
            raise ConversationNotFound(conversation_id)

        messages = self._store[conversation_id]
        offset = 0 if cursor is None else _decode_cursor(cursor)

        window = messages[offset : offset + limit]
        next_offset = offset + limit
        next_cursor = _encode_cursor(next_offset) if next_offset < len(messages) else None

        return Page(items=tuple(window), next_cursor=next_cursor)
