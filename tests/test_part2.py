"""Part 2 -- ContextWindow compaction.

Contract (the "spec"):
  * add(message) appends the message, then evicts the OLDEST messages until the
    retained messages' total token_count <= max_tokens.
  * messages are kept oldest-first and are always a contiguous suffix of what
    was added (you never drop something newer to keep something older).
  * BOUNDARY: a total exactly equal to max_tokens is allowed (no eviction).
  * OVERSIZED RULE: the single most-recently-added message is always retained,
    even if its token_count alone exceeds max_tokens. In that case it is the
    only message in the window.
  * total_tokens reflects the retained messages.

These will FAIL until you implement Part 2 in candidate.py.
"""

from conftest import make_message
from candidate import ContextWindow


def _add_all(window, messages):
    for m in messages:
        window.add(m)
    return window


def test_everything_fits_keeps_all():
    window = ContextWindow(max_tokens=100)
    msgs = [make_message(i, token_count=10) for i in range(5)]
    _add_all(window, msgs)
    assert [m.id for m in window.messages] == [m.id for m in msgs]
    assert window.total_tokens == 50


def test_evicts_oldest_first():
    window = ContextWindow(max_tokens=30)
    msgs = [make_message(i, token_count=10) for i in range(5)]
    _add_all(window, msgs)
    # Only the last 3 (30 tokens) fit.
    assert [m.id for m in window.messages] == ["m0002", "m0003", "m0004"]
    assert window.total_tokens == 30


def test_exact_boundary_keeps_message():
    window = ContextWindow(max_tokens=20)
    msgs = [make_message(i, token_count=10) for i in range(2)]
    _add_all(window, msgs)
    assert len(window.messages) == 2
    assert window.total_tokens == 20


def test_eviction_happens_incrementally():
    window = ContextWindow(max_tokens=25)
    window.add(make_message(0, token_count=10))
    window.add(make_message(1, token_count=10))
    assert window.total_tokens == 20
    window.add(make_message(2, token_count=10))  # 30 > 25 -> drop oldest
    assert [m.id for m in window.messages] == ["m0001", "m0002"]
    assert window.total_tokens == 20


def test_oversized_newest_message_is_kept_alone():
    window = ContextWindow(max_tokens=15)
    window.add(make_message(0, token_count=10))
    window.add(make_message(1, token_count=50))  # alone exceeds the budget
    assert [m.id for m in window.messages] == ["m0001"]
    assert window.total_tokens == 50


def test_retained_is_always_a_suffix():
    window = ContextWindow(max_tokens=35)
    msgs = [make_message(i, token_count=token) for i, token in enumerate([10, 20, 5, 30])]
    _add_all(window, msgs)
    kept_ids = [m.id for m in window.messages]
    all_ids = [m.id for m in msgs]
    # kept must be a contiguous tail of all_ids
    assert all_ids[len(all_ids) - len(kept_ids):] == kept_ids
