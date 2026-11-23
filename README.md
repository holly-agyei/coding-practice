# Sierra SWE Mock Interview

A realistic ~45-minute CoderPad-style coding interview inspired by reported
Sierra SWE experiences. You get a small, working codebase and extend it across
three progressive parts.

**👉 Start with [`questions/question.md`](questions/question.md).**

## Quick start

```bash
python3 -m venv .venv            # create a virtual environment
source .venv/bin/activate        # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt  # installs pytest

python -m sierra.sandbox         # see the transcript API in action
pytest -q                        # run the test suite
```

## What to expect when you first run the tests

- `tests/test_client_smoke.py` — **passes** (verifies the provided client + your
  environment).
- `tests/test_part1.py`, `test_part2.py`, `test_part3.py` — **fail** until you
  implement each part. That's expected.

## You only edit one file

All your work goes in [`candidate.py`](candidate.py). Read the `sierra/` package
to understand the API; don't modify it.

## Layout

| Path | What it is |
|------|------------|
| `sierra/models.py` | `Message`, `Page` data models |
| `sierra/client.py` | `ConversationClient` — your entry point |
| `sierra/_backend.py` | Simulated remote service (implementation detail) |
| `sierra/sandbox.py` | Sample data + `python -m sierra.sandbox` demo |
| `candidate.py` | **Your workspace** |
| `questions/` | Interview prompts (overview + 3 parts) |
| `tests/` | Executable tests |

See `questions/question.md` for the reported-vs-constructed provenance note.
