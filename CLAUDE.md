# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

An in-memory task tracker: a store for tasks (title, status, tags, due date) and pure functions that compute
summary stats from a list of tasks.

## Commands

```
python -m unittest discover -s tests   # run all tests
python demo.py                         # run the sample report
```

## Structure

- `tasks/store.py` — `TaskStore`: the only place tasks are created or mutated. `find` is the only lookup and
  returns `None` on a miss.
- `tasks/reports.py` — pure functions (e.g. `completion_rate`) over a plain `list[dict]` of tasks. Not coupled
  to `TaskStore`.
- `tests/test_store.py`, `tests/test_reports.py` — one test file per module above, same split.

## Conventions

- A missing task is `None` (from `find`) or `KeyError` (from anything that requires the task to exist) — never
  an unguarded crash on `None`.
- No shared mutable default arguments (`tags=None`, built fresh inside the function — not `tags=[]`).
- Getters that look like they return a copy (`all()`) must return one (`list(self._tasks)`), not the internal list.

## Testing

- `unittest`, stdlib only. One `TestCase` class per module, one test method per behavior.
- A test that reproduces a bug must **fail** an assertion, not error out on an uncaught exception — catch
  broadly and call `self.fail(...)` with the cause if you don't know the exact exception type in advance.
- Cover the edge cases by name when they're the point of the function (e.g. `completion_rate`: all-done, mixed,
  empty), not just one happy-path case.

## Do not

- Do not weaken a test to make it pass. Fix the code, or say the test is wrong and why.
- Do not patch at the point of the crash. `set_status` didn't need a `None` check bolted on — the bug was that
  `find` returning `None` was never handled by its caller; look for the same unguarded pattern elsewhere before
  patching one call site.
- Do not add a dependency for something the standard library already does here (`datetime`, `unittest`).

## Maintenance

Keep this file synchronized with the repository's actual commands,
architecture, and conventions.

Update this file in the same commit whenever a code or tooling change
makes any instruction here inaccurate.

Before changing test commands, project structure, public behavior,
testing conventions, or dependencies, check whether this file needs
an update.

If an instruction is only relevant to a single task or session, do not
add it here; keep it as a prompt instead.