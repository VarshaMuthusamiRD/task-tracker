## Handoff

### Goal
Building a small in-memory task tracker (`TaskStore`) with status/tag support and summary reporting. Currently extending it with tag-based lookup and due dates so tasks can carry a deadline.

### Done so far
- `8f8a12c`–`4fdbc9b`–`47142b1`–`05d5f2f`–`a1adebb`: core `TaskStore`/`completion_rate` plus four bug fixes (unguarded `find()` in `set_status`, `all()` leaking the live list, tags shared across tasks via a mutable default, completion rate computed against the wrong denominator).
- `3c2701b`: added `TaskStore.by_tag(tag)` returning tasks matching a given tag, with tests.
- **Uncommitted, not yet reviewed/tested by anyone but me:** `due_date` field added to `TaskStore.add()` (optional, ISO `"YYYY-MM-DD"` string, validated via `datetime.date.fromisoformat`), 4 new tests in `tests/test_store.py`, and `demo.py` updated to print each task's due date. All 17 tests pass locally (`python -m unittest discover`) and `python demo.py` output looks correct.

### Decisions made (and why)
- Stored `due_date` as a plain ISO date string, not a `datetime`/`date` object — keeps tasks as plain JSON-serializable dicts, consistent with how `status`/`tags` are already stored as primitives.
- Made `due_date` optional (default `None`) rather than required — keeps `store.add("title")` backward compatible with existing calls in `demo.py` and the test suite.
- Validation lives inline in `add()` (a `try/except` around `datetime.date.fromisoformat`), not in a separate validators module — this project has no existing validation layer (`VALID_STATUSES` is defined but not even enforced), so a new abstraction for one field would be inconsistent with the current style.
- Raise `ValueError` (not a custom exception) on a bad `due_date` string — matches what `fromisoformat` itself raises, and mirrors the existing precedent of using stdlib-appropriate exceptions (`set_status` uses `KeyError` for a *lookup* failure, which is a different kind of error).

### Tried and rejected
- Considered making `due_date` a required argument to `add()` — rejected because it would break `demo.py`'s `store.add("Ship the feature")` call and all existing tests that call `add()` with just a title, for no real benefit.

### Next step
Commit the `due_date` changes (`tasks/store.py`, `tests/test_store.py`, `demo.py`) — not yet committed, waiting on explicit go-ahead per this session's workflow (fixes are implemented but only committed when asked).

### Open questions
- `TaskStore.add_tag()` still doesn't guard against an unknown `task_id` the way `set_status` does (it will raise `AttributeError` on `None["tags"]` instead of a clean error) — flagged twice this session, not yet fixed or explicitly deferred.
- No enforcement anywhere of `VALID_STATUSES` — `set_status`/`add` will happily accept any string as a status. Not in scope for the due-date work, but worth deciding whether/when to address.
- Untracked `tests/test_reports.py` and `__pycache__/` dirs are sitting in the working tree — `test_reports.py` looks intentional (covers `completion_rate`) but has never been committed; worth confirming it should be added.
