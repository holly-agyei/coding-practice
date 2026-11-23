"""Sierra conversation platform -- interview sandbox.

Public surface you'll care about:

    from sierra import ConversationClient, Message, Page

Everything in modules prefixed with ``_`` simulates a remote service and is an
implementation detail.
"""

from ._backend import ConversationNotFound, InvalidCursor
from .client import ConversationClient
from .models import Message, Page

__all__ = [
    "ConversationClient",
    "ConversationNotFound",
    "InvalidCursor",
    "Message",
    "Page",
]
