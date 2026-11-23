"""Public client for the Sierra transcript service.

This is the main entry point you'll use. Read the docstrings carefully -- the
pagination contract is described here and is the thing you must work with in
Part 1.
"""

from __future__ import annotations

from ._backend import ConversationNotFound, InMemoryBackend, InvalidCursor
from .models import Page

__all__ = ["ConversationClient", "ConversationNotFound", "InvalidCursor"]


class ConversationClient:
    """Reads conversation transcripts from the (simulated) transcript service.

    The service never returns an entire transcript at once. Instead it returns
    *pages*: a chunk of messages plus a cursor that points at the next chunk.

    Example::

        client = ConversationClient.from_store({"conv_1": [...]})
        page = client.get_messages("conv_1")
        page.items        # -> up to `limit` Message objects, oldest first
        page.next_cursor  # -> opaque str, or None when the transcript is done

    Notes:
        * Cursors are opaque. Do not try to construct or parse them -- only ever
          pass back a value the service previously handed you.
        * Messages within a conversation are returned oldest-first and the
          ordering is stable across pages.
    """

    #: Page size used when the caller does not specify one.
    DEFAULT_PAGE_SIZE = 25

    #: Hard upper bound the service will accept for ``limit``.
    MAX_PAGE_SIZE = 100

    def __init__(self, backend: InMemoryBackend) -> None:
        self._backend = backend

    @classmethod
    def from_store(cls, store: dict) -> "ConversationClient":
        """Convenience constructor around an in-memory transcript store."""
        return cls(InMemoryBackend(store))

    def get_messages(
        self,
        conversation_id: str,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Page:
        """Fetch a single page of messages for ``conversation_id``.

        Args:
            conversation_id: Which conversation to read.
            cursor:          ``None`` for the first page, otherwise the
                             ``next_cursor`` from the previous page.
            limit:           Max messages to return on this page. Defaults to
                             ``DEFAULT_PAGE_SIZE``.

        Returns:
            A :class:`~sierra.models.Page`.

        Raises:
            ConversationNotFound: The conversation id does not exist.
            InvalidCursor:        The cursor is malformed.
            ValueError:           ``limit`` is not in ``1..MAX_PAGE_SIZE``.
        """
        if limit is None:
            limit = self.DEFAULT_PAGE_SIZE
        if not (1 <= limit <= self.MAX_PAGE_SIZE):
            raise ValueError(
                f"limit must be between 1 and {self.MAX_PAGE_SIZE}, got {limit}"
            )
        return self._backend.get_page(conversation_id, cursor, limit)
