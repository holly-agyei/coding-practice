"""YOUR WORKSPACE.

This is the only file you need to edit. Implement the three functions/classes
below. Each is exercised by a test file under ``tests/``.

Run the tests with::

    pytest -q                 # everything
    pytest tests/test_part1.py -q   # just one part

The transcript service you'll be working against lives in the ``sierra``
package. Start by reading ``sierra/client.py`` and ``sierra/models.py``.
"""

from __future__ import annotations

from sierra import ConversationClient, Message


# =============================================================================
# PART 1 -- Load a full transcript
# =============================================================================
def fetch_all_messages(
    client: ConversationClient, conversation_id: str
) -> list[Message]:
    """Return every message in ``conversation_id``, oldest first.

    The service hands back transcripts one page at a time. Your job is to use
    the client to assemble the complete, correctly-ordered history.

    See tests/test_part1.py for the exact contract.
    """
    # TODO(candidate): implement Part 1.
    raise NotImplementedError


# =============================================================================
# PART 2 -- Context-window compaction
# =============================================================================
class ContextWindow:
    """A bounded, token-limited view over a running conversation.

    Messages are fed in one at a time via :meth:`add`. The window keeps a
    contiguous suffix of the most recent messages whose combined token count
    fits the budget, evicting the oldest messages as needed.

    See tests/test_part2.py for the exact contract (including the boundary and
    oversized-message rules you must honor).
    """

    def __init__(self, max_tokens: int) -> None:
        self.max_tokens = max_tokens
        # TODO(candidate): choose your internal representation.

    def add(self, message: Message) -> None:
        """Append ``message`` to the window, evicting as required by the budget."""
        # TODO(candidate): implement Part 2.
        raise NotImplementedError

    @property
    def messages(self) -> list[Message]:
        """The retained messages, oldest first."""
        # TODO(candidate): implement Part 2.
        raise NotImplementedError

    @property
    def total_tokens(self) -> int:
        """Sum of ``token_count`` over the retained messages."""
        # TODO(candidate): implement Part 2.
        raise NotImplementedError


# =============================================================================
# PART 3 -- Query retention (builds on Part 2)
# =============================================================================
class RetainingContextWindow(ContextWindow):
    """A :class:`ContextWindow` that also remembers the most frequent user
    queries, even after they've been evicted from the live window.

    See tests/test_part3.py for the retention policy you must implement.
    """

    #: How many distinct queries to retain at most.
    MAX_RETAINED_QUERIES = 20

    def __init__(self, max_tokens: int) -> None:
        super().__init__(max_tokens)
        # TODO(candidate): set up whatever you need to track queries.

    def top_queries(self, n: int | None = None) -> list[tuple[str, int]]:
        """Return up to ``n`` ``(query, count)`` pairs, most frequent first.

        Defaults to :attr:`MAX_RETAINED_QUERIES` when ``n`` is None.
        See tests/test_part3.py for normalization, ranking and tie-breaking.
        """
        # TODO(candidate): implement Part 3.
        raise NotImplementedError
