"""Sanity checks for the *provided* transcript client.

These should PASS out of the box -- they confirm your environment works and
demonstrate how the pagination API behaves. If these fail, something is wrong
with your setup, not your solution.
"""

import pytest

from sierra import ConversationClient, ConversationNotFound, InvalidCursor
from conftest import make_message


def test_single_page_when_everything_fits():
    msgs = [make_message(i) for i in range(5)]
    client = ConversationClient.from_store({"conv": msgs})

    page = client.get_messages("conv")  # default page size is large enough
    assert len(page.items) == 5
    assert page.next_cursor is None


def test_cursor_advances_across_pages():
    msgs = [make_message(i) for i in range(5)]
    client = ConversationClient.from_store({"conv": msgs})

    page1 = client.get_messages("conv", limit=2)
    assert [m.id for m in page1.items] == ["m0000", "m0001"]
    assert page1.next_cursor is not None

    page2 = client.get_messages("conv", cursor=page1.next_cursor, limit=2)
    assert [m.id for m in page2.items] == ["m0002", "m0003"]


def test_unknown_conversation_raises():
    client = ConversationClient.from_store({"conv": []})
    with pytest.raises(ConversationNotFound):
        client.get_messages("does_not_exist")


def test_empty_conversation_is_one_empty_page():
    client = ConversationClient.from_store({"conv": []})
    page = client.get_messages("conv")
    assert page.items == ()
    assert page.next_cursor is None


def test_bad_cursor_raises():
    client = ConversationClient.from_store({"conv": [make_message(0)]})
    with pytest.raises(InvalidCursor):
        client.get_messages("conv", cursor="not-a-real-cursor")


def test_limit_bounds_are_enforced():
    client = ConversationClient.from_store({"conv": [make_message(0)]})
    with pytest.raises(ValueError):
        client.get_messages("conv", limit=0)
    with pytest.raises(ValueError):
        client.get_messages("conv", limit=ConversationClient.MAX_PAGE_SIZE + 1)
