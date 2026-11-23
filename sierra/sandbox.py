"""Sample data + a tiny demo so you can poke at the client interactively.

Run it directly to see the API in action::

    python -m sierra.sandbox

This is only here to help you explore. Nothing you build needs to import it.
"""

from __future__ import annotations

from .client import ConversationClient
from .models import Message

# A fictional hotel-booking assistant conversation. Token counts are made up but
# plausible; roles alternate like a real agent transcript.
_TURNS = [
    ("user", "Hi, I need a room in Lisbon for next weekend", 12),
    ("assistant", "Happy to help! What dates and how many guests?", 11),
    ("user", "Friday to Sunday, two adults", 7),
    ("assistant", "Found 14 hotels. Do you have a neighborhood preference?", 12),
    ("user", "Somewhere near Alfama with a sea view", 9),
    ("assistant", "The Tagus View Boutique has sea-view rooms at 180 EUR/night.", 16),
    ("tool", "search_hotels(city=Lisbon, area=Alfama) -> 3 results", 14),
    ("user", "What's the cancellation policy?", 6),
    ("assistant", "Free cancellation up to 48 hours before check-in.", 11),
    ("user", "Great, can you also find somewhere with parking?", 10),
    ("assistant", "Yes -- the Tagus View has on-site parking for 20 EUR/day.", 16),
    ("user", "Book it", 2),
    ("assistant", "Booked! Confirmation is LIS-48213. Anything else?", 12),
    ("user", "What's the cancellation policy?", 6),
    ("assistant", "As mentioned, free cancellation up to 48 hours before.", 12),
]


def build_sample_client() -> ConversationClient:
    """A client preloaded with one long-ish conversation: ``conv_lisbon``."""
    base_ts = 1_700_000_000.0
    messages = [
        Message(
            id=f"m{i:03d}",
            conversation_id="conv_lisbon",
            role=role,
            content=content,
            token_count=tokens,
            created_at=base_ts + i,
        )
        for i, (role, content, tokens) in enumerate(_TURNS)
    ]
    return ConversationClient.from_store(
        {
            "conv_lisbon": messages,
            "conv_empty": [],  # a conversation that exists but has no messages
        }
    )


def _demo() -> None:
    client = build_sample_client()
    # Intentionally small page size so you can watch the cursor change.
    page = client.get_messages("conv_lisbon", limit=4)
    print("first page items:", len(page.items))
    print("first next_cursor:", page.next_cursor)
    page2 = client.get_messages("conv_lisbon", cursor=page.next_cursor, limit=4)
    print("second page items:", len(page2.items))
    print("first message of page 2:", page2.items[0].content)


if __name__ == "__main__":
    _demo()
