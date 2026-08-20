# Prompts Log

Notable prompts from today's debugging session, and what I'd do differently.

## 1. "explain what the test was trying to do and explain whats the root cause, dont change anything yet"

Asked for `test_set_status_rejects_an_unknown_id`'s failure. Got back: the test wants a `KeyError` for an unknown id, but `set_status` dereferences `find()`'s `None` result unguarded, producing `TypeError` instead.
**Would say differently**: nothing — clean diagnosis, no back-and-forth needed.

## 2. "Write a new test... a narrower one aimed at the cause" → rejected first answer

First answer: added a test on `add_tag` (a sibling method with the same bug) instead of `set_status`, reasoning that `set_status` already had test coverage. User pushed back — "why add_tag instead of set_status" — and asked for the `set_status` version too, done properly as a *failure* (not an unhandled error).
**Would say differently**: should have asked which method the "narrower test" should target before picking one on my own, or covered both from the start instead of guessing at scope.

## 3. "it should fail not give error"

Pointed out `assertRaises(KeyError)` produces an `ERROR` (uncaught `TypeError`), not a `FAIL`. Fixed by catching broadly and calling `self.fail()` with a message naming the cause.
**Would say differently**: should have used this pattern by default for any "reproduce the bug" test, since `assertRaises` only cleanly demonstrates a bug if you already know the exact exception type it raises.

## 4. "Write a failing test for the correct behaviour, covering the all-done case, a mixed case, and the empty list"

Had to find the right target first (`completion_rate` in `tasks/reports.py`, untested until now). Wrote three cases; two failed against the buggy implementation as expected, exposing both a wrong denominator and an inverted empty-case guard.
**Would say differently**: nothing — the three-case split (all-done / mixed / empty) was the right minimal set to pin down both bugs in the formula at once.
