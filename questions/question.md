# Sierra — Software Engineering Interview

**Duration:** 45 minutes
**Environment:** Python · CoderPad-style codebase

## Background

You're working on Sierra's conversational agent platform.

Agents interact with customers across multi-turn conversations. For example, a
hotel-booking assistant might help a customer search for hotels, compare
options, and complete a reservation over several messages.

These conversations are stored by a separate service and can be accessed through
an existing API client.

Your task is to implement several features that help agents retrieve, manage, and
retain conversation information.

## Provided Codebase

The project contains the following files:

```
sierra/
    models.py      # Message, Page data models
    client.py      # ConversationClient — your entry point
    _backend.py    # the conversation service (implementation detail)
    sandbox.py     # sample data + a runnable demo

candidate.py       # implement your solutions here

tests/
    test_part1.py
    test_part2.py
    test_part3.py

questions/
    question.md
    part1.md
    part2.md
    part3.md
```

The existing codebase provides the conversation service, client interface, and
data models. Implement your solutions in `candidate.py`, using the provided
interfaces.

> The conversation service is **simulated locally**, but treat it like a real
> remote API: its internals (`sierra/_backend.py`) are an implementation detail.
> Everything you need is on the client's public surface — part of the task is
> discovering that contract by reading the code.

**Read these first:** `sierra/models.py` (the shapes you'll handle) and
`sierra/client.py` (how you talk to the service). You can also run the demo:

```bash
python -m sierra.sandbox
```

## Interview Tasks

The interview consists of three progressive parts. **Each part builds on the
previous implementation.** Additional requirements and constraints are provided
in the corresponding question file.

### Part 1 — Conversation History
Implement functionality to retrieve a complete conversation history from the
provided service. See `questions/part1.md`.

### Part 2 — Context Management
Extend the system to manage conversation history within a configurable token
budget. See `questions/part2.md`.

### Part 3 — Query Retention
Extend the conversation system to track frequently occurring user queries while
maintaining a bounded collection. See `questions/part3.md`.

## Running the tests

```bash
pytest -q                      # run everything
pytest tests/test_part1.py -q  # one part at a time
```

- `tests/test_client_smoke.py` tests the **provided** client and should pass
  immediately — if it fails, fix your environment first.
- `tests/test_part1.py`, `test_part2.py`, `test_part3.py` test **your** code and
  are expected to **fail until you implement each part**.

---

## Provenance — reported vs. constructed

To be upfront about what this mock is and isn't:

- **Reported** (from candidate accounts of Sierra interviews): a 45-minute
  CoderPad round working in an existing codebase; three progressive parts built
  on one another; Part 1 involved **cursor pagination** against an API client
  using a `next_cursor`; Part 2 involved **context/compaction** evicting older
  entries once a token/context-window limit is exceeded; Part 3 involved
  **retaining the top ~20 queries** and dealing with repeated queries.
- **Constructed / assumed** (invented to make a runnable exercise): the specific
  hotel-booking domain, all class/function names and signatures, the exact
  `Message`/`Page` fields, the opaque-cursor mechanics, every token count, the
  precise edge-case rules in Parts 2–3, and the full Part 3 retention policy
  (the original exact requirements were not reported, so a reasonable, clearly
  specified policy was chosen — see `part3.md`).

Treat the reported items as the "shape" of the real interview and the
constructed items as a faithful-but-invented scaffold to practice against.
