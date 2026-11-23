# Sierra — SWE Mock Interview (45 min, CoderPad-style)

> A realistic, build-on-itself coding interview inspired by reported Sierra
> SWE on-site/CoderPad experiences. You are given a small, working codebase and
> asked to extend it across three progressive parts.

## The setup

You've joined a team working on Sierra's conversational agent platform. Agents
hold long, multi-turn conversations with customers (think: a hotel-booking
assistant). Transcripts of those conversations are stored in a service you
access through a provided client. You'll work with that client to build up a
small piece of the agent's memory/context machinery.

**This is not a LeetCode puzzle.** There is a real (small) codebase to read.
Part of the exercise is understanding how the provided pieces fit together
before you write anything. Budget a few minutes up front to read the code.

## What's in the repo

```
sierra/            # provided codebase — READ THIS, don't change it
  models.py        #   Message, Page  (the data you'll handle)
  client.py        #   ConversationClient  (your entry point)
  _backend.py      #   simulated remote service (implementation detail)
  sandbox.py       #   sample data + a runnable demo
candidate.py       # YOUR WORKSPACE — implement everything here
tests/             # executable tests for all three parts
questions/         # these instructions
```

Start here:

1. Read `sierra/models.py` — the shapes you'll pass around.
2. Read `sierra/client.py` — how you talk to the service.
3. Run the demo to see it live: `python -m sierra.sandbox`
4. Open `candidate.py` — the stubs you'll fill in.

> The transcript service is **simulated locally**, but treat it like a real
> remote API: its internals (`sierra/_backend.py`) are an implementation detail
> you shouldn't reach into. Everything you need is on the client's public
> surface, and part of the task is discovering that contract by reading it.

## The three parts

Each part builds on the previous one. Do them in order.

- **Part 1 — Cursor pagination** (`questions/part1.md`): assemble a complete
  conversation transcript from the paginated service.
- **Part 2 — Context compaction** (`questions/part2.md`): keep a bounded,
  token-limited context window over a running conversation.
- **Part 3 — Query retention** (`questions/part3.md`): extend Part 2 to remember
  the most frequent user queries over time.

## Running the tests

```bash
pytest -q                      # run everything
pytest tests/test_part1.py -q  # one part at a time
```

- `tests/test_client_smoke.py` tests the **provided** client and should pass
  immediately. If it fails, your environment is wrong — fix that first.
- `tests/test_part1.py`, `test_part2.py`, `test_part3.py` test **your** code and
  are expected to **fail until you implement each part**.

## How you'll be evaluated (what a real interviewer looks for)

- Do you read and use the existing code instead of reinventing it?
- Correct handling of edge cases (empty input, boundaries, off-by-one).
- Clean, incremental progress — get Part 1 green before starting Part 2.
- Clear communication of assumptions and trade-offs as you go.

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
