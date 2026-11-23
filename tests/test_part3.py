"""Part 3 -- RetainingContextWindow query retention.

This builds on Part 2: RetainingContextWindow IS a ContextWindow, so eviction
must still work exactly as in Part 2 (not re-tested here except for the
integration case).

Retention policy (the mock spec -- see questions/part3.md):
  * A "query" is the normalized content of a USER-role message. Messages with
    any other role are ignored for retention.
  * Normalization: collapse runs of whitespace to single spaces, strip the
    ends, and lowercase. i.e. " ".join(content.split()).lower().
  * Every user message recorded increments that query's count (repeats count).
  * top_queries(n) returns up to n (normalized_query, count) pairs, ranked by
    count descending, ties broken by MOST RECENT occurrence first.
  * top_queries() with no argument returns at most MAX_RETAINED_QUERIES (20).
  * Query retention is independent of window eviction: a query still counts even
    after its message has been evicted from the live token window.

These will FAIL until you implement Part 3 in candidate.py.
"""

from conftest import make_message
from candidate import RetainingContextWindow


def _user(idx, content, token_count=10):
    return make_message(idx, role="user", content=content, token_count=token_count)


def test_counts_repeated_queries():
    w = RetainingContextWindow(max_tokens=10_000)
    for i in range(3):
        w.add(_user(i, "book a room"))
    w.add(_user(3, "cancel booking"))
    assert w.top_queries() == [("book a room", 3), ("cancel booking", 1)]


def test_non_user_roles_are_ignored():
    w = RetainingContextWindow(max_tokens=10_000)
    w.add(_user(0, "find flights"))
    w.add(make_message(1, role="assistant", content="find flights"))
    w.add(make_message(2, role="tool", content="find flights"))
    assert w.top_queries() == [("find flights", 1)]


def test_normalization_merges_queries():
    w = RetainingContextWindow(max_tokens=10_000)
    w.add(_user(0, "Book A Room"))
    w.add(_user(1, "  book   a room  "))
    w.add(_user(2, "BOOK A ROOM"))
    assert w.top_queries() == [("book a room", 3)]


def test_tie_break_prefers_more_recent():
    w = RetainingContextWindow(max_tokens=10_000)
    w.add(_user(0, "older query"))
    w.add(_user(1, "newer query"))
    # both count==1; the more recently seen ranks first
    assert w.top_queries() == [("newer query", 1), ("older query", 1)]


def test_default_caps_at_twenty():
    w = RetainingContextWindow(max_tokens=10_000)
    for i in range(25):
        w.add(_user(i, f"query number {i}"))
    top = w.top_queries()
    assert len(top) == 20
    names = [q for q, _ in top]
    # all counts are 1, so recency decides: the newest 20 are kept.
    assert "query number 24" in names
    assert "query number 0" not in names


def test_explicit_n_can_exceed_or_shrink():
    w = RetainingContextWindow(max_tokens=10_000)
    for i in range(5):
        w.add(_user(i, f"q{i}"))
    assert len(w.top_queries(2)) == 2
    assert len(w.top_queries(50)) == 5  # never more than what exists


def test_retention_survives_window_eviction():
    # Small window so the first query gets evicted from the live context,
    # but it must still be counted in the retained queries.
    w = RetainingContextWindow(max_tokens=15)
    w.add(_user(0, "evicted query", token_count=10))
    w.add(_user(1, "surviving query", token_count=10))  # evicts message 0
    assert [m.id for m in w.messages] == ["m0001"]  # Part 2 behavior intact
    counts = dict(w.top_queries())
    assert counts == {"evicted query": 1, "surviving query": 1}
