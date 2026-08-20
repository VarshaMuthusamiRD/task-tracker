# Debugging Log

## Bug 1: `set_status` crashes with `TypeError` on unknown id

- **Symptom**: `store.set_status(99, "done")` raised `TypeError: 'NoneType' object does not support item assignment`.
- **Hypothesis**: `find()` returns `None` for a missing id, and `set_status` uses that result without checking.
- **Actual cause**: confirmed as hypothesized — `find()` returns `None` on a miss; `set_status` does `task["status"] = status` with no `None` check.
- **Right?**: yes.
- **How proved**: reverted the fix, added a test asserting a clean `KeyError` (not `TypeError`), watched it fail with the original error; reapplied the fix and watched it pass.
- **Next time look at first**: any function that calls `find()` and immediately indexes the result — same pattern existed in `add_tag` too, left unfixed on request.

## Bug 2: `all()` returns a live reference, not a snapshot

- **Symptom**: `len(snapshot)` changed after `store.add()` was called later, even though `snapshot` was captured earlier.
- **Hypothesis**: `all()` returns `self._tasks` directly, so the caller's "snapshot" is the same list object as the store's internal state.
- **Actual cause**: confirmed — `return self._tasks` instead of a copy.
- **Right?**: yes.
- **How proved**: ran the existing test before and after changing `all()` to `return list(self._tasks)`.
- **Next time look at first**: any getter named like it returns a copy (`all`, `snapshot`, `list`) — check whether it actually copies before trusting the name.

## Bug 3: Tags leak between tasks

- **Symptom**: tagging task 1 also added the tag to task 2, which was never tagged.
- **Hypothesis**: `tags=[]` as a default argument in `add()` is a shared mutable default.
- **Actual cause**: confirmed — Python evaluates default args once at function definition, so every `add()` call without an explicit `tags` got the same list object.
- **Right?**: yes.
- **How proved**: ran `test_tags_are_not_shared_between_tasks` before/after switching to `tags=None` with a fresh list built inside the function body.
- **Next time look at first**: any function signature with `=[]`, `={}`, or `=set()` as a default — a classic Python trap, worth a quick scan on any new function.

## Bug 4: `completion_rate` returns the wrong percentage

- **Symptom**: an all-done task list reported `0.0%`; a half-done list reported `100.0%`.
- **Hypothesis**: the function divides by the wrong denominator and/or has an inverted empty-case check.
- **Actual cause**: confirmed both — it divided `done` by `outstanding` instead of by total `tasks`, and returned `0.0` when `outstanding` was empty (the all-done case), which is backwards.
- **Right?**: yes.
- **How proved**: wrote failing tests for all-done, mixed, and empty-list cases first; two failed against the buggy code as predicted; fixed the formula to `len(done) / len(tasks)`; all three passed.
- **Next time look at first**: when a percentage/ratio looks inverted, check the denominator and the base-case guard together — they're often wrong in the same way (using the complement of what the docstring promises).
