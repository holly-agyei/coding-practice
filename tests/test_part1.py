"""Part 1 -- fetch_all_messages.

Contract:
  * Returns ALL messages in the conversation, oldest first.
  * Order is stable and matches created_at order.
  * No duplicates and no gaps across page boundaries.
  * Works when the transcript length is an exact multiple of a page size.
  * An empty-but-existing conversation returns [].
  * An unknown conversation propagates ConversationNotFound.

These will FAIL until you implement Part 1 in candidate.py.
"""

import pytest

from sierra import ConversationClient, ConversationNotFound
from conftest import make_message
from candidate import fetch_all_messages


def _client(n, conversation_id="conv"):
    msgs = [make_message(i, conversation_id=conversation_id) for i in range(n)]
    return ConversationClient.from_store({conversation_id: msgs})


def test_returns_everything_in_order():
    client = _client(130)  # well past a single default page
    result = fetch_all_messages(client, "conv")
    assert [m.id for m in result] == [f"m{i:04d}" for i in range(130)]


def test_no_duplicates_or_gaps():
    client = _client(77)
    result = fetch_all_messages(client, "conv")
    ids = [m.id for m in result]
    assert len(ids) == len(set(ids)) == 77


@pytest.mark.parametrize("n", [0, 1, 25, 100, 101])
def test_boundary_lengths(n):
    # includes exact multiples of the default page size (25, 100) and off-by-one.
    client = _client(n)
    result = fetch_all_messages(client, "conv")
    assert len(result) == n


def test_empty_conversation_returns_empty_list():
    client = ConversationClient.from_store({"conv": []})
    assert fetch_all_messages(client, "conv") == []


def test_unknown_conversation_propagates():
    client = ConversationClient.from_store({"conv": []})
    with pytest.raises(ConversationNotFound):
        fetch_all_messages(client, "nope")


def test_only_target_conversation_is_returned():
    store = {
        "conv": [make_message(i, conversation_id="conv") for i in range(30)],
        "other": [make_message(i, conversation_id="other") for i in range(30)],
    }
    client = ConversationClient.from_store(store)
    result = fetch_all_messages(client, "conv")
    assert {m.conversation_id for m in result} == {"conv"}
    assert len(result) == 30
