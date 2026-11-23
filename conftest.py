"""Shared pytest fixtures/helpers. Makes the project root importable and
provides small builders so each test can set up precise transcripts.
"""

from __future__ import annotations

import pytest

from sierra import ConversationClient, Message


def make_message(
    idx: int,
    *,
    conversation_id: str = "conv",
    role: str = "user",
    content: str | None = None,
    token_count: int = 10,
) -> Message:
    """Build a Message with a monotonically increasing timestamp from ``idx``."""
    return Message(
        id=f"m{idx:04d}",
        conversation_id=conversation_id,
        role=role,
        content=content if content is not None else f"message {idx}",
        token_count=token_count,
        created_at=1_700_000_000.0 + idx,
    )


@pytest.fixture
def make_message_factory():
    return make_message


@pytest.fixture
def client_factory():
    """Returns a function: list[Message] (+ optional extra convos) -> client."""

    def _factory(messages, conversation_id="conv", extra=None):
        store = {conversation_id: list(messages)}
        if extra:
            store.update(extra)
        return ConversationClient.from_store(store)

    return _factory
